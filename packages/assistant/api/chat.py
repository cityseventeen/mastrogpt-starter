import os
import openai

MODEL = "llama3.1:8b"
ROLE = "system:You are an helpful assistant."

#TODO:E4.1 add the stream function
#fix it to extract line.choices[0].delta.content
#END TODO

# init added by me
import json, socket, traceback
def streamer(args, lines):
  sock = args.get("STREAM_HOST") ; port = int(args.get("STREAM_PORT"))
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        msg = {"output": line}
        s.sendall(json.dumps(msg).encode("utf-8"))
        out += str(line) #; print(line, end='')
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

# end added by me


class Chat:
    def __init__(self, args):
        
        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        api_key = args.get("AUTH", os.getenv("AUTH"))
        base_url = f"https://{api_key}@{host}/v1"
        
        self.client = openai.OpenAI(
            base_url = base_url,
            api_key = api_key,
        )
        
        self.messages = []
        self.add(ROLE)
        
        self.args = args # added by me
        #TODO:E4.1 
        # save args in a field
        #END TODO
        
    def add(self, msg):
        [role, content] = msg.split(":", maxsplit=1)
        self.messages.append({
            "role": role,
            "content": content,
        })
    
    def complete(self):
        #TODO:E4.1 
        # add stream: True
        res = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
            stream = True # added by me
        )
        # END TODO
        try: 
            out_streamed = ""
            #TODO:E4.1 stream the result 
            # modified with for
            for m in res:
                out_streamed = m.choices[0].delta.content # modified messages in delta
            #END TODO
            self.add(f"assistant:{out}")
        except:
            out =  "error"
        return out
    
