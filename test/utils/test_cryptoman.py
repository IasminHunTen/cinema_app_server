import unittest

from main.utils.cryptoman import CryptoManager


class TestCryptoManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.crypto_man = CryptoManager()
        cls.word = 'word_to_be_encrypted'

    def test_crypto_man_is_singleton(self):
        assert self.crypto_man == CryptoManager()

    def test_crypto_flow(self):
        assert self.crypto_man.decrypt_word(
            self.crypto_man.encrypt_word(self.word)
        ) == self.word






