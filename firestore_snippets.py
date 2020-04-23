# Copyright 2017, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import threading
from time import sleep

from google.cloud import firestore


def quickstart_new_instance():
    # [START quickstart_new_instance]
    from google.cloud import firestore

    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()
    # [END quickstart_new_instance]

    return db


def quickstart_add_data_one():
    db = firestore.Client()
    # [START quickstart_add_data_one]
    doc_ref = db.collection('users').document('alovelace')
    doc_ref.set({
        'first': 'Ada',
        'last': 'Lovelace',
        'born': 1815
    })
    # [END quickstart_add_data_one]


def quickstart_add_data_two():
    db = firestore.Client()
    # [START quickstart_add_data_two]
    doc_ref = db.collection('users').document('aturing')
    doc_ref.set({
        'first': 'Alan',
        'middle': 'Mathison',
        'last': 'Turing',
        'born': 1912
    })
    # [END quickstart_add_data_two]


def quickstart_get_collection():
    db = firestore.Client()
    # [START quickstart_get_collection]
    users_ref = db.collection('users')
    docs = users_ref.stream()

    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))
    # [END quickstart_get_collection]


def add_from_dict():
    db = firestore.Client()
    # [START add_from_dict]
    data = {
        'name': 'Los Angeles',
        'state': 'CA',
        'country': 'USA'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('cities').document('LA').set(data)
    # [END add_from_dict]


def add_data_types():
    db = firestore.Client()
    # [START add_data_types]
    data = {
        'stringExample': 'Hello, World!',
        'booleanExample': True,
        'numberExample': 3.14159265,
        'dateExample': datetime.datetime.now(),
        'arrayExample': [5, True, 'hello'],
        'nullExample': None,
        'objectExample': {
            'a': 5,
            'b': True
        }
    }

    db.collection('data').document('one').set(data)
    # [END add_data_types]


# [START custom_class_def]
class City(object):
    def __init__(self, name, state, country, capital=False, population=0,
                 regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = City(source['name'], source['state'], source['country'])

        if 'capital' in source:
            city.capital = source['capital']

        if 'population' in source:
            city.population = source['population']

        if 'regions' in source:
            city.regions = source['regions']

        return city
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            'name': self.name,
            'state': self.state,
            'country': self.country
        }

        if self.capital:
            dest['capital'] = self.capital

        if self.population:
            dest['population'] = self.population

        if self.regions:
            dest['regions'] = self.regions

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            'City(name={}, country={}, population={}, capital={}, regions={})'
            .format(self.name, self.country, self.population, self.capital,
                    self.regions))
# [END custom_class_def]


def add_example_data():
    db = firestore.Client()
    # [START add_example_data]
    cities_ref = db.collection('cities')
    cities_ref.document('BJ').set(
        City('Beijing', None, 'China', True, 21500000, ['hebei']).to_dict())
    cities_ref.document('SF').set(
        City('San Francisco', 'CA', 'USA', False, 860000,
             ['west_coast', 'norcal']).to_dict())
    cities_ref.document('LA').set(
        City('Los Angeles', 'CA', 'USA', False, 3900000,
             ['west_coast', 'socal']).to_dict())
    cities_ref.document('DC').set(
        City('Washington D.C.', None, 'USA', True, 680000,
             ['east_coast']).to_dict())
    cities_ref.document('TOK').set(
        City('Tokyo', None, 'Japan', True, 9000000,
             ['kanto', 'honshu']).to_dict())
    # [END add_example_data]


def add_custom_class_with_id():
    db = firestore.Client()
    # [START add_custom_class_with_id]
    city = City(name='Los Angeles', state='CA', country='USA')
    db.collection('cities').document('LA').set(city.to_dict())
    # [END add_custom_class_with_id]


def add_data_with_id():
    db = firestore.Client()
    data = {}
    # [START add_data_with_id]
    db.collection('cities').document('new-city-id').set(data)
    # [END add_data_with_id]


def add_custom_class_generated_id():
    db = firestore.Client()
    # [START add_custom_class_generated_id]
    city = City(name='Tokyo', state=None, country='Japan')
    db.collection('cities').add(city.to_dict())
    # [END add_custom_class_generated_id]


def add_new_doc():
    db = firestore.Client()
    # [START add_new_doc]
    new_city_ref = db.collection('cities').document()

    # later...
    new_city_ref.set({
        # ...
    })
    # [END add_new_doc]


def get_check_exists():
    db = firestore.Client()
    # [START get_check_exists]
    doc_ref = db.collection('cities').document('SF')

    doc = doc_ref.get()
    if doc.exists:
        print('Document data: {}'.format(doc.to_dict()))
    else:
        print('No such document!')
    # [END get_check_exists]


def get_custom_class():
    db = firestore.Client()
    # [START get_custom_class]
    doc_ref = db.collection('cities').document('BJ')

    doc = doc_ref.get()
    city = City.from_dict(doc.to_dict())
    print(city)
    # [END get_custom_class]


def get_simple_query():
    db = firestore.Client()
    # [START get_simple_query]
    docs = db.collection('cities').where('capital', '==', True).stream()

    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))
    # [END get_simple_query]


def array_contains_filter():
    db = firestore.Client()
    # [START fs_array_contains_filter]
    cities_ref = db.collection('cities')

    query = cities_ref.where('regions', 'array_contains', 'west_coast')
    # [END fs_array_contains_filter]
    docs = query.stream()
    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))


def get_full_collection():
    db = firestore.Client()
    # [START get_full_collection]
    docs = db.collection('cities').stream()

    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))
    # [END get_full_collection]


def structure_doc_ref():
    db = firestore.Client()
    # [START structure_doc_ref]
    a_lovelace_ref = db.collection('users').document('alovelace')
    # [END structure_doc_ref]
    print(a_lovelace_ref)


def structure_collection_ref():
    db = firestore.Client()
    # [START structure_collection_ref]
    users_ref = db.collection('users')
    # [END structure_collection_ref]
    print(users_ref)


def structure_doc_ref_alternate():
    db = firestore.Client()
    # [START structure_doc_ref_alternate]
    a_lovelace_ref = db.document('users/alovelace')
    # [END structure_doc_ref_alternate]

    return a_lovelace_ref


def structure_subcollection_ref():
    db = firestore.Client()
    # [START structure_subcollection_ref]
    room_a_ref = db.collection('rooms').document('roomA')
    message_ref = room_a_ref.collection('messages').document('message1')
    # [END structure_subcollection_ref]
    print(message_ref)


def update_doc():
    db = firestore.Client()
    db.collection('cities').document('DC').set(
        City('Washington D.C.', None, 'USA', True, 680000,
             ['east_coast']).to_dict())

    # [START update_doc]
    city_ref = db.collection('cities').document('DC')

    # Set the capital field
    city_ref.update({'capital': True})
    # [END update_doc]


def update_doc_array():
    db = firestore.Client()
    db.collection('cities').document('DC').set(
        City('Washington D.C.', None, 'USA', True, 680000,
             ['east_coast']).to_dict())

    # [START fs_update_doc_array]
    city_ref = db.collection('cities').document('DC')

    # Atomically add a new region to the 'regions' array field.
    city_ref.update({'regions': firestore.ArrayUnion(['greater_virginia'])})

    # // Atomically remove a region from the 'regions' array field.
    city_ref.update({'regions': firestore.ArrayRemove(['east_coast'])})
    # [END fs_update_doc_array]
    city = city_ref.get()
    print('Updated the regions field of the DC. {}'.format(city.to_dict()))


def update_multiple():
    db = firestore.Client()
    db.collection('cities').document('DC').set(
        City('Washington D.C.', None, 'USA', True, 680000,
             ['east_coast']).to_dict())

    # [START update_multiple]
    doc_ref = db.collection('cities').document('DC')

    doc_ref.update({
        'name': 'Washington D.C.',
        'country': 'USA',
        'capital': True
    })
    # [END update_multiple]


def update_create_if_missing():
    db = firestore.Client()
    # [START update_create_if_missing]
    city_ref = db.collection('cities').document('BJ')

    city_ref.set({
        'capital': True
    }, merge=True)
    # [END update_create_if_missing]


def update_nested():
    db = firestore.Client()
    # [START update_nested]
    # Create an initial document to update
    frank_ref = db.collection('users').document('frank')
    frank_ref.set({
        'name': 'Frank',
        'favorites': {
            'food': 'Pizza',
            'color': 'Blue',
            'subject': 'Recess'
        },
        'age': 12
    })

    # Update age and favorite color
    frank_ref.update({
        'age': 13,
        'favorites.color': 'Red'
    })
    # [END update_nested]


def update_server_timestamp():
    db = firestore.Client()
    # [START update_server_timestamp]
    city_ref = db.collection('objects').document('some-id')
    city_ref.update({
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    # [END update_server_timestamp]


def update_data_transaction():
    db = firestore.Client()
    # [START update_data_transaction]
    transaction = db.transaction()
    city_ref = db.collection('cities').document('SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        transaction.update(city_ref, {
            'population': snapshot.get('population') + 1
        })

    update_in_transaction(transaction, city_ref)
    # [END update_data_transaction]


def update_data_transaction_result():
    db = firestore.Client()
    # [START update_data_transaction_result]
    transaction = db.transaction()
    city_ref = db.collection('cities').document('SF')

    @firestore.transactional
    def update_in_transaction(transaction, city_ref):
        snapshot = city_ref.get(transaction=transaction)
        new_population = snapshot.get('population') + 1

        if new_population < 1000000:
            transaction.update(city_ref, {
                'population': new_population
            })
            return True
        else:
            return False

    result = update_in_transaction(transaction, city_ref)
    if result:
        print('Population updated')
    else:
        print('Sorry! Population is too big.')
    # [END update_data_transaction_result]


def update_data_batch():
    db = firestore.Client()
    # [START update_data_batch]
    batch = db.batch()

    # Set the data for NYC
    nyc_ref = db.collection('cities').document('NYC')
    batch.set(nyc_ref, {'name': 'New York City'})

    # Update the population for SF
    sf_ref = db.collection('cities').document('SF')
    batch.update(sf_ref, {'population': 1000000})

    # Delete DEN
    den_ref = db.collection('cities').document('DEN')
    batch.delete(den_ref)

    # Commit the batch
    batch.commit()
    # [END update_data_batch]


def compound_query_example():
    db = firestore.Client()
    # [START compound_query_example]
    # Create a reference to the cities collection
    cities_ref = db.collection('cities')

    # Create a query against the collection
    query_ref = cities_ref.where('state', '==', 'CA')
    # [END compound_query_example]

    return query_ref


def compound_query_simple():
    db = firestore.Client()
    # [START compound_query_simple]
    cities_ref = db.collection('cities')

    query = cities_ref.where('capital', '==', True)
    # [END compound_query_simple]

    print(query)


def compound_query_single_clause():
    db = firestore.Client()
    # [START compound_query_single_clause]
    cities_ref = db.collection('cities')

    cities_ref.where('state', '==', 'CA')
    cities_ref.where('population', '<', 1000000)
    cities_ref.where('name', '>=', 'San Francisco')
    # [END compound_query_single_clause]


def compound_query_valid_multi_clause():
    db = firestore.Client()
    # [START compound_query_valid_multi_clause]
    cities_ref = db.collection('cities')

    denver_query = cities_ref.where(
        'state', '==', 'CO').where('name', '==', 'Denver')
    large_us_cities_query = cities_ref.where(
        'state', '==', 'CA').where('population', '>', 1000000)
    # [END compound_query_valid_multi_clause]
    print(denver_query)
    print(large_us_cities_query)


def compound_query_valid_single_field():
    db = firestore.Client()
    # [START compound_query_valid_single_field]
    cities_ref = db.collection('cities')
    cities_ref.where('state', '>=', 'CA').where('state', '<=', 'IN')
    # [END compound_query_valid_single_field]


def compound_query_invalid_multi_field():
    db = firestore.Client()
    # [START compound_query_invalid_multi_field]
    cities_ref = db.collection('cities')
    cities_ref.where(
        'state', '>=', 'CA').where('population', '>=', 1000000)
    # [END compound_query_invalid_multi_field]


def order_simple_limit():
    db = firestore.Client()
    # [START order_simple_limit]
    db.collection('cities').order_by('name').limit(3).stream()
    # [END order_simple_limit]


def order_simple_limit_desc():
    db = firestore.Client()
    # [START order_simple_limit_desc]
    cities_ref = db.collection('cities')
    query = cities_ref.order_by(
        'name', direction=firestore.Query.DESCENDING).limit(3)
    results = query.stream()
    # [END order_simple_limit_desc]
    print(results)


def order_multiple():
    db = firestore.Client()
    # [START order_multiple]
    cities_ref = db.collection('cities')
    cities_ref.order_by('state').order_by(
        'population', direction=firestore.Query.DESCENDING)
    # [END order_multiple]


def order_where_limit():
    db = firestore.Client()
    # [START order_where_limit]
    cities_ref = db.collection('cities')
    query = cities_ref.where(
        'population', '>', 2500000).order_by('population').limit(2)
    results = query.stream()
    # [END order_where_limit]
    print(results)


def order_where_valid():
    db = firestore.Client()
    # [START order_where_valid]
    cities_ref = db.collection('cities')
    query = cities_ref.where(
        'population', '>', 2500000).order_by('population')
    results = query.stream()
    # [END order_where_valid]
    print(results)


def order_where_invalid():
    db = firestore.Client()
    # [START order_where_invalid]
    cities_ref = db.collection('cities')
    query = cities_ref.where('population', '>', 2500000).order_by('country')
    results = query.stream()
    # [END order_where_invalid]
    print(results)


def cursor_simple_start_at():
    db = firestore.Client()
    # [START cursor_simple_start_at]
    cities_ref = db.collection('cities')
    query_start_at = cities_ref.order_by('population').start_at({
        'population': 1000000
    })
    # [END cursor_simple_start_at]

    return query_start_at


def cursor_simple_end_at():
    db = firestore.Client()
    # [START cursor_simple_end_at]
    cities_ref = db.collection('cities')
    query_end_at = cities_ref.order_by('population').end_at({
        'population': 1000000
    })
    # [END cursor_simple_end_at]

    return query_end_at


def snapshot_cursors():
    db = firestore.Client()
    # [START fs_start_at_snapshot_query_cursor]
    doc_ref = db.collection('cities').document('SF')

    snapshot = doc_ref.get()
    start_at_snapshot = db.collection(
        'cities').order_by('population').start_at(snapshot)
    # [END fs_start_at_snapshot_query_cursor]
    results = start_at_snapshot.limit(10).stream()
    for doc in results:
        print('{}'.format(doc.id))

    return results


def cursor_paginate():
    db = firestore.Client()
    # [START cursor_paginate]
    cities_ref = db.collection('cities')
    first_query = cities_ref.order_by('population').limit(3)

    # Get the last document from the results
    docs = first_query.stream()
    last_doc = list(docs)[-1]

    # Construct a new query starting at this document
    # Note: this will not have the desired effect if
    # multiple cities have the exact same population value
    last_pop = last_doc.to_dict()['population']

    next_query = (
        cities_ref
        .order_by('population')
        .start_after({
            'population': last_pop
        })
        .limit(3)
    )
    # Use the query for pagination
    # ...
    # [END cursor_paginate]

    return next_query


def listen_document():
    db = firestore.Client()
    # [START listen_document]

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print('Received document snapshot: {}'.format(doc.id))
        callback_done.set()

    doc_ref = db.collection('cities').document('SF')

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)
    # [END listen_document]

    # Creating document
    data = {
        'name': 'San Francisco',
        'state': 'CA',
        'country': 'USA',
        'capital': False,
        'population': 860000
    }
    doc_ref.set(data)
    # Wait for the callback.
    callback_done.wait(timeout=60)
    # [START detach_listener]
    # Terminate watch on a document
    doc_watch.unsubscribe()
    # [END detach_listener]


def listen_multiple():
    db = firestore.Client()
    # [START listen_multiple]

    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        print('Callback received query snapshot.')
        print('Current cities in California:')
        for doc in col_snapshot:
            print('{}'.format(doc.id))
        callback_done.set()

    col_query = db.collection('cities').where('state', '==', 'CA')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    # [END listen_multiple]
    # Creating document
    data = {
        'name': 'San Francisco',
        'state': 'CA',
        'country': 'USA',
        'capital': False,
        'population': 860000
    }
    db.collection('cities').document('SF').set(data)
    # Wait for the callback.
    callback_done.wait(timeout=60)
    query_watch.unsubscribe()


def listen_for_changes():
    db = firestore.Client()
    # [START listen_for_changes]

    # Create an Event for notifying main thread.
    delete_done = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        print('Callback received query snapshot.')
        print('Current cities in California: ')
        for change in changes:
            if change.type.name == 'ADDED':
                print('New city: {}'.format(change.document.id))
            elif change.type.name == 'MODIFIED':
                print('Modified city: {}'.format(change.document.id))
            elif change.type.name == 'REMOVED':
                print('Removed city: {}'.format(change.document.id))
                delete_done.set()

    col_query = db.collection('cities').where('state', '==', 'CA')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    # [END listen_for_changes]
    mtv_document = db.collection('cities').document('MTV')
    # Creating document
    mtv_document.set({
        'name': 'Mountain View',
        'state': 'CA',
        'country': 'USA',
        'capital': False,
        'population': 80000
    })
    sleep(1)

    # Modifying document
    mtv_document.update({
        'name': 'Mountain View',
        'state': 'CA',
        'country': 'USA',
        'capital': False,
        'population': 90000
    })
    sleep(1)

    # Delete document
    mtv_document.delete()

    # Wait for the callback captures the deletion.
    delete_done.wait(timeout=60)
    query_watch.unsubscribe()


def cursor_multiple_conditions():
    db = firestore.Client()
    # [START cursor_multiple_conditions]
    start_at_name = (
        db.collection('cities')
        .order_by('name')
        .order_by('state')
        .start_at({
            'name': 'Springfield'
        })
    )

    start_at_name_and_state = (
        db.collection('cities')
        .order_by('name')
        .order_by('state')
        .start_at({
            'name': 'Springfield',
            'state': 'Missouri'
        })
    )
    # [END cursor_multiple_conditions]

    return start_at_name, start_at_name_and_state


def delete_single_doc():
    db = firestore.Client()
    # [START delete_single_doc]
    db.collection('cities').document('DC').delete()
    # [END delete_single_doc]


def delete_field():
    db = firestore.Client()
    # [START delete_field]
    city_ref = db.collection('cities').document('BJ')
    city_ref.update({
        'capital': firestore.DELETE_FIELD
    })
    # [END delete_field]


def delete_full_collection():
    db = firestore.Client()

    # [START delete_full_collection]
    def delete_collection(coll_ref, batch_size):
        docs = coll_ref.limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            print('Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
            doc.reference.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return delete_collection(coll_ref, batch_size)
    # [END delete_full_collection]

    delete_collection(db.collection('cities'), 10)
    delete_collection(db.collection('data'), 10)
    delete_collection(db.collection('objects'), 10)
    delete_collection(db.collection('users'), 10)


def collection_group_query(db):
    # [START fs_collection_group_query_data_setup]
    cities = db.collection('cities')

    sf_landmarks = cities.document('SF').collection('landmarks')
    sf_landmarks.document().set({
        'name': 'Golden Gate Bridge',
        'type': 'bridge'
    })
    sf_landmarks.document().set({
        'name': 'Legion of Honor',
        'type': 'museum'
    })
    la_landmarks = cities.document('LA').collection('landmarks')
    la_landmarks.document().set({
        'name': 'Griffith Park',
        'type': 'park'
    })
    la_landmarks.document().set({
        'name': 'The Getty',
        'type': 'museum'
    })
    dc_landmarks = cities.document('DC').collection('landmarks')
    dc_landmarks.document().set({
        'name': 'Lincoln Memorial',
        'type': 'memorial'
    })
    dc_landmarks.document().set({
        'name': 'National Air and Space Museum',
        'type': 'museum'
    })
    tok_landmarks = cities.document('TOK').collection('landmarks')
    tok_landmarks.document().set({
        'name': 'Ueno Park',
        'type': 'park'
    })
    tok_landmarks.document().set({
        'name': 'National Museum of Nature and Science',
        'type': 'museum'
    })
    bj_landmarks = cities.document('BJ').collection('landmarks')
    bj_landmarks.document().set({
        'name': 'Jingshan Park',
        'type': 'park'
    })
    bj_landmarks.document().set({
        'name': 'Beijing Ancient Observatory',
        'type': 'museum'
    })
    # [END fs_collection_group_query_data_setup]

    # [START fs_collection_group_query]
    museums = db.collection_group('landmarks')\
        .where('type', '==', 'museum')
    docs = museums.stream()
    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))
    # [END fs_collection_group_query]
    return docs


def array_contains_any_queries(db):
    # [START fs_query_filter_array_contains_any]
    cities_ref = db.collection('cities')

    query = cities_ref.where(
        'regions', 'array_contains_any', ['west_coast', 'east_coast']
    )
    return query
    # [END fs_query_filter_array_contains_any]


def in_query_without_array(db):
    # [START fs_query_filter_in]
    cities_ref = db.collection('cities')

    query = cities_ref.where('country', 'in', ['USA', 'Japan'])
    return query
    # [END fs_query_filter_in]


def in_query_with_array(db):
    # [START fs_query_filter_in_with_array]
    cities_ref = db.collection('cities')

    query = cities_ref.where(
        'regions', 'in', [['west_coast'], ['east_coast']]
    )
    return query
    # [END fs_query_filter_in_with_array]


def update_document_increment(db):
    # [START fs_update_document_increment]
    washington_ref = db.collection('cities').document('DC')

    washington_ref.update({"population": firestore.Increment(50)})
    # [END fs_update_document_increment]