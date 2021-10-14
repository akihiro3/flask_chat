from flask import Flask, config, render_template, request, redirect, jsonify, session
from flask.globals import session
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from models.bot import Bot


app = Flask(__name__)
app.secret_key = 'user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
bot = Bot()

# cssファイルとjsファイルを最新版を使うようにする


@app.context_processor  # HTMLから呼び出せるようにする
def add_staticfile():
    # folderとfailenameを取得
    def staticfile_cp(folder, fname):
        # 指定したファイルのpathを取得
        path = os.path.join(app.root_path, 'static/', folder, fname)
        # ファイルの最終内容更新日時を取得
        mtime = str(int(os.stat(path).st_mtime))
        # 最終内容更新日時のverのファイルのpathを返す
        return '/static/' + folder + "/" + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)

# ユーザデータのデータベース


class User(db.Model):
    # ユーザID
    id = db.Column(db.Integer, primary_key=True)
    # ユーザの名前
    name = db.Column(db.String(30), nullable=False)
    # Password
    pas = db.Column(db.String(30), nullable=False)
    # 日付
    date = db.Column(db.DateTime, nullable=False)


# ユーザのチャットデータベース
class Chat(db.Model):
    # ユーザID
    id = db.Column(db.Integer, primary_key=True)
    # ユーザの入力
    user_chat = db.Column(db.String(100), nullable=False)
    # botの出力
    bot_chat = db.Column(db.String(100), nullable=False)

    # ユーザidをユーザデータのデータベースと紐づける
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref('chats', lazy=True))


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        # home画面を表示
        if not session.get('login'):
            return render_template("home.html")
        else:
            name = session.get('login')
            login_user = db.session.query(User).\
                filter(User.name == name).\
                first()
            login = login_user.id
            return redirect("/chat/%d" % login)
    else:
        name = request.form.get("name")
        today = datetime.date.today()

        login_user = db.session.query(User).\
            filter(User.name == name).\
            first()

        if not login_user:
            flash("Userが存在しません")
        else:
            login = login_user.id
            return redirect("/chat/%d" % login)

        session.pop('login', None)
        return render_template("login.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not session.get('login'):
            return render_template("login.html")
        else:
            name = session.get('login')
            login_user = db.session.query(User).\
                filter(User.name == name).\
                first()
            login = login_user.id
            return redirect("/chat/%d" % login)

    else:
        # ユーザの名前と日付を取得
        name = request.form.get("name")
        pas = request.form.get("pas")
        today = datetime.date.today()

        # ユーザデータベースにデータがあるか
        login_user = db.session.query(User).\
            filter(User.name == name).\
            first()

        if login_user is None:
            flash("ユーザ名が異なります")
        else:
            login_pas = login_user.pas
            if login_pas != pas:
                flash("Passwordが異なります")
            else:
                session['login'] = name
                # loginしたユーザのIDを取得
                login = login_user.id
                # ユーザのチャットページへ
                return redirect("/chat/%d" % login)

        return render_template("login.html")


@app.route('/logout')
def logout():
    flash("ログアウトしました")
    session.pop('login', None)
    return render_template("home.html")


@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "GET":
        if not session.get('login'):
            return render_template("create.html")
        else:
            name = session.get('login')
            login_user = db.session.query(User).\
                filter(User.name == name).\
                first()
            login = login_user.id
            return redirect("/chat/%d" % login)
    else:
        if not session.get('login'):
            name = request.form.get("name")
            pas = request.form.get("pas")
            today = datetime.date.today()

            login_user = db.session.query(User).\
                filter(User.name == name).\
                first()

            if login_user is None:
                login_user = User(name=name, pas=pas, date=today,)
                db.session.add(login_user)
                db.session.commit()
                session['login'] = True
                # loginしたユーザのIDを取得
                login = login_user.id
                # ユーザのチャットページへ
                return redirect("/chat/%d" % login)

            # 既存ユーザの場合
            else:
                flash("既に存在するユーザです")

            return render_template("create.html")

        else:
            return render_template("room.html")


@app.route("/chat/<int:id>", methods=["GET", "POST"])
# チャットページでの処理
def chat(id):
    if request.method == "GET":
        # GET requestはチャットページを表示
        if not session.get('login'):
            return render_template("login.html")
        else:
            user = User.query.get(id)
            return render_template("chat.html", user=user)
    else:
        if not session.get('login'):
            return render_template("login.html")
        else:
            # ユーザIDと入力を取得
            user = User.query.get(id)
            user_chat = request.form.get("text", default="こんにちは", type=str)

            # botの返答の処理
            bot_chat = bot.message(user_chat)
            new_chat = Chat(user_chat=user_chat, bot_chat=bot_chat, user=user)
            db.session.add(new_chat)
            db.session.commit()

            # チャットページを更新する
            return render_template("chat.html", user=user)


@app.route('/delete/<int:id>')
# ユーザデータのdelete時の処理
def delete(id):
    # ユーザデータをデータベースから消す
    user = User.query.get(id)
    chat = db.session.query(Chat).\
        filter(Chat.user_id == id).\
        all()

    for log in chat:
        db.session.delete(log)

    db.session.delete(user)
    db.session.commit()

    # home画面に戻す
    return redirect('/')


@app.route('/api', methods=["POST"])
def api():
    if request.method == 'POST':
        user_talk = request.json

        user_name = user_talk.get('name')
        login_user = db.session.query(User).\
            filter(User.name == user_name).\
            first()
        user_pas = user_talk.get('pas')
        if login_user is None:
            talk = "ユーザ名が異なります"
        else:
            login_pas = login_user.pas
            if login_pas != user_pas:
                talk = "Passwordが異なります"
            else:
                talk = user_talk.get('talk')
                bot_chat = bot.message(talk)

        return jsonify({"reply": bot_chat})
    else:
        return jsonify({"reply": "Error"})


if __name__ == '__main__':
    app.run(debug=True)
