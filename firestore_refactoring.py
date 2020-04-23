from google.cloud import firestore

def reset_timestamps():
    import datetime
    db = firestore.Client()
    for col in ['Game','User','test_Game','test_User']:
        num_changed = 0
        docs = db.collection(col).stream()
        batch = db.batch()
        for d in docs:
            d_dict = d.to_dict()
            changed = False
            for field_name in ['created', 'modified']:
                field_value = d_dict[field_name]
                d_ref = db.collection(col).document(d.id)
                if isinstance(field_value,int):
                    changed = True
                    timestamp = datetime.datetime.fromtimestamp(field_value/1000.0)
                    batch.update(d_ref, {field_name: timestamp})
            if changed:
                num_changed += 1
        print('{} -> {}'.format(col, num_changed))
        batch.commit()
    
    # city_ref.update({u'capital': True})

def check_timestamp():
    db = firestore.Client()
    d = db.collection('test_Game').document('TEST_1586753289838').get()
    d_dict = d.to_dict()    
    print(u'{} => created: {} ({}), modified: {} ({})'.format(
        d_dict['id'], 
        d_dict['created'], isinstance(d_dict['created'],int),
        d_dict['modified'], isinstance(d_dict['modified'],int))
    )


if __name__ == "__main__":
    reset_timestamps()
    # check_timestamp()
