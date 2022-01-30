import json
import os


class Storage:
    def __init__(self, path='database.db'):
        self._file = open(path, "w+")

        print(f"Loaded db file ({self.size()}b)")

    def size(self):
        """Get the file size

        :return: The size of the file in bytes (int)
        """
        self._file.seek(0, os.SEEK_END)
        return self._file.tell()

    def write(self, data: dict):
        """Write the the data to the loaded file"""

        # move cursor to first line
        self._file.seek(0)

        # serialize data
        serialized_data = json.dumps(data)

        # write to file
        self._file.write(serialized_data)
        self._file.truncate()

        print(f"Changes written to file ({self.size()}b)")

    def read(self):
        """Read the loaded file"""

        # move cursor to first line
        self._file.seek(0)

        # if file is empty return empty
        if not self.size():
            return {}
        else:
            self._file.seek(0)
            # return file content
            return json.load(self._file)
    
    def close(self):
        """Close file context"""
        self._file.close()
