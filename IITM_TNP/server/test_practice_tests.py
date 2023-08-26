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


def test_create_practice_test(client):

    login_data = json.dumps({
        "email": "test@admin.com",
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

    test_practice_test = json.dumps({
        "name": "PracticeTest1",
        "tags": ["Logical Reasoning", "Verbal Aptitude"],
        "question_ids": ["1", "2", "3", "4", "5", "6"]
    }

    )
    response = requests.post("http://localhost:3000/api/practice_tests",
                             data=test_practice_test,
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Practice Test created"}


def test_edit_practice_tests(client):

    login_data = json.dumps({
        "email": "test@admin.com",
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

    test_practice_test = json.dumps({
        "practice_test_id": 1,
        "name": "Practice Test 1",
        "question_ids_to_remove": [1],
        "tags": [],
        "question_ids_to_add": []

    }
    )
    response = requests.put("http://localhost:3000/api/practice_tests",
                            data=test_practice_test,
                            headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Practice test updated"}


def test_get_practice_test(client):

    login_data = json.dumps({
        "email": "test@admin.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get("http://localhost:3000/api/practice_tests/1",
                            headers=headers)

    assert response.status_code == 200
    assert response.json().get("msg") == "Success"
    assert "practice_tests" in response.json()

def test_delete_practice_test(client):
    login_data = json.dumps({
        "email": "test@admin.com",
        "password": "test_password"
    })
    header = {"Content-Type": "application/json"}
    login_response = requests.post(
        'http://localhost:3000/api/login', data=login_data, headers=header)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}


    response = requests.delete("http://localhost:3000/api/practice_tests/1",
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Practice test deleted"}
