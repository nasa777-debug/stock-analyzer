import os
os.environ['DATABASE_URL']='sqlite:///:memory:'
from app import app

def test_routes():
    client=app.test_client()
    assert client.get('/login').status_code == 200
    assert client.get('/').status_code == 302
