from asyncio.windows_events import NULL
from genericpath import exists
import os
from Crypto.Util.Padding import pad
from Cryptodome.Cipher import AES

class Encryption:
    def __init__(self, key, out_path="encrypted.bin"):
        self.out_path = out_path
        self.key = key
        
        self.create_new_cipher()

    def create_new_cipher(self):
        self.cipher = AES.new(self.key, AES.MODE_EAX)

    def encrypt(self, data: str):
        ciphertext, tag = self.cipher.encrypt_and_digest(bytes(data, 'utf8'))
        file_out = open(self.out_path, 'wb')

        [file_out.write(x) for x in (self.cipher.nonce, tag, ciphertext)]
        file_out.close()
    
    def decrypt(self):

        if (not exists(self.out_path)):
            return NULL

        file = open(self.out_path, 'rb')
        nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1)]

        self.cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        data = self.cipher.decrypt_and_verify(ciphertext, tag)
        
        file.close()
        return data.decode('utf8')
