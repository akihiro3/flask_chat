from flask_app import create_app

# Flaskのインスタンス化
app = create_app()

if __name__ == "__main__":
    app().run()
