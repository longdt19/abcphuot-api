from api.common.base_errors import Base


class InvalidCredentials(Base):
    status_code = 499
    message = 'Invalid credentials!'
