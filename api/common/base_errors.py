from bson import json_util


class Base(Exception):
    status_code = 500
    message = 'An unknown error happened.'

    def __init__(self, message=None, payload=None):
        if message:
            self.message = message
        self.payload = payload
        super().__init__(self.message)

    def get_message(self):
        data = {
            'message': self.message
        }
        if self.payload:
            data['payload'] = str(self.payload)
        return data

    def __str__(self):
        return json_util.dumps(self.get_message())


class InvalidRequestParams(Base):
    status_code = 400
    message = 'Invalid request params.'


class PermissionError(Base):
    status_code = 403
    message = 'Permission error!'


class ServerError(Base):
    status_code = 500
    message = 'Server error!'
