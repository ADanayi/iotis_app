# In the name of Allah

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode
from base64 import b64decode, urlsafe_b64decode
from threading import Lock
import pickle
import json
import typing as T


class Cipher:
    def __init__(self, data_dict: T.Optional[dict] = None):
        self.__lock = Lock()
        self.__generated = False
        if data_dict is not None:
            self.__tag = data_dict['tag']
            if 'private_key' in data_dict:
                # print(f'creating cipher@{self.__tag} (private)')
                self.__key = RSA.import_key(data_dict['private_key'], data_dict['public_key'])#, data_dict['private_key'])
            else:
                # print(f'creating cipher@{self.__tag} (public)')
                self.__key = RSA.import_key(data_dict['public_key'])#, data_dict['private_key'])
            self.__generated = True
        else:
            self.__tag = None
            self.__key = None

    def generate_key(self, key_length: int, tag: str = ''):
        with self.__lock:
            if self.__generated:
                raise Exception('Already generated')
            assert key_length in [1024, 2048, 4096]
            self.__tag = tag
            rng = Random().read
            self.__key = RSA.generate(key_length, rng)
            self.__generated = True
            return
    
    @property
    def has_private(self) -> bool:
        return self.key.has_private()

    @property
    def generated(self) -> bool:
        return self.__generated

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def key(self) -> RsaKey:
        if self.__key is None:
            raise Exception('Please first call the generate_key function')
        return self.__key

    def encrypt(self, data: str, perform_b64: bool = False):
        if perform_b64:
            plaintext = b64encode(data.encode())
        else:
            plaintext = data.encode()
        rsa_encryption_cipher = PKCS1_v1_5.new(self.key)
        ciphertext = rsa_encryption_cipher.encrypt(plaintext)
        return b64encode(ciphertext).decode()

    def decrypt(self, data: str, perform_b64: bool = False):
        if not self.key.has_private():
            raise Exception('This cipher is only used for encryption')
        rsa_decryption_cipher = PKCS1_v1_5.new(self.key)
        # ciphertext = b64decode(data.encode())
        ciphertext = urlsafe_b64decode(data.encode())
        plaintext = rsa_decryption_cipher.decrypt(ciphertext, 16)
        if perform_b64:
            return b64decode(plaintext).decode()
        else:
            return plaintext.decode()

    @property
    def public_key(self) -> bytes:
        return self.key.public_key().export_key()

    def write_public_key(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.public_key)

    @property
    def private_key(self) -> bytes:
        if not self.key.has_private():
            raise Exception('This cipher is only used for encryption')
        return self.key.export_key()

    @property
    def __dict__(self) -> dict:
        k = self.key
        if self.has_private:
            return {
                'public_key': self.public_key,
                'private_key': self.private_key,
                'tag': self.tag
            }
        else:
            return {
                'public_key': self.public_key,
                'tag': self.tag
            }

    def write(self, path: str, format: str = 'json'):
        """type can be either 'json' or 'bin' (pickled)"""
        if not self.__generated:
            raise Exception('Can not write a non-generated key')
            if format == 'json':
                with open(path, 'w') as file:
                    json.dump(vars(self), file, indent='  ', ensure_ascii=False)
            elif format == 'bin':
                with open(path, 'wb') as file:
                    pickle.dump(vars(self), file)
            else:
                raise Exception('Right now only bin and json are accepted')
