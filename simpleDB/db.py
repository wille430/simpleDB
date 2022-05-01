from pydoc import locate
from .storage import Storage
from simpleDB.Table import Table


class Database:
    def __init__(self):
        self.storage: Storage = Storage()
        self._tables: dict[str, Table] = {}

        self.init_tables()

    def __exit__(self):
        print("Saving database...")
        self.storage.write(lambda x : {**x, "tables": self.tables()})

    def _getitem(self, acc_value: dict, upd_value):
        return acc_value.setdefault(upd_value, {})

    def log(self, msg: str):
        print(msg)

    def save(self):
        serialized_tables = {}

        for key in self.tables():
            serialized_tables[key] = self.tables()[key].serialize()

        self.storage.write(lambda x : {**x, 'tables': serialized_tables})
        self.storage.save()

    def save_and_close(self):
        """Save data and close storage"""

        self.save()
        self.storage.close()
    
    def init_tables(self):
        """Reads storage and saves database tables in memory."""

        raw_data = self.storage.read()

        table_dict = raw_data.get('tables', {})

        for key in table_dict:
            table = table_dict[key]
            self._tables[key] = Table.fromJSON(self.storage, table)

    def tables(self) -> dict[str, Table]:
        """Get all tables in the database"""
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
        self.storage.write({})
        self._tables = {}

    def create_table(self, name: str, cols) -> Table:
        """Create a table if it doesn't already exist. Returns the table.

        :param name: The name of the table
        :param cols: A dict where the key is a string and the value a type
        """

        if not self.table(name):
            table = Table(self.storage, name, cols)
            self._tables[name] = table

        return self._tables[name]
