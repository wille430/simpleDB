from .storage import Storage
from simpleDB.Table import Table


class Database:
    def __init__(self, encrypt=False):
        self.storage: Storage = Storage(encrypt=encrypt)
        self._tables: dict[str, Table] = {}

    def __exit__(self):
        print("Saving database...")
        self.storage.write(self.tables())

    def _getitem(self, acc_value: dict, upd_value):
        return acc_value.setdefault(upd_value, {})

    def log(self, msg: str):
        print(msg)

    def close(self):
        self.storage.write(self._tables)
        self.storage.close()

    def tables(self) -> dict[str, Table]:
        """Get all tables in the database"""
        self._tables = self.storage.read()

        return self._tables

    def table(self, table_name: str) -> Table:
        """Find a table by name"""

        # Check if it exists in instance
        if table_name in self._tables:
            return self._tables[table_name]
        else:
            return None

    def clear(self):
        """Resets the entire database"""
        self._tables = {}
        self.storage.write({})

    def create_table(self, name: str, cols) -> Table:
        """Create a table if it doesn't already exist. Returns the table.

        :param name: The name of the table
        :param cols: A dict where the key is a string and the value a type
        """
        if not self.table(name):
            table = Table(self.storage, name, cols)
            self._tables[name] = table

        return self._tables[name]
