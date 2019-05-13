from time import time

def flatten(L):
    ret = []
    for i in L:
        if isinstance(i,list):
            ret.extend(flatten(i))
        else:
            ret.append(i)
    return ret

def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def represents_int_between(s, low, high):
    if not represents_int(s):
        return False
    sInt = int(s)
    if sInt>=low and sInt<=high:
        return True
    return False

MARKDOWN_CHARS = '*_`['

def contains_markdown(text):
    return any(c in text for c in MARKDOWN_CHARS)

def escape_markdown(text):
    for char in MARKDOWN_CHARS:
        text = text.replace(char, '\\'+char)
    return text

def remove_markdown(text):
    for char in MARKDOWN_CHARS:
        text = text.replace(char, '')
    return text

def add_full_stop_if_missing_end_puct(text):
    if text[-1] not in ['.','!','?']:
        text = text + '.'
    return text

def normalize_apostrophe(text):    
    for char in '’`':
        text = text.replace(char, "'")
    return text

def normalize_completion(text):
    text = add_full_stop_if_missing_end_puct(text)
    return text

def get_milliseconds():
  """
    @return Milliseconds since the epoch
  """
  return int(round(time() * 1000))
