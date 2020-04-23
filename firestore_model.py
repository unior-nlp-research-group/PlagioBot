# from https://gitlab.com/jeremyfromearth/firestore-model

import key
import logging
import uuid
import functools
from dataclasses import dataclass, asdict

from google.cloud import firestore

import datetime

# --------------------------------------------
#
#  The main database client reference
#
# -------------------------------------------
db = firestore.Client()

def get_env_collection_name(c_name):
    if key.TEST:
        return '{}_{}'.format(key.VERSION, c_name)
    return c_name


def require_database(f, *args, **kwargs):
    """ Decorator for methods that access the database
      @raises Exception
      @return Decorator for methods that require database access
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if db is None:
            raise Exception('Database is not defined.')
        else:
            return f(*args, **kwargs)
    return wrapper

def transactional(f, *args, **kwargs):
    
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        
        @firestore.transactional 
        def update_in_transaction(transaction): 
            __self = args[0]
            logging.debug('Entering transactional function {} with args={} and kwargs={}'.format(f.__name__, args, kwargs))
            snapshot_copy_dict = __self.ref().get(transaction=transaction).to_dict()
            __self.copy_from_dict(snapshot_copy_dict)
            result =  f(*args, **kwargs)
            transaction.set(__self.ref(), asdict(__self))                        
            logging.debug('Exiting transactional function {} with args={} and kwargs={}'.format(f.__name__, args, kwargs))
            return result

        return update_in_transaction(db.transaction())

    return wrapper

# --------------------------------------------
#
#  Classes
#
# -------------------------------------------


class Query(object):
    """ A class representing a query on a collection
    """

    def __init__(self, cls, query_params):
        """
          @param cls The model class to run the query on
          @param A list of query params. The lists can be (key, value) or (key, operator, value)

          While possible, this method is not intended to be called by itself. The intended use 
          is from within the Model.query method. 

          Examples:
            # Get all users with first name Sonic
            q = User.query([('first_name', 'Sonic')])
            result = q.get()
            for r in result:
              # do something with r

            # Get 10 users created before a specific datetime
            query = User.query([('created', '<', 23409328408)])
            query.q.limit(10)
            result = query.get()
            for r in result:
              # do something with r

          References: 
            https://googleapis.github.io/google-cloud-python/latest/firestore/query.html 
        """
        self.cls = cls
        self.result = None
        env_collection_name = get_env_collection_name(cls.__name__)
        self.q = db.collection(env_collection_name)

        # parse the params
        for param in query_params:
            if len(param) == 2:
                self.q = self.q.where(param[0], '==', param[1])
            if len(param) == 3:
                self.q = self.q.where(*param)

    def get(self):
        """ Executes the query
          @return Generator object that yields hydrated instances of the class supplied __init__
        """
        self.result = self.q.get()
        for r in self.result:
            if hasattr(self.cls, 'from_dict'):
                yield self.cls.from_dict(r.to_dict())
            else:
                yield self.cls(**r.to_dict())


@dataclass
class Model:
    """ Base class for all other model classes
    """
    # --------------------------------------------
    #
    #  static
    #
    # -------------------------------------------

    @classmethod
    @require_database
    def delete_doc(cls, doc_id):
        try:
            env_collection_name = get_env_collection_name(cls.__name__)
            db.collection(env_collection_name).document(doc_id).delete()
        except Exception as e:
            logging.error(e)

    @classmethod
    @require_database
    def get(cls, doc_id):
        """ Get a single model instance
          @param cls The class of the instance calling make
          @param doc_id The id of the document to get
          @return A model instance of type class hydrated w/ data from the database 
        """
        try:
            env_collection_name = get_env_collection_name(cls.__name__)
            doc_ref = db.collection(env_collection_name).document(doc_id).get()
            return cls(**doc_ref.to_dict())
        except Exception as e:
            logging.error(e)

    @classmethod
    def make(cls, id=None, save=False, *args, **kwargs):
        """ Create a new instance of a model class
          @param cls The class of the instance calling make
          @param save A flag indicating the model should be saved immediately after creation
          @returns A new model instance of type cls

          Example:
            User.make(
                name = 'Sonic', 
                location = 'Earth', 
                save = True
              )
        """
        id = id if id else str(uuid.uuid4())
        created = datetime.datetime.utcnow()
        m = cls(id, created, created, *args, **kwargs)
        if save:
            m.save()
        return m

    @classmethod
    @require_database
    def query(cls, q=()):
        """ Get a handle to a query object (see Query helper class above)
          @param cls The class of the instance calling make
          @param q A list of query key/value or key/operator/value pairs (
        """
        return Query(cls, q)

    # --------------------------------------------
    #
    #  instance
    #
    # -------------------------------------------    

    id: str
    created: datetime.datetime
    modified: datetime.datetime

    @require_database
    def ref(self):
        env_collection_name = get_env_collection_name(self.__class__.__name__)
        
        return db.collection(env_collection_name).document(self.id)


    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    @require_database
    def delete(self):
        """ Removes this model from Cloud Datastore

          @raises Exception indicating that deletion failed
        """
        try:
            self.ref().delete()
            return True
        except Exception as e:
            logging.error(e)

    @require_database
    def save(self):
        """ Saves this model to Cloud Firestore """
        return self.set(asdict(self))

    def copy_from_dict(self, kvs):
        """ Set values on this model
          @param kvs A dictionary containing key value pairs to set on this model. 
          Unrecognized keys are ignored
        """
        for k, v in kvs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @require_database
    def set(self, kvs):
        self.copy_from_dict(kvs)
        self.modified = datetime.datetime.utcnow()
        self.ref().set(asdict(self))

    @require_database
    def update(self, kvs):
        self.modified = kvs['modified'] = datetime.datetime.utcnow()
        self.copy_from_dict(kvs)
        self.ref().update(kvs)

    def to_dict(self):
        """ A convenience function that converts this model into a dictionary representation

          @return Dictionary of key value pairs representing this model
        """
        return asdict(self)
