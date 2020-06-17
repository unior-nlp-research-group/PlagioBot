import key
import utility
import json
from collections import defaultdict
from uuid import uuid4

synonym_data_file = './data/exercises_en_synonym_mwe.json'

def generate_data_file_from_spreadsheet():
    
    # HEADERS:
    # 'MWE', 'SENTENCE', 'ACCEPTED(Y/N)', 'COMMENTS', 'Cleaned Sentence', 
    # 'Text to be highlighted/replaced (if it differs from the string in column A)', 
    # 'Synonyms']
    
    H_MWE_VARIATION = 'Text to be highlighted/replaced (if it differs from the string in column A)'
    spreadsheet_id_gid = key.MWE_DATA_SPREADSHEET_ID_GID
    spread_dict_list = utility.import_url_csv_to_dict_list(*spreadsheet_id_gid)
    
    mwe_type_sentences_dict = defaultdict(list)
    accepted_mwe_types = []
    for d in spread_dict_list:
        if d['ACCEPTED(Y/N)'] != 'Y':
            continue
        if not d['Synonyms (comma separated)']:
            continue
        mwe_type = d['MWE']
        mwe_text = d[H_MWE_VARIATION] if d[H_MWE_VARIATION] else d['MWE']        
        sentence = d['Cleaned Sentence'] if d['Cleaned Sentence'] else d['SENTENCE']
        if sentence.count(mwe_text) != 1:
            print("'{}' not in '{}'".format(mwe_text, sentence))
            continue
        mwe_type_sentences_dict[mwe_type].append(
            {
                'ID': str(uuid4()),
                'SENTENCE': sentence, 
                'REPLACEMENT': mwe_text
            }
        )        
        if mwe_type not in accepted_mwe_types:
            accepted_mwe_types.append(mwe_type)
    
    accepted_mwe_types = [m for m in accepted_mwe_types if len(mwe_type_sentences_dict[m])>=2]
    group_size = 5
    batches = utility.split_list(accepted_mwe_types, group_size)
    
    if len(batches[-1]) < group_size:
        batches = batches[:-1]

    batch_mwe_type_sentences_dict = {}
    for batch_num, mwe_batch in enumerate(batches,1):
        print("MWE Batch {}: {}".format(batch_num, mwe_batch))
        batch_title = "MWE {}".format(batch_num)
        batch_mwe_type_sentences_dict[batch_title] = {
            k:v for k,v in mwe_type_sentences_dict.items()
            if k in mwe_batch
        }

    with open(synonym_data_file, 'w') as f_out:
        json.dump(batch_mwe_type_sentences_dict, f_out, indent=3, ensure_ascii=False)


def get_exercise_batch_title_and_description():
    with open(synonym_data_file) as f_in:
        batch_exercise_dict = json.load(f_in)
    return [
        {batch_title: ', '.join(sorted(ex.keys()))}
        for batch_title, ex in batch_exercise_dict.items()
    ]


def extract_random_exercises(batch_title, num_samples):
    import itertools
    import random
    with open(synonym_data_file) as f_in:
        mwe_dict = json.load(f_in)
    batch_mwe_dict = mwe_dict[batch_title]
    result = []
    round_robin_mwe_types = itertools.cycle(batch_mwe_dict.values())
    while len(result) != num_samples:
        next_mwe = random.choice(next(round_robin_mwe_types))
        if next_mwe not in result:
            result.append(next_mwe)    
    return result


if __name__ == '__main__':
    generate_data_file_from_spreadsheet()
    # result = extract_random_exercises(5)
    # print(json.dumps(result, indent=3))
    