from flask import Flask
from .database import db
from .config import Config
from .views import st, bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    app.register_blueprint(st)
    app.register_blueprint(bp)

    return app