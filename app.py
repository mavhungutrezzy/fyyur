import logging
import os
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment

import database
from routes import route_blueprint
from utils.caching import cache


def create_app():
    app = Flask(__name__, static_folder="static")
    moment = Moment(app)
    app.config.from_object("config.DevelopmentConfig")
    database.init_app(app)
    migrate = Migrate(app, database.db)
    cache.init_app(
        app, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}
    )
    app.register_blueprint(route_blueprint)

    def format_datetime(value, time_format="medium"):
        date = dateutil.parser.parse(value)
        if time_format == "full":
            time_format = "EEEE MMMM, d, y 'at' h:mma"
        elif time_format == "medium":
            time_format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, time_format, locale="en")

    app.jinja_env.filters["datetime"] = format_datetime

    if app.config["ENV"] == "testing":
        with app.app_context():
            database.db.create_all()

    return app


if __name__ == "__main__":
    create_app().run()
