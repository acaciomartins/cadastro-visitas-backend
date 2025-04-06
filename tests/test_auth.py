import pytest
from app import create_app
from app.models import User, db
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        return user

def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Usuário criado com sucesso'

def test_register_duplicate_username(client):
    # Primeiro registro
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test1@example.com',
        'password': 'test123'
    })
    
    # Tentativa de registro com mesmo username
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test2@example.com',
        'password': 'test123'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Usuário já existe'

def test_login_success(client, admin_user):
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['username'] == 'admin'
    assert data['user']['is_admin'] == True

def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Usuário ou senha inválidos'

def test_get_current_user(client, admin_user):
    # Primeiro fazer login para obter o token
    login_response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = login_response.get_json()['access_token']
    
    # Usar o token para acessar a rota /me
    response = client.get('/api/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'admin'
    assert data['is_admin'] == True 