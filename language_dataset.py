import key
import utility
import json
from collections import defaultdict
from uuid import uuid4

DATASET_INDEX = None
# list of dictionaries with keys: ['Name', 'Lang', 'Type', 'Sheet Name', 'GID', 'Description']

def update():
    global DATASET_INDEX
    spreadsheet_id_gid = key.LANGAUGE_DATASET_INDEX_GID
    DATASET_INDEX = utility.import_url_csv_to_dict_list(*spreadsheet_id_gid)

def get_exercise_list(lang, type):
    if DATASET_INDEX == None:
        update()
    return [e for e in DATASET_INDEX if e['Lang']==lang.upper() and e['Type']==type]

def get_exercise_random_sample(gid, num_samples):
    import random
    exercise = utility.import_url_csv_to_dict_list(key.LANGAUGE_DATASET_INDEX_GID[0], gid)
    return random.sample(exercise, num_samples)


if __name__ == '__main__':
    pass
    