import os
import config

DATE_FORMAT = '%d/%m/%Y'

JWT_TOKEN_EXPIRE = 7200  # second

APP_ROOT_DIR = os.path.dirname(config.__file__)

PAGINATION = {
    'page': 1,
    'per_page': 50
}

STRING_LENGTH = {
    'EX_SHORT': 30,
    'SHORT': 50,
    'MEDIUM': 200,
    'LONG': 500,
    'EX_LONG': 1000,
    'LARGE': 3000,
    'EX_LARGE': 10000
}