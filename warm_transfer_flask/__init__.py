from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from warm_transfer_flask.config import config_classes


db = SQLAlchemy()
app = Flask(__name__)


def prepare_app(environment='development', p_db=db):
    app.config.from_object(config_classes[environment])
    p_db.init_app(app)
    from .views import routes

    routes(app)
    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()


db.save = save_and_commit
