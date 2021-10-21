import os
from flask_app import create_app, db
from flask import jsonify
import pytest
import json


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                     'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    client = app.test_client()
    app_context = app.app_context()
    app_context.push()

    yield client


def test_all(client):
    # 非ログイン時のhomeページ
    rv = client.get('/', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post('/', data=dict(name="sam"), follow_redirects=True)
    assert rv.status_code == 200

    # 非ログイン時のchatページ
    rv = client.get('/chat/1', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post('/chat/1', data=dict(text="こんにちは"),
                     follow_redirects=True)
    assert rv.status_code == 200

    # アカウントの作成とログアウト
    rv = client.post('/create', data=dict(name="sam",
                     pas="sam"), follow_redirects=True)
    assert "account".encode() in rv.data
    rv = client.post('/create', data=dict(name="sam",
                     pas="sam"), follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/logout', follow_redirects=True)
    assert "logout".encode() in rv.data

    # アカウントのログイン失敗時
    rv = client.get('/login', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post('/login', data=dict(name="fal",
                     pas="fal"), follow_redirects=True)
    assert "user".encode() in rv.data
    rv = client.post('/login', data=dict(name="sam",
                     pas="fal"), follow_redirects=True)
    assert "Password".encode() in rv.data

    # アカウントのログイン成功時
    rv = client.post('/login', data=dict(name="sam",
                     pas="sam"), follow_redirects=True)
    assert "login".encode() in rv.data

    # アカウントのログイン後の各ページ
    rv = client.post('/', data=dict(name="sam"), follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/login', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/create', follow_redirects=True)
    assert "login".encode() in rv.data
    rv = client.post('/create', data=dict(name="aaa",
                     pas="aaa"), follow_redirects=True)
    assert "login".encode() in rv.data

    # ログイン後のチャットページ
    rv = client.get('/chat/1', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/chat/2', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post('/chat/1', data=dict(text="こんにちは"),
                     follow_redirects=True)
    assert rv.status_code == 200
    rv = client.post('/chat/2', data=dict(text="こんにちは"),
                     follow_redirects=True)
    assert rv.status_code == 200

    # アカウントの削除
    rv = client.get('/delete', follow_redirects=True)
    assert "account".encode() in rv.data
