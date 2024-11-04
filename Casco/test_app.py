import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_user(client):
    response = client.post('/create_user', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "is_leader": True
    })
    assert response.status_code == 201

def test_login(client):
    client.post('/create_user', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "is_leader": True
    })
    response = client.post('/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
