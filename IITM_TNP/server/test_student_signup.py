import json
import requests
import pytest
from application.api.authentication import *
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client



def test_student_registration(client):
    test_user_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password",
        "confirm_password": "test_password",
        "name": "Test User",
        "username": "testuser",
        "level": "BSc",
        "github_link": "https://github.com/testuser",
        "linkedin_link": "https://www.linkedin.com/in/testuser"
    }
)
    header = {"Content-Type":"application/json"}
    response = requests.post('http://localhost:3000/api/student_signup', data=test_user_data,headers=header)
    assert response.status_code == 200
    assert response.json() == {"msg": "User created"}


def test_user_login(client):

    login_data = json.dumps({
        "email": "test@example.com",
        "password": "test_password"
    })
    header = {"Content-Type":"application/json"}
    response = requests.post('http://localhost:3000/api/login', data=login_data,headers=header)
    print(response)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("name") == "Test User"

    assert response.json().get("role") == "student"

# def test_admin_registration(client):
#     test_admin_data = {
#         "email": "admin@example.com",
#         "password": "admin_password",
#         "confirm_password": "admin_password",
#         "name": "Admin User",
#         "username": "adminuser",
#         "level": "super admin",
#         "github_link": "https://github.com/adminuser",
#         "linkedin_link": "https://www.linkedin.com/in/adminuser"
#     }

#     with patch('application.api.authentication.send_mail', Mock()):
#         response = client.post('/api/admin_signup', json=test_admin_data)
#         assert response.status_code == 200
#         assert response.json == {"msg": "User created"}


if __name__ == '__main__':
    pytest.main()
