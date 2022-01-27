import os
import json
from functools import reduce
import operator
import uuid

from simpleDB.Table import Table


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
            self.__dict__ = json.load(open(self.path, 'r+'))
        except:
            # pass empty dict
            self.log('Creating a new database...')
            self.tables = {}

    def _getitem(self, acc_value: dict, upd_value):
        return acc_value.setdefault(upd_value, {})

    def log(self, msg: str):
        print(msg)

    def generate_primary_key(self):
        return uuid.uuid4().hex

    def save(self):
        with open(self.path, 'w') as f:
            # TODO: serialize each table
            json.dump(self.__dict__, f)

    # create table
    def create_table(self, table: Table):
        # check if table with name already exists
        if self.tables.get(table.name):
            raise OSError("Table already exists")
        
        self.tables[table.name] = table

    def add_row(self, table_name, row):
        self.tables[table_name].add_row(row)
