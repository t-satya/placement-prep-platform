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


def test_create_question(client):

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

    test_question = json.dumps({
                "name": "Water Image 5",                                 
                "tags": ["Maths","Reasoning"],                                     
                "description": "Identify water image",                      
                "question_type": "MCQ",                                    
                "options": {"1":"A","2":"B","3":"C","4":"D"},               
                "correct_answers" : ["1"]
            }

    )
    response = requests.post("http://localhost:3000/api/question",
                             data=test_question,
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Question created"}

def test_edit_question(client):

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

    test_question = json.dumps({
                "practice_test_id":1,
                "name": "Water-Image-1",                                 
            }
    )
    response = requests.put("http://localhost:3000/api/practice_tests",
                             data=test_question,
                             headers=headers)

    assert response.status_code == 200
    assert response.json() == {"msg": "Question updated"}


def test_get_question(client):

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
    assert "questions" in response.json()

# def test_delete_question(client):
#     login_data = json.dumps({
#         "email": "test@admin.com",
#         "password": "test_password"
#     })
#     header = {"Content-Type": "application/json"}
#     login_response = requests.post(
#         'http://localhost:3000/api/login', data=login_data, headers=header)

#     assert login_response.status_code == 200
#     assert "access_token" in login_response.json()

#     access_token = login_response.json().get("access_token")

#     headers = {"Authorization": f"Bearer {access_token}"}

    
#     response = requests.delete("http://localhost:3000/api/question/1",
#                              headers=headers)

#     assert response.status_code == 200
#     assert response.json() == {"msg": "Question deleted"}