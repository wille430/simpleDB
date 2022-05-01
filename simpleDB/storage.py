import atexit
import json
import os
from pathlib import Path
from typing import Any, Callable
# from Crypto.Random import get_random_bytes
from Cryptodome.Cipher import AES

class Storage:
    def __init__(self, path='database.db', temp_path='_database-temp.db'):
        self.temp_path = temp_path
        self.out_path = path

        self._file = open(temp_path, 'wb+')
        self._key = b'Sixteen byte key'
        self._cipher_bytes_start = 32

        if Path(path).exists():
            out_file = open(path, 'rb')
        else:
            out_file = open(path, 'wb+')

        # if database file is empty, then start with empty data
        if os.path.getsize(path) > 0:
            print("Loading existing database file...")
            # copy over file content to temporary file
            self._file.write(out_file.read())

            print(f"Loaded db file ({self.size()}b)")
            
            self._file.seek(0)
            self._nonce = self._file.read(16)
            self._tag = self._file.read(16)
        else:
            print("Creating new db...")
            self.write({})

        out_file.close()

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
            decrypted_data: bytes = cipher.decrypt_and_verify(self._file.read(), self._tag)

            # return file content
            return json.loads(decrypted_data.decode())
        
    def close(self):
        """Close file context"""

        if not self._file.closed:
            self._file.close()

            try:
                if os.path.exists(self.temp_path):
                    os.remove(self.temp_path)
            except:
                return
        
    def save(self):
        self._file.seek(0)

        with open(self.out_path, 'wb') as f:
            f.write(self._file.read())