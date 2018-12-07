from api.common.base_logics import BaseLogic

from .methods import decrypt, make_jwt_token
from .models import User
from .errors import *


class UserBL(BaseLogic):
    def authenticate(self, email, password):
        user = User.objects(email=email).first()
        if not user:
            raise InvalidCredentials

        if password != decrypt(user.password):
            raise InvalidCredentials

        access_token = make_jwt_token(id=str(user.id))
        return dict(access_token=access_token, auth_user=user.output())


user_bl = UserBL()
