import atexit
import json
import os
from typing import Any, Callable
# from Crypto.Random import get_random_bytes
from Cryptodome.Cipher import AES

class Storage:
    def __init__(self, path='database.db', temp_path='_database-temp.db'):
        self.file_path = temp_path
        self._out_path = path

        self._file = open(temp_path, 'wb+')

        # copy over file content to temporary file
        with open(path, 'rb') as f:
            self._file.write(f.read())

        self._key = b'Sixteen byte key'
        self._cipher_bytes_start = 32

        print(f"Loaded db file ({self.size()}b)")
        
        self._nonce = self._file.read(16)
        self._tag = self._file.read(16)

        atexit.register(self.close)


    def size(self):
        """Get the file size

        :return: The size of the file in bytes (int)
        """
        self._file.seek(0, os.SEEK_END)
        return self._file.tell()

    def write(self, data_func: Callable[[Any], dict] or dict):
        """Write the the data to the loaded file"""

        # move cursor to first line
        self._file.seek(0)

        # serialize data
        serialized_data = None
        if isinstance(data_func, dict):
            serialized_data = json.dumps(data_func)
        else:
            serialized_data = json.dumps(data_func(self.read()))

        # encrypt
        cipher = AES.new(self._key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(bytes(serialized_data, 'utf-8'))

        self._file.seek(0)
        self._nonce = nonce
        self._tag = tag

        # first 16 bytes = nonce, following 16 bytes = tag, remaining bytes = ciphertext
        self._file.write(nonce)
        self._file.write(tag)
        self._file.write(ciphertext)

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
            cipher = AES.new(self._key, AES.MODE_EAX, nonce=self._nonce)

            self._file.seek(self._cipher_bytes_start)
            decrypted_data = cipher.decrypt_and_verify(self._file.read(), self._tag)

            # return file content
            return json.loads(decrypted_data.decode())
        
    def close(self):
        """Close file context"""
        self._file.close()
    