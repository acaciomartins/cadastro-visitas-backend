from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    
    # Validar campos obrigatórios
    if not data.get('username'):
        return jsonify({'error': 'O campo username é obrigatório'}), 400
    if not data.get('name'):
        return jsonify({'error': 'O campo name é obrigatório'}), 400
    if not data.get('email'):
        return jsonify({'error': 'O campo email é obrigatório'}), 400
    if not data.get('password'):
        return jsonify({'error': 'O campo password é obrigatório'}), 400
    
    # Verificar se usuário já existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuário já existe'}), 400
    
    # Verificar se email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    try:
        user = User(
            username=data['username'],
            name=data['name'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        if not request.is_json:
            print("Requisição não contém JSON")
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        print(f"Dados recebidos no login: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        if 'username' not in data or 'password' not in data:
            print("Campos obrigatórios não fornecidos")
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
            
        user = User.query.filter_by(username=data['username']).first()
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário ou senha inválidos'}), 401
            
        if not user.check_password(data['password']):
            print("Senha inválida")
            return jsonify({'error': 'Usuário ou senha inválidos'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        print(f"Token gerado: {access_token}")
        
        user_dict = user.to_dict()
        print(f"Dados do usuário: {user_dict}")
        
        response = jsonify({
            'access_token': access_token,
            'user': user_dict
        })
        
        print(f"Resposta enviada: {response.get_json()}")
        return response, 200
    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET', 'OPTIONS'])
@jwt_required(locations=['headers'], fresh=False)
def get_current_user():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado no banco de dados")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        user_dict = user.to_dict()
        print(f"Dados do usuário: {user_dict}")
        
        return jsonify(user_dict)
    except Exception as e:
        print(f"Erro ao obter usuário atual: {str(e)}")
        return jsonify({'error': str(e)}), 422 