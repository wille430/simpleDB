
import json


class Table:
    def __init__(self, name, cols: dict, rows = []):
        self.name = name
        self.columns = cols.keys()
        self.columnTypes = cols.values()
        self.rows = []

        for row in rows:
            self.add_row(row)

    def _validate_row(self, row):
        for index, col in row:
            if type(col) is not self.columnTypes[index]:
                raise TypeError(
                    f'Row value on index {index} is of invalid type. Value must be type of {self.columnTypes[index]}')

    def serialize(self):
        return json.dump(self.__init__)

    def add_row(self, row):
        # validate types in row
        self._validate_row(row)

        # add row to table
        self.rows.append(row)