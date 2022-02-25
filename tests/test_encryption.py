import os
from random import choice, randrange
import string
import unittest
from simpleDB.encryption import Encryption
from Crypto.Random import get_random_bytes

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.key = get_random_bytes(16)
        self.encryption = Encryption(self.key)
        self.data = ''.join(choice(string.ascii_letters) for i in range(0, randrange(10*4, 10**6)))

    def tearDown(self) -> None:
        os.remove(self.encryption.out_path)
    
    def test_encryption(self):
        self.encryption.encrypt(self.data)
        out_file = open(self.encryption.out_path, 'rb')

        out_data = b''.join(i for i in out_file.readlines())

        out_file.close()
        self.assertNotEqual(self.data, out_data)

    def test_decrypt(self):
        self.encryption.encrypt(self.data)
        decrypted_data = self.encryption.decrypt()

        self.assertEqual(self.data, decrypted_data)

if __name__ == '__main__':
    unittest.main()