from api.common.base_errors import Base


class InvalidFileExt(Base):
    status_code = 499
    message = 'Invalid file type!'
