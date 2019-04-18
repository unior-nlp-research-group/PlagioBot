# https://firebase.google.com/docs/firestore/manage-data/add-data
from google.cloud import firestore
from google.cloud.firestore_v1beta1 import ArrayRemove, ArrayUnion

# https://gitlab.com/futureprojects/firestore-model/blob/master/examples/main.py
import firestore_model
from firestore_model import Model

db = firestore.Client()
firestore_model.db = db
# transaction = db.transaction()

def set_doc_in_collection():
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('cities').document('LA').set(
        {
            'name': 'Los Angeles',
            'state': 'CA',
            'country': 'USA',
            'dizionario': {
                '0': 'one',
                '1': 'two',
                '2': 'three',
                'sub': {
                    '0': 'one',
                    '1': 'two',
                    '2': 'three'
                }
            },
            'list': [{'a':1},2,3]
        }
    )

def test_array_union():
    city_ref = db.collection(u'cities').document(u'DC')

    # Atomically add a new region to the 'regions' array field.
    city_ref.update({u'regions': db.ArrayUnion([u'greater_virginia'])})

    # // Atomically remove a region from the 'regions' array field.
    city_ref.update({u'regions': ArrayRemove([u'east_coast'])})


if __name__ == "__main__":
    # set_doc_in_collection()
    pass