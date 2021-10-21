from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_app.models.bot import Bot


bot = Bot()
app = None
db = None

# flaskのインスタンス化，dbの初期設定，test時の処理


def create_app(test_config=None):
    global app, db
    app = Flask(__name__)
    db = SQLAlchemy(app)

    # 設定
    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_AS_ASCII=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///user.db',
        SECRET_KEY='dev'
    )

    if test_config is None:
        # testでない時
        app.config.from_pyfile('config.py')
    else:
        # testの時
        app.config.from_mapping(test_config)

    # views.pyの読み込み
    from flask_app import views
    return app
