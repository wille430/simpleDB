import os
import json
from functools import reduce
from simpleDB.utils import generate_primary_key
from .storage import Storage
from simpleDB.Table import Table


class Database:
    def __init__(self):
        self.storage: Storage = Storage()
        self._tables: dict[str, Table] = {}

    def __exit__(self):
        print("Saving database...")
        self.storage.write(self.tables())

    def _getitem(self, acc_value: dict, upd_value):
        return acc_value.setdefault(upd_value, {})

    def log(self, msg: str):
        print(msg)

    def tables(self) -> dict:
        self._tables = self.storage.read()

        return self._tables

    def table(self, table_name) -> Table:
        # Find table by name

        # Check if it exists in instance
        if table_name in self._tables:
            return self._tables[table_name]
        else:
            return None

    def clear(self):
        # FIXME: clear storage
        self._tables = {}
        self.storage.write({})

    def create_table(self, name: str, cols) -> Table:
        """
        Create a table if it doesn't already exist.
        Returns the table.

        :param name: the name of the table
        :param cols: a dict where the key is a string and the value a type
        """
        if not self.table(name):
            table = Table(self.storage, name, cols)
            self._tables[name] = table

        return self._tables[name]
