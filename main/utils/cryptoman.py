import os

from cryptography.fernet import Fernet

from . import SingletonMeta


class CryptoManager(metaclass=SingletonMeta):

    def __init__(self):
        self.__standard = 'utf-8'
        self.__crypto_man = Fernet(bytes(os.getenv('SECRET_KEY'), self.__standard))

    def encrypt_word(self, word):
        encrypted_word = self.__crypto_man.encrypt(bytes(word, self.__standard))
        return encrypted_word.decode(self.__standard)

    def decrypt_word(self, encrypted_word_string):
        return (self.__crypto_man.decrypt(
            bytes(encrypted_word_string, self.__standard))).decode(self.__standard)
