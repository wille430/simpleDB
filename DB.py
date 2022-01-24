import os
import json

class Database:
    def __init__(self, path):
        self.path = path
        self._load()

    def _load(self):
        self.data = json.load(open(self.path, 'rw'))

    # retrieve value in dict from nested keys
    def get(self, *keys):
        retrieved_data = None

        # find nested values in data dict
        for key in keys:
            if retrieved_data:
                retrieved_data = retrieved_data[key]
            else:
                retrieved_data = self.data[key]


    def delete(self, *keys):
        nested_data = self.data
        for key in keys:
            nested_data = nested_data[key]
        
        del nested_data

    # def set(self, value, *keys):
        # todo: add value to nested key
