import yaml
import os


class Base(object):
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    PROPAGATE_EXCEPTIONS = True

    MONGODB_CONNECT = False


class Default(Base):
    DEBUG = True

    APP_NAME = 'your_app_name'

    SECRET_KEY = 'this is a very secret key'

    CAS_KEY = 'cas key'

    MONGODB_HOST = 'mongodb://127.0.0.1:27017/db_name'

    DOMAIN = 'http://127.0.0.1:5000'

    SOCKET_MSG_QUEUE = 'redis://127.0.0.1:6379/0'

    CELERY_BROKER = 'redis://127.0.0.1:6379/1'
    CELERY_BACKEND = 'redis://127.0.0.1:6379/2'



def get_config():
    config_file_path = 'app.yaml'
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as stream:
            data = yaml.load(stream)
        result = type('Config', (Base,), data)
    else:
        result = Default

    return result


Config = get_config()
