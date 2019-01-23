# -*- coding: utf-8 -*-
# https://pypi.org/project/google-cloud-datastore/
# https://googleapis.github.io/google-cloud-python/latest/datastore/entities.html


import logging
import datetime

from google.api_core import exceptions
from google.api_core import retry

# retry_commit = retry.Retry(
#     predicate=retry.if_exception_type(exceptions.ServiceUnavailable),
#     deadline=60)


from google.cloud import datastore
CLIENT = datastore.Client()

class NDB_Base(object):

    def __init__(self, entry=None, key=None):
        assert entry or key
        if entry:
            self.entry = entry            
        if key:
            self.entry = CLIENT.get(key)

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

    @retry.Retry(predicate=retry.if_exception_type(exceptions.ServiceUnavailable))
    def put(self):
        self.last_update=datetime.datetime.now()
        CLIENT.put(self.entry)

    def delete(self):
        CLIENT.delete(self.entry.key)

def transactional(func):
    import google.cloud.exceptions
    from bot_telegram import report_master
    def transactional_wrapper(*args, **kwargs):
        for _ in range(5):
            try:
                with CLIENT.transaction():
                    args[0].refresh() #args[0] is self
                    return func(*args, **kwargs)
            except google.cloud.exceptions.Conflict:
                continue
        else:
            report_string = '❗️ Concurrent transaction conflict'
            report_master(report_string)
            logging.error(report_string)
    return transactional_wrapper
