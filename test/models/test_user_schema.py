import unittest
from marshmallow import ValidationError


from main.models import UserPost
from main.constants import CRED_MIN_LENGTH, CRED_MAX_LENGTH, CRED_OUT_OF_BOUNDS, \
    PASSWORD_WITHOUT_UPPERCASE, PASSWORD_WITHOUT_LOWERCASE, PASSWORD_WITH_WHITESPACES


class TestUserPostSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = UserPost()
        cls.payload = {
            'username': 'ValidUsername',
            'email': 'valid@email.com',
            'password': 'ValidPassword'
        }

    def tearDown(self) -> None:
        self.payload.update({
            'username': 'ValidUsername',
            'email': 'valid@email.com',
            'password': 'ValidPassword'
        })

    def abstract_test(self, key, value, error_message):
        self.payload[key] = value

        try:
            self.schema.load(self.payload)
        except ValidationError as ve:
            assert error_message in ve.messages[key][0]
            return
        assert False

    def test_valid_schema(self):
        try:
            self.schema.load(self.payload)
        except ValidationError as ve:
            assert False
        assert True

    def test_try_without_username(self):
        self.payload.pop('username')
        try:
            self.schema.load(self.payload)
        except ValidationError as ve:
            assert 'required' in ve.messages['username'][0]
            return
        assert False

    def test_try_without_password(self):
        self.payload.pop('password')
        try:
            self.schema.load(self.payload)
        except ValidationError as ve:
            assert 'required' in ve.messages['password'][0]
            return
        assert False

    def test_try_with_a_short_username(self):
        self.abstract_test('username', 'a'*(CRED_MIN_LENGTH - 1), CRED_OUT_OF_BOUNDS)

    def test_try_with_a_long_username(self):
        self.abstract_test('username', 'a'*(CRED_MAX_LENGTH + 1), CRED_OUT_OF_BOUNDS)

    def test_try_with_a_long_email(self):
        zone = (CRED_MAX_LENGTH + 1 - len('.com@')) // 2
        test_email = f"{'e'*zone}@{'d'*zone}.com"
        self.abstract_test('email', test_email, 'maximum length')

    def test_try_with_a_bad_email(self):
        self.abstract_test('email', 'not_an_email', 'Not a valid email address')

    def test_try_with_a_short_password(self):
        self.abstract_test('password', 'a' * (CRED_MIN_LENGTH - 1), CRED_OUT_OF_BOUNDS)

    def test_try_with_a_long_password(self):
        self.abstract_test('password', 'a' * (CRED_MAX_LENGTH + 1), CRED_OUT_OF_BOUNDS)

    def test_try_with_password_with_no_uppercase(self):
        self.abstract_test('password', 'a'*CRED_MIN_LENGTH, PASSWORD_WITHOUT_UPPERCASE)

    def test_try_with_password_with_no_lowercase(self):
        self.abstract_test('password', 'A'*CRED_MAX_LENGTH, PASSWORD_WITHOUT_LOWERCASE)

    def test_try_with_password_containing_white_spaces(self):
        self.abstract_test('password', 'A password white spaces', PASSWORD_WITH_WHITESPACES)
