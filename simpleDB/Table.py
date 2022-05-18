from email.policy import default
import json
from pydoc import locate
from time import process_time_ns
from typing import Dict, Mapping
from numpy import result_type
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
        self.rows = self._read_table()

    def serialize_columns(self, data: Dict[str, type]):
        return data.__name__ or data

    def _validate_row(self, row: Row):
        for key, value in row.items():
            if type(value) is not self._columns.get(key):
                raise TypeError(
                    f'Column {key} in row is of invalid type. Value must be type of {self._columns.get(key)}')

    def name(self):
        return self._name

    def insert(self, row: Row):
        # validate row
        self._validate_row(row)
        row_id = generate_primary_key()

        # add row
        self.rows[row_id] = row

        # return id
        return row_id

    def find(self, row_id: str) -> Row:
        """Get a row by id"""
        return self.rows.get(row_id)

    def _read_table(self):
        """Get table from database"""

        tables = self._storage.read().get('tables', {})

        if tables is None or len(tables.keys()) == 0:
            return {}
        else:
            table_obj = tables[self._name]

            # Omit table meta data
            return {x: table_obj[x] for x in table_obj if x[0] != '_'}

    def delete(self, row_id):
        """Delete a row inside the table"""
        self.rows.pop(row_id)

    def query(self, fieldName, operation, value, limit=-1) -> Query:

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

        for row_key in self.rows:
            row = self.rows[row_key]
            if matches_operation(row.setdefault(fieldName, None), value):
                result_count += 1
                result.append(row)

            if limit != -1 and result_count > limit:
                # exit if limit is reached
                break

        return Query(result)

    def serialize(self) -> dict:
        serialized = {
            '_name': self._name,
            '_columns': json.loads(json.dumps(self._columns, default=self.serialize_columns)),
            **self.rows
        }
        return serialized

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def fromJSON(storage: Storage, table_obj):
        parsed_columns = {}

        for key in table_obj['_columns']:
            parsed_columns[key] = locate(table_obj['_columns'].get(key))

        table = Table(storage, table_obj['_name'], parsed_columns)

        # Remove keys that start with _ to get rows with data
        rows = {x: table_obj[x] for x in table_obj if x[0] != '_'}

        # and add rows to table
        # TODO: keep row ID
        for row in rows.values():
            table.insert(row)

        return table
