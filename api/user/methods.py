import jwt
from cryptography.fernet import Fernet
from collections import OrderedDict
from datetime import timedelta, datetime

from config import Config

from .constants import JWT_TOKEN_EXPIRE


fernet = Fernet(Config.SECRET_KEY)


def encrypt(string):
    if not isinstance(string, bytes):
        string = string.encode()
    return fernet.encrypt(string).decode()


def decrypt(token):
    if not isinstance(token, bytes):
        token = token.encode()
    return fernet.decrypt(token).decode()


def make_jwt_token(*args, **kwargs):
    now = datetime.now()
    expire = now + timedelta(seconds=JWT_TOKEN_EXPIRE)
    payload = OrderedDict(
        exp=expire,
        **kwargs
    )
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256').decode()


def decode_jwt_token(token):
    try:
        token_data = jwt.decode(token, Config.SECRET_KEY, options={'verify_exp': False})

    except Exception as error:
        print('Check token error', error.args)
        return None
    return token_data
