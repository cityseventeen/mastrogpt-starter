import os, requests as req, json, socket

MODEL="llama3.1:8b"
#MODEL="deepseek-r1:32b"

from enum import Enum
class MODEL_LIST(Enum):
  llama =  "llama3.1:8b"
  deepseek = "deepseek-r1:32b"



def url(args):
  #TODO:E2.1
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  #END TODO
  base = f"https://{auth}@{host}"
  return f"{base}/api/generate"

import json, socket, traceback
def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT"))
  print(f"DEBUG  {sock}  {port}")
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sock, port))
    try:
      for line in lines:
        #print(line, end='')     
        #TODO:E2.2 fix this streaming implementation
        # line is a json string and you have to extract only the "response" field

        response_extracted = json.loads(line.decode("utf-8")).get("response", "error")

        msg = {"output": response_extracted}
        out += response_extracted
        #END TODO
        s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
  return out

def stateless(args):
  global MODEL
  global MODEL_LIST
  llm = url(args)
  out = f"Welcome to {MODEL}"
  inp = args.get("input", "")
  if inp != "":
    message_to_model_const = "Who are you?"
    #TODO:E2.3 
    model = MODEL #default
    message_to_model = ""
    if inp in MODEL_LIST.__members__:
      model = chooseModel(inp)
      message_to_model = message_to_model_const
    else:
      message_to_model = inp

    # add if to switch to llama3.1:8b or deepseek-r1:32b
    # on input 'llmama' or 'deepseek' and change the inp to "who are you"
    #END TODO

    msg = { "model": MODEL, "prompt": "message_to_model", "stream": True }
    lines = req.post(llm, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}




def chooseModel(input):
  global MODEL_LIST
  if input in MODEL_LIST.__members__:
    return MODEL_LIST.__members__[input].value
  else:
    raise Exception("Modello non presente in lista")
