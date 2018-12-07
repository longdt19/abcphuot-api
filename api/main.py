from flask import Flask, request, abort, g, make_response, jsonify
from api.extensions import api, db, cors
from api.user.models import User
from api.user.methods import decode_jwt_token
from config import Config

from .endpoints import ENDPOINTS

__all__ = ['create_app']


def create_app(app_name=None):
    """
    create app with given config
    :param config:
    :param app_name:
    :param blueprints:
    :return: socketio, app
    """

    if not app_name:
        app_name = Config.APP_NAME

    app = Flask(app_name)

    app.config.from_object(Config)

    configure_hook(app)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)
    return app


def configure_extensions(app):
    # database
    db.init_app(app)

    # cors
    cors.init_app(app)

    # flask_restful api
    api.app = app
    for endpoint, data in ENDPOINTS.items():
        api.add_resource(data['resource'], endpoint)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_logging(app):
    # app.logger.addHandler(file_handler)
    # app.logger.debug()
    pass


def configure_hook(app):
    """configure_hook regist hook in app like before_request, after_request
        :param app:
    """

    @app.before_request
    def before_request():
        """ This function runs when app receives a request before endpoint. """

        auth_data = request.headers.get('Authorization', None)
        g.user = get_auth_user(auth_data=auth_data)

        if is_required_auth(endpoint=request.path, method=request.method) and not g.user:
            return abort(401)


def configure_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_error(error):
        if hasattr(error, 'status_code'):
            response = make_response(str(error), error.status_code)

        elif hasattr(error, 'code'):
            response = make_response(str(error), error.code)

        else:
            if app.debug:
                raise error
            response = make_response(
                jsonify({'message': 'An unknown error happened - %s' % error}), 500)

        return response


def is_required_auth(endpoint, method):
    # don't require token for options method
    if method == 'OPTIONS':
        return False

    # if request endpoint is invalid
    if endpoint not in ENDPOINTS.keys():
        return False

    # if request endpoint is valid, then get its required auth methods
    required_auth_methods = ENDPOINTS[endpoint].get('required_auth_methods')

    if not required_auth_methods:
        return False

    if method in required_auth_methods:
        return True

    return False


def get_auth_user(auth_data=None):
    if not auth_data:
        return None

    try:
        bearer, access_token = auth_data.split(' ')
    except ValueError:
        return None

    if bearer != 'Bearer' or not access_token:
        return None

    token_data = decode_jwt_token(token=access_token)
    if not token_data:
        return None

    return User.objects(id=token_data.get('id')).first()
