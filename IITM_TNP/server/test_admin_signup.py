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

def test_admin_signup(client):

    login_data = json.dumps({
        "email": "xyz@superadmin.mail.com",
        "password": "password"
    })
    header = {"Content-Type":"application/json"}
    login_response = requests.post('http://localhost:3000/api/login', data=login_data,headers=header)
    
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    access_token = login_response.json().get("access_token")

    headers = {"Content-Type":"application/json",
               "Authorization":f"Bearer {access_token}"}
    
    test_admin_data = json.dumps({
        "email": "test@admin.com",
        "password": "test_password",
        "confirm_password": "test_password",
        "name": "Test Admin",
        "username": "testadmin",
        "level": "SupportStaff",
        "github_link": "https://github.com/testadmin",
        "linkedin_link": "https://www.linkedin.com/in/testadmin"
    }
)
    response = requests.post("http://localhost:3000/api/admin_signup",
                            data=test_admin_data,
                            headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"msg": "User created"}
