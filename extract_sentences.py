import key
import utility
import json
from collections import defaultdict

data_file = './data/mwe_en_exercises.json'

def generate_data_file_from_spreadsheet():
    
    # HEADERS:
    # 'MWE', 'SENTENCE', 'ACCEPTED(Y/N)', 'COMMENTS', 'Cleaned Sentence', 
    # 'Text to be highlighted/replaced (if it differs from the string in column A)', 
    # 'Synonyms']
    
    H_MWE_VARIATION = 'Text to be highlighted/replaced (if it differs from the string in column A)'
    spreadsheet_id_gid = key.TEACHER_EXPERIMNET_SPREADSHEET_ID_GID
    spread_dict_list = utility.get_google_spreadsheet_dict_list(*spreadsheet_id_gid)
    
    result_dict = defaultdict(list)
    for d in spread_dict_list:
        if d['ACCEPTED(Y/N)'] != 'Y':
            continue
        mwe_type = d['MWE']
        mwe_occurrence = d[H_MWE_VARIATION] if d[H_MWE_VARIATION] else d['MWE']        
        sentence = d['Cleaned Sentence'] if d['Cleaned Sentence'] else d['SENTENCE']
        if sentence.count(mwe_occurrence) != 1:
            continue
        result_dict[mwe_type].append({'SENTENCE': sentence, 'MWE': mwe_occurrence})        
    
    with open(data_file, 'w') as f_out:
        json.dump(result_dict, f_out, indent=3, ensure_ascii=False)

def extract_random_exercises(num_samples):
    import itertools
    import random
    with open(data_file) as f_in:
        mwe_dict = json.load(f_in)
    result = []
    round_robin_mwe_types = itertools.cycle(mwe_dict.values())
    while len(result) != num_samples:
        next_mwe = random.choice(next(round_robin_mwe_types))
        if next_mwe not in result:
            result.append(next_mwe)
    print(json.dumps(result, indent=3))
    return result




if __name__ == '__main__':
    # generate_data_file_from_spreadsheet()
    extract_random_exercises(5)
    