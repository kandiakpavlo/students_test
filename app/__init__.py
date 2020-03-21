from flask import Flask

from .config import Config
from .database import db
from .veiws import students_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    app.register_blueprint(students_api)
    return app