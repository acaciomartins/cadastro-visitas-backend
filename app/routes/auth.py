from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from ..models import User, db
from ..utils.password_validator import PasswordValidator

auth_bp = Blueprint('auth', __name__)
password_validator = PasswordValidator()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(minutes=15)
    )

    return jsonify({'access_token': access_token})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado'}), 400

    if not password_validator.validate(password):
        return jsonify({'error': 'A senha não atende aos requisitos mínimos de segurança'}), 400

    hashed_password = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not all([current_password, new_password]):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Senha atual incorreta'}), 401

    if not password_validator.validate(new_password):
        return jsonify({'error': 'A nova senha não atende aos requisitos mínimos de segurança'}), 400

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Senha alterada com sucesso'}) 