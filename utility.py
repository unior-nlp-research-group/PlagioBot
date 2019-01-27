# -*- coding: utf-8 -*-

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

def escape_markdown(text):
    for char in '*_`[':
        text = text.replace(char, '\\'+char)
    return text

def add_full_stop_if_missing_end_puct(text):
    if text[-1] not in ['.','!','?']:
        text = text + '.'
    return text