from asyncio.windows_events import NULL
from genericpath import exists
import os
from Crypto.Util.Padding import pad
from Cryptodome.Cipher import AES

class Encryption:
    def __init__(self, key, out_path="encrypted.bin"):
        self.out_path = out_path
        self.key = key

    def encrypt(self, data: str):
        print("Encrypting...")
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(data, 'utf8'))
        file_out = open(self.out_path, 'wb')

        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()
        print("DONE")
    
    def decrypt(self):
        if (not exists(self.out_path)):
            print("No encrypted file found. Returning empty data.")
            return {}

        print("Decrypting", self.out_path)
        file = open(self.out_path, 'rb')
        nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1)]

        cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        
        print("DONE")
        return data.decode('utf8')
