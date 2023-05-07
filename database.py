from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql.base import PGDialect


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    db.create_all(app=app)
