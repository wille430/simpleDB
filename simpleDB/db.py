import os
import json
from functools import reduce
import operator
import uuid


class Database:
    def __init__(self, path, is_absolute_path=False):
        if is_absolute_path:
            self.path = path
        else:
            self.path = os.path.join(os.path.curdir, path)

        self._load()

    def _load(self):
        try:
            # try to open file and convert to json
            self.data = json.load(open(self.path, 'r+'))
        except:
            # pass empty dict
            self.log('Creating a new database...')
            self.data = {}

    def _getitem(self, acc_value: dict, upd_value):
        return acc_value.setdefault(upd_value, {})

    def log(self, msg: str):
        print(msg)

    def generate_primary_key(self):
        return uuid.uuid4().hex

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    # users/userId ==> ['users', 'userId']
    def path_to_keys(self, path: str):
        return path.split('/')

    # retrieve value in dict from nested keys
    def find(self, path):
        keys = self.path_to_keys(path)

        # find nested values in data dict
        retrieved_data = reduce(operator.getitem, keys, self.data)

        return retrieved_data

    def delete(self, path):
        keys = self.path_to_keys(path)

        # delete nested key
        self.data = reduce(operator.delitem, keys, self.data)

    def set(self, value, path):
        keys = self.path_to_keys(path)

        # add value to nested dict
        reduce(self._getitem, keys[0:-1], self.data)[keys[-1]] = value

    def append(self, value, path):
        # create new primary key
        uniqueId = self.generate_primary_key()

        # add value to primary key
        self.set(value, f'{path}/{uniqueId}')
