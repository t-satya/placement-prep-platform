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


def test_create_posts(client):

    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}

    test_post = json.dumps({
        "description": "Here's how to get started with competitive coding",
        "tags": ["Competitive Programming", "Coding", "DSA"]
    })
    response = requests.post("http://localhost:3000/api/posts",
                             data=test_post,
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg":"Posted successfully"}

def get_user_id_by_name(name):
    with app.app_context():
        user = User.query.filter_by(name=name).first()
        if user:
            return user.id
        return None

def test_edit_posts(client):

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
        get_post = Posts.query.filter_by(user_id=user_id).first()
    
    post_id = get_post.id
    access_token = login_response.json().get("access_token")

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}"}

    test_post = json.dumps({
        "description": "Here are some interesting ways to get started with competitive coding",
        "tags": ["Competitive Programming", "Data Structures"]
    })
    response = requests.put(f"http://localhost:3000/api/posts/{post_id}",
                             data=test_post,
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg":"Post edited successfully"}

def test_get_posts(client):

    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}

    
    response = requests.get("http://localhost:3000/api/posts",
                             headers=headers)

    assert response.status_code == 200
    assert response.json().get("msg") == "Success"
    assert "all_posts" in response.json()

def test_delete_post(client):
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
        get_post = Posts.query.filter_by(user_id=user_id).first()
    
    post_id = get_post.id
    access_token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(f"http://localhost:3000/api/posts/{post_id}",
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg":"Deleted successfully"}
