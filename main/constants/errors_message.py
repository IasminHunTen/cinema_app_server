from . import CRED_MAX_LENGTH, CRED_MIN_LENGTH

CRED_OUT_OF_BOUNDS = f'The credential length must be between {CRED_MIN_LENGTH} and {CRED_MAX_LENGTH}'
PASSWORD_WITHOUT_LOWERCASE = 'The password must contain at least one lowercase'
PASSWORD_WITHOUT_UPPERCASE = 'The password must contain at least one uppercase'
PASSWORD_WITH_WHITESPACES = 'White spaces are not allowed in password'

SQL_DUPLICATE_ERR = '{} already in use'
