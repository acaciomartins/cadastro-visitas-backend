import pytest
from app import create_app, db
from app.models import User, Grau
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def admin_user(app):
    with app.app_context():
        # Verifica se o usuário admin já existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@test.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        return admin

@pytest.fixture
def regular_user(app):
    with app.app_context():
        user = User(username='user', email='user@test.com', is_admin=False)
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_grau(app, client):
    with app.app_context():
        grau = Grau(numero=1, descricao='Primeiro Grau')
        db.session.add(grau)
        db.session.commit()
        grau_id = grau.id
        db.session.expunge_all()  # Limpa a sessão
        return grau_id  # Retorna apenas o ID

def test_create_grau_as_admin(client, admin_user):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Criar grau
    response = client.post('/api/graus', 
        json={'numero': 1, 'descricao': 'Primeiro Grau'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.json['numero'] == 1
    assert response.json['descricao'] == 'Primeiro Grau'

def test_create_grau_as_regular_user(client, regular_user):
    # Login como usuário regular
    response = client.post('/api/auth/login', json={
        'username': 'user',
        'password': 'user123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Tentar criar grau
    response = client.post('/api/graus', 
        json={'numero': 1, 'descricao': 'Primeiro Grau'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403

def test_create_grau_without_auth(client):
    response = client.post('/api/graus', 
        json={'numero': 1, 'descricao': 'Primeiro Grau'}
    )
    assert response.status_code == 401

def test_create_grau_with_invalid_data(client, admin_user):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Tentar criar grau sem dados obrigatórios
    response = client.post('/api/graus', 
        json={},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 400
    assert 'error' in response.json

def test_list_graus(client, admin_user):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Criar alguns graus
    with client.application.app_context():
        grau1 = Grau(numero=1, descricao='Primeiro Grau')
        grau2 = Grau(numero=2, descricao='Segundo Grau')
        db.session.add(grau1)
        db.session.add(grau2)
        db.session.commit()

    # Listar graus
    response = client.get('/api/graus',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_grau_by_id(client, admin_user, test_grau):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Buscar grau por ID
    response = client.get(f'/api/graus/{test_grau}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['numero'] == 1
    assert response.json['descricao'] == 'Primeiro Grau'

def test_get_nonexistent_grau(client, admin_user):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Tentar buscar grau inexistente
    response = client.get('/api/graus/999',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 404

def test_update_grau_as_admin(client, admin_user, test_grau):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Atualizar grau
    response = client.put(f'/api/graus/{test_grau}',
        json={'numero': 3, 'descricao': 'Terceiro Grau'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['numero'] == 3
    assert response.json['descricao'] == 'Terceiro Grau'

def test_update_grau_as_regular_user(client, regular_user, test_grau):
    # Login como usuário regular
    response = client.post('/api/auth/login', json={
        'username': 'user',
        'password': 'user123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Tentar atualizar grau
    response = client.put(f'/api/graus/{test_grau}',
        json={'numero': 3, 'descricao': 'Terceiro Grau'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403

def test_delete_grau_as_admin(client, admin_user, test_grau):
    # Login como admin
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Deletar grau
    response = client.delete(f'/api/graus/{test_grau}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200

    # Verificar se o grau foi deletado
    response = client.get(f'/api/graus/{test_grau}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 404

def test_delete_grau_as_regular_user(client, regular_user, test_grau):
    # Login como usuário regular
    response = client.post('/api/auth/login', json={
        'username': 'user',
        'password': 'user123'
    })
    assert response.status_code == 200
    token = response.json['access_token']

    # Tentar deletar grau
    response = client.delete(f'/api/graus/{test_grau}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403 