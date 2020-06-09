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
MARKDOWN_CHARS_SLASH = MARKDOWN_CHARS + ' /'

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

PUNCTUATION = ['.','!','?',':',';']

def add_full_stop_if_missing_end_puct(text):
    if text[-1] not in PUNCTUATION:
        text = text + '.'
    return text

def remove_trailing_punctuation(text):
    if text[-1] in PUNCTUATION:
        return remove_trailing_punctuation(text[:-1])
    else:
        return text

def normalize_apostrophe(text):    
    for char in '’`':
        text = text.replace(char, "'")
    return text

def check_if_substitue_suggestion_matches_prefix_suffix(text, replacement_in_text, answer):
    text = remove_trailing_punctuation(text)
    answer = remove_trailing_punctuation(answer)
    prefix_end = text.index(replacement_in_text)
    suffix_start = prefix_end + len(replacement_in_text)
    prefix = text[:prefix_end]
    suffix = text[suffix_start:]
    return answer.startswith(prefix) and answer.endswith(suffix)

def has_parenthesis_in_correct_format(text):
    open_index = text.find('(')
    close_index = text.find(')')
    return open_index!=-1 and close_index!=-1 and open_index < close_index

def distribute_elements(seq, max_size=5):
    if len(seq)==0:
        return []
    lines = len(seq) // max_size
    if len(seq) % max_size > 0:
        lines += 1
    avg = len(seq) / float(lines)
    result = []
    last = 0.0
    while last < len(seq):
        result.append(seq[int(last):int(last + avg)])
        last += avg
    return result

def split_list(iterable, group_size):
    from itertools import zip_longest
    args = [iter(iterable)] * group_size
    return list(([e for e in t if e != None] for t in zip_longest(*args)))

def get_milliseconds():
    from time import time
    return int(round(time() * 1000))    

def clean_new_lines(s):
    return s.replace('\\n', '\n').strip()

# if spreadsheet has header
def import_url_csv_to_dict_list(spreadsheed_id, gid, remove_new_line_escape=True): #escapeMarkdown=True
    import csv
    import requests
    url = 'https://docs.google.com/spreadsheets/d/{}/export?gid={}&format=csv'.format(spreadsheed_id, gid)
    r = requests.get(url)
    r.encoding = "utf-8"
    spreadsheet_csv = r.text.split('\n')
    reader = csv.DictReader(spreadsheet_csv)
    if remove_new_line_escape:
        return [
            {
                clean_new_lines(k): clean_new_lines(v)
                for k,v in dict.items()
            } for dict in reader
        ]
    return [dict for dict in reader]

# if spreadsheet has no header
def import_url_csv_to_list_list(spreadsheed_id, gid, remove_new_line_escape=True): #escapeMarkdown=True
    import csv
    import requests
    url = 'https://docs.google.com/spreadsheets/d/{}/export?gid={}&format=csv'.format(spreadsheed_id, gid)
    r = requests.get(url)
    r.encoding = "utf-8"
    spreadsheet_csv = r.text.split('\n') 
    reader = csv.reader(spreadsheet_csv)
    result = list(reader)
    result = [[clean_new_lines(x) for x in l] for l in result ]
    return result
