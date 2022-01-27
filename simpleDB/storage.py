import json

from importlib_metadata import os


class Storage:
    def __init__(self, path='database.db'):
        self._file = open(path, "r+")

        print(f"Loaded db file ({self.size()}b)")

    def size(self):
        self._file.seek(0, os.SEEK_END)
        return self._file.tell()

    def write(self, data: dict):
        # move cursor to first line
        self._file.seek(0)

        # serialize data
        serialized_data = json.dumps(data)

        # write to file
        self._file.write(serialized_data)

        print(f"Changes written to file ({self.size()}b)")

    def read(self):
        # move cursor to first line
        self._file.seek(0)
        
        # if file is empty return empty
        if not self.size():
            return {}
        else:
            self._file.seek(0)
            # return file content
            return json.load(self._file)
