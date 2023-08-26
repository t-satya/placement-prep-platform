import json
import requests
import pytest
from application.api.authentication import *
from main import app
from application.models import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_create_reply(client):

    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "name" in login_response.json()
    
    access_token = login_response.json().get("access_token")

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}

    test_reply = json.dumps({
        "description": "I really enjoyed your post. But ...",
        "postid": "1"
    })
    response = requests.post(f"http://localhost:3000/api/reply",
                            data=test_reply,
                            headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Replied to the post successfully"}

def test_edit_reply(client):

    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "name" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}

    test_reply = json.dumps({
        "description": "Thank you. Your post helped me a lot",
        "postid": "1"
    })
    with app.app_context():
        get_reply = Replies.query.filter_by(post_id=1).first()
    reply_id = get_reply.id
    response = requests.put(f"http://localhost:3000/api/reply/{reply_id}",
                            data=test_reply,
                            headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg":"Reply edited"}

def get_user_id_by_name(name):
    with app.app_context():
        user = User.query.filter_by(name=name).first()
        if user:
            return user.id
        return None
    
def test_delete_reply(client):
    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "name" in login_response.json()
    
    user_id = get_user_id_by_name(login_response.json().get("name"))

    with app.app_context():
        get_reply = Replies.query.filter_by(user_id=user_id).first()
    
    reply_id = get_reply.id
    access_token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(f"http://localhost:3000/api/reply/{reply_id}",
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg":"Reply Deleted"}
