def reverse(args):
  inp = args.get("input", "")
  out = "Scrivi qualcosa e ti farò il reverse"
  if inp!="":
   out = inp[::-1]
  return {
    "output": out }
