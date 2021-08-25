# ベースイメージ
FROM python:3.6

RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

RUN mkdir /var/www

WORKDIR /var/www

# 依存Pythonライブラリ一覧コピー
COPY requirements.txt ./

# 依存Pythonライブラリインストール
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uwsgi","--ini","/var/www/uwsgi.ini"]