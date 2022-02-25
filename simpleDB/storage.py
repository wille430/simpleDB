import json
import os
from Crypto.Random import get_random_bytes
from simpleDB.encryption import Encryption


class Storage:
    def __init__(self, path='database.db', encrypt=False, encrypted_path='database.bin'):
        self.file_path = path

        if (encrypt):

            self.encrypted = True

            key = get_random_bytes(16)
            self.encryption = Encryption(key, encrypted_path)
            decrypted_data = self.encryption.decrypt()

            self._file = open(path, 'w+')
            self.write(decrypted_data)

        else:
            self.encrypted = False
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

        if (self.encrypted):
            print('Encrypting data...')
            self.encryption.encrypt(json.dumps(self.read()))

            print('Closing storage...')
            self._file.close()

            print(f'Removing decrypted file {self.file_path}...')
            os.remove(self.file_path)
        else:
            print('Closing storage...')
            self._file.close()



        print('Storage successfully closed.')
