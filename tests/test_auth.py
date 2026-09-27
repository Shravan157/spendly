import pytest
from werkzeug.security import generate_password_hash

def test_registration_success(client, db_conn):
    response = client.post('/register', data={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully!" in response.data

def test_registration_password_mismatch(client):
    response = client.post('/register', data={
        'name': 'Fail User',
        'email': 'fail@example.com',
        'password': 'password123',
        'confirm_password': 'wrongpassword'
    }, follow_redirects=True)
    assert b"Passwords do not match." in response.data

def test_login_success(client, db_conn):
    from database.db import create_user
    password = 'secretpassword'
    create_user("Login User", "login@example.com", generate_password_hash(password))

    response = client.post('/login', data={
        'email': 'login@example.com',
        'password': password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully logged in!" in response.data

def test_login_failure(client, db_conn):
    from database.db import create_user
    create_user("Login User", "login@example.com", generate_password_hash("correct"))

    response = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b"Invalid email or password." in response.data

def test_profile_access_unauthenticated(client):
    response = client.get('/profile', follow_redirects=True)
    # Should redirect to login
    assert b"Login" in response.data

def test_logout(client, db_conn):
    from database.db import create_user
    create_user("Logout User", "logout@example.com", generate_password_hash("pass"))

    client.post('/login', data={'email': 'logout@example.com', 'password': 'pass'})
    response = client.get('/logout', follow_redirects=True)
    assert b"You have been logged out." in response.data
