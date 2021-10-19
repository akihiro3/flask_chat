from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_app.models.bot import Bot


bot = Bot()
app = None
db = None


def create_app(test_config=None):
    # create and configure the app
    global app, db
    #
    app = Flask(__name__)
    db = SQLAlchemy(app)
    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_AS_ASCII=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///user.db',
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        print("test")
        app.config.from_mapping(test_config)

    from flask_app import views
    return app
