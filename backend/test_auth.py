import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import create_app
from backend.models.user import User
from backend.database import db
import json
from config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def register(client, username, email, password):
    return client.post('/api/auth/register', json={
        'username': username,
        'email': email,
        'password': password
    })

def test_successful_registration(client):
    resp = register(client, 'user1', 'user1@example.com', 'Password123')
    data = resp.get_json()
    assert resp.status_code == 201
    assert 'access_token' in data
    assert data['user']['username'] == 'user1'

def test_missing_fields(client):
    resp = register(client, '', 'user2@example.com', 'Password123')
    assert resp.status_code == 400
    resp = register(client, 'user2', '', 'Password123')
    assert resp.status_code == 400
    resp = register(client, 'user2', 'user2@example.com', '')
    assert resp.status_code == 400

def test_invalid_email(client):
    resp = register(client, 'user3', 'invalidemail', 'Password123')
    assert resp.status_code == 400
    assert 'Invalid email format' in resp.get_json()['error']

def test_weak_password(client):
    resp = register(client, 'user4', 'user4@example.com', 'short')
    assert resp.status_code == 400
    resp = register(client, 'user4', 'user4@example.com', 'allletters')
    assert resp.status_code == 400
    resp = register(client, 'user4', 'user4@example.com', '12345678')
    assert resp.status_code == 400

def test_duplicate_email(client):
    register(client, 'user5', 'user5@example.com', 'Password123')
    resp = register(client, 'user6', 'user5@example.com', 'Password123')
    assert resp.status_code == 400
    assert 'Email already registered' in resp.get_json()['error']

def test_duplicate_username(client):
    register(client, 'user7', 'user7@example.com', 'Password123')
    resp = register(client, 'user7', 'user8@example.com', 'Password123')
    assert resp.status_code == 400
    assert 'Username already taken' in resp.get_json()['error']

def test_login_success(client):
    # Register a user first
    register(client, 'loginuser', 'loginuser@example.com', 'Password123')
    resp = client.post('/api/auth/login', json={
        'email': 'loginuser@example.com',
        'password': 'Password123'
    })
    data = resp.get_json()
    assert resp.status_code == 200
    assert 'access_token' in data
    assert data['user']['username'] == 'loginuser'

def test_login_wrong_password(client):
    register(client, 'wrongpass', 'wrongpass@example.com', 'Password123')
    resp = client.post('/api/auth/login', json={
        'email': 'wrongpass@example.com',
        'password': 'WrongPassword'
    })
    assert resp.status_code == 401
    assert 'Invalid credentials' in resp.get_json()['error']

def test_login_nonexistent_email(client):
    resp = client.post('/api/auth/login', json={
        'email': 'doesnotexist@example.com',
        'password': 'Password123'
    })
    assert resp.status_code == 401
    assert 'Invalid credentials' in resp.get_json()['error'] 