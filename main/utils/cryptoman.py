from . import SingletonMeta
from . import get_secret_key
from cryptography.fernet import Fernet


class CryptoManager(metaclass=SingletonMeta):

    def __init__(self):
        self.__crypto_man = Fernet(get_secret_key())
        self.__standard = 'utf-8'

    def encrypt_word(self, word):
        encrypted_word = self.__crypto_man.encrypt(bytes(word, self.__standard))
        return encrypted_word.decode(self.__standard)

    def decrypt_word(self, encrypted_word_string):
        return (self.__crypto_man.decrypt(
            bytes(encrypted_word_string, self.__standard))).decode(self.__standard)


