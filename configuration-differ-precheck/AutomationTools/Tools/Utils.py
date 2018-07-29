def parseFileContent(content):
  '''
This function parses a file's content to output it as an array of lines.
  '''
  # TODO: maybe allow for CSV or other formats someday
  # formatting file content as an array of lines
  return [l.strip() for l in content.strip().split('\n')]

def checkPrompt(data):
  lines = data.decode("utf-8").replace('\r','').strip().split('\n')
  if lines[-1].endswith("End-Of-File"): return True
  return False
  # if prompt.upper() in  data[-len(prompt) - 4:] or prompt.lower() in data[-len(prompt)-4:]:
  #  return True

