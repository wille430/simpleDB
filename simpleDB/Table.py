from typing import Callable, Dict, Mapping
from simpleDB.query import Query
from simpleDB.storage import Storage
from simpleDB.utils import generate_primary_key


class Row(Dict[str, any]):
    def __init__(self, value: Mapping[str, any]):
        super().__init__(value)


class Table:
    def __init__(
        self,
        storage: Storage,
        name: str,
        columns: Dict[str, type]
    ):
        self._storage = storage
        self._name = name
        self._columns = columns

    def _validate_row(self, row: Row):
        for key, value in row.items():
            if type(value) is not self._columns.get(key):
                raise TypeError(
                    f'Column {key} in row is of invalid type. Value must be type of {self._columns.get(key)}')

    def name(self):
        return self._name

    def rows(self) -> Dict[str, Row]:
        """Get all rows in the table

        :returns: A list with all rows in table
        """

        table = self._read_table()
        return table

    def insert(self, row: Row):
        # validate row
        self._validate_row(row)
        row_id = generate_primary_key()

        # update callback
        def update_table(table):
            table[row_id] = dict(row)

        # add row
        self._update_table(update_table)

        # return id
        return row_id

    def _update_table(self, callback: Callable):
        # Get all tables in storage
        tables = self._storage.read()
        table = tables.setdefault(self._name, {})

        # call callback
        callback(table)

        # Write storage
        self._storage.write(tables)

    def find(self, row_id: str) -> Row:
        """Get a row by id"""
        return self.rows().get(row_id)

    def _read_table(self):
        """Get table from database"""

        tables = self._storage.read()

        if tables is None:
            return {}
        else:
            return tables[self._name]

    def delete(self, row_id):
        """Delete a row inside the table"""

        def remove_row(table):
            try:
                del table[row_id]
            except:
                pass

            return table

        self._update_table(remove_row)

    def query(self, fieldName, operation, value, limit = -1) -> Query:

        result = []
        result_count = 0

        def matches_operation(val1, val2):

            if val1 == None and val2 != None:
                return False

            match operation:
                case '==':
                    return val1 == val2
                case '>=':
                    return val1 >= val2
                case '<=':
                    return val1 <= val2
                case '!=':
                    return val1 != val2
                case '>':
                    return val1 > val2
                case '<':
                    return val1 < val2

        for row in self.rows().values():
            if matches_operation(row.setdefault(fieldName, None), value):
                result_count += 1
                result.append(row)

            if limit != -1 and result_count > limit:
                # exit if limit is reached
                break


        return Query(result)
