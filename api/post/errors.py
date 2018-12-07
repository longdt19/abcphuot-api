from api.common.base_errors import Base


class NameAlreadyExists(Base):
    status_code = 499
    message = 'Name already exists!'
