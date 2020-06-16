import key
import utility
import json
from collections import defaultdict
from uuid import uuid4

nature_it_continuation_data_file = './data/exercise_it_continuation_natura.json'
nature_en_continuation_data_file = './data/exercise_en_continuation_natura.json'

nature_files = {
    'it': nature_it_continuation_data_file,
    'en': nature_en_continuation_data_file
}

def generate_data_file_from_spreadsheet():    

    spreadsheet_id_gid = key.NATURE_DATA_SPREADSHEET_ID_GID
    spread_dict_list = utility.import_url_csv_to_list_list(*spreadsheet_id_gid)

    it_data = []
    en_data = []
    
    for row in spread_dict_list:
        if not utility.represents_int(row[0]):
            continue
        incipit_it, cont_in = row[2], row[3]
        incipit_en, cont_en = row[4], row[5]
        source = row[6]
        it_data.append({
            'ID': str(uuid4()),
            'INCIPIT': incipit_it,
            'CONTINUATION': cont_in,
            'SOURCE': source
        })
        en_data.append({
            'ID': str(uuid4()),
            'INCIPIT': incipit_en,
            'CONTINUATION': cont_en,
            'SOURCE': source
        })

    with open(nature_it_continuation_data_file, 'w') as f_out:
        json.dump(it_data, f_out, indent=3, ensure_ascii=False)
    
    with open(nature_en_continuation_data_file, 'w') as f_out:
        json.dump(en_data, f_out, indent=3, ensure_ascii=False)


def extract_random_exercises(lang, num_samples):
    import itertools
    import random
    with open(nature_files[lang]) as f_in:
        nature_data = json.load(f_in)
    return random.sample(nature_data, num_samples)


if __name__ == '__main__':
    generate_data_file_from_spreadsheet()
    # result = extract_random_exercises(5)
    # print(json.dumps(result, indent=3))
    