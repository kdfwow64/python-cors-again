import re 

def IpinRange(mask, IP):
   splitted_IP = IP.split('.')
   for index, current_range in enumerate(mask.split('.')):
      if '-' in current_range:
         mini, maxi = map(int,current_range.split('-'))
      else:
         mini = maxi = int(current_range)
      if not (mini <= int(splitted_IP[index]) <= maxi):
         return 0
   return 1

def GetAllRegExLine(result_lines, value):
  result_text =  "".join(line + "\r\n" for line in result_lines)
  match = re.compile(value)
  is_matched = match.findall(result_text)
  match_lines = []
  if is_matched:
    for mt in is_matched:
      for line in result_lines:
        if mt in line:
          match_lines.append(line)
    return 1, match_lines
  return 0, None

def GetAllRegEx(result_lines, value):
  result_text =  "".join(line + "\r\n" for line in result_lines)
  match = re.compile(value)
  is_matched = match.findall(result_text)
  if is_matched:
    return 1, is_matched
  return 0, None

def GetMatchedRegExLine(result_lines, value):
  result_text =  "".join(line + "\r\n" for line in result_lines)
  is_matched = re.search(value, result_text)
  match_lines = []
  if is_matched:
    for line in result_lines:
      if is_matched.group(0) in line:
        match_lines.append(line)
    return 1, match_lines
  return 0, None

def GetMatchedRegEx(result_lines, value):
  result_text =  "".join(line + "\r\n" for line in result_lines)
  match = re.compile(value)
  is_matched = match.search(result_text)
  match_lines = []
  if is_matched:
    return 1, is_matched.group(0)
  return 0, None

def not_contains(result_lines, value):
  if not value in result_text:
    return 1, None
  return 0, None

def equal(result_lines, value):
  if result_text == value:
    return 1, None
  return 0, None

def not_equal(result_lines, value):
  if result_text != value:
    return 1, None
  return 0, None

def contains(result_lines, value):
  result_text =  "".join(line + "\r\n" for line in result_lines)
  match_lines = []
  if value in result_text:
    for line in result_lines:
      if value in line:
        match_lines.append(line)
    return 1, match_lines
  return 0, None
    
