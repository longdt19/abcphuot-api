from flask_script import Manager, Server
from flask import current_app

from api.main import create_app
from api.extensions import db
from api.user import models as user_models
from api.product import models as product_models
from api.common import methods as common_methods

from seed import Seed


def create_my_app():
    return create_app()


manager = Manager(create_my_app)

# runs Flask development server locally at port 5000
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


# start a Python shell with contexts of the Flask application
@manager.shell
def make_shell_context():
    return dict(app=current_app,
                user_models=user_models,
                product_models=product_models,
                common_methods=common_methods,
                db=db, seed=Seed())


if __name__ == "__main__":
    manager.run()
