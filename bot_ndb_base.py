# -*- coding: utf-8 -*-
# https://pypi.org/project/google-cloud-datastore/
# https://googleapis.github.io/google-cloud-python/latest/datastore/entities.html

import logging
import datetime
from google.cloud import datastore
CLIENT = datastore.Client()

class NDB_Base(object):    

    def __getattr__(self, attr):
        if attr == 'key':
            return self.entry.key
        return self.entry.get(attr,None)
    
    def __setattr__(self, key, value):
        if key == 'entry':
            super().__setattr__(key, value)
        else:
            self.entry[key] = value

    def __eq__(self, other):
        if isinstance(other, NDB_Base):
            return self.key == other.key
        else:
            return False

    def put(self):
        self.last_update=datetime.datetime.now()
        CLIENT.put(self.entry)
        # from bot_ndb_user import NDB_User
        # if type(self)==NDB_User:
        #     logging.debug('In put with user={} key={}'.format(self.entry, self.key))
        #     from bot_telegram import send_message
        #     msg = "updated entry: {}".format(self.entry)
        #     send_message(self, msg, markdown=False)
        

    def delete(self):
        CLIENT.delete(self.entry.key)