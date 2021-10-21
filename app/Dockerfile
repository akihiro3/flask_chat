# ベースイメージ
FROM python:3.6

# pipのupgrade
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

# 作業ディレクトリの変更
WORKDIR /var/www/app

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./

# 依存Pythonライブラリインストール
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["uwsgi","--ini","/var/www/app/uwsgi.ini"]