from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Rito, User
from app import db

bp = Blueprint('ritos', __name__, url_prefix='/api/ritos')

@bp.route('', methods=['GET'])
@jwt_required()
def get_ritos():
    try:
        print("Recebendo requisição GET para listar ritos")
        ritos = Rito.query.all()
        print(f"Ritos encontrados: {len(ritos)}")
        return jsonify([rito.to_dict() for rito in ritos])
    except Exception as e:
        print(f"Erro ao listar ritos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_rito(id):
    try:
        rito = Rito.query.get_or_404(id)
        return jsonify(rito.to_dict())
    except Exception as e:
        print(f"Erro ao buscar rito: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_rito():
    try:
        print("Recebendo requisição POST para criar rito")
        user_id = get_jwt_identity()
        print(f"ID do usuário do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        if not user.is_admin:
            print("Usuário não é admin")
            return jsonify({'error': 'Apenas administradores podem criar ritos'}), 403
        
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Nenhum dado recebido'}), 400
        
        # Validar campos obrigatórios
        if not data.get('nome'):
            print("Campo nome não fornecido")
            return jsonify({'error': 'O campo nome é obrigatório'}), 400
        
        # Validar tamanho do nome
        if len(data['nome']) > 100:
            print("Nome excede o limite de caracteres")
            return jsonify({'error': 'O nome não pode ter mais de 100 caracteres'}), 400
        
        print("Criando novo rito...")
        rito = Rito(
            nome=data['nome'],
            descricao=data.get('descricao', '')
        )
        
        print("Adicionando rito à sessão...")
        db.session.add(rito)
        
        print("Commitando alterações...")
        db.session.commit()
        
        print(f"Rito criado com sucesso: {rito.to_dict()}")
        return jsonify(rito.to_dict()), 201
        
    except Exception as e:
        print(f"Erro ao criar rito: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_rito(id):
    try:
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return jsonify({'error': 'Apenas administradores podem atualizar ritos'}), 403
        
        rito = Rito.query.get_or_404(id)
        data = request.get_json()
        
        rito.nome = data.get('nome', rito.nome)
        rito.descricao = data.get('descricao', rito.descricao)
        db.session.commit()
        
        return jsonify(rito.to_dict())
    except Exception as e:
        print(f"Erro ao atualizar rito: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_rito(id):
    try:
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return jsonify({'error': 'Apenas administradores podem deletar ritos'}), 403
        
        rito = Rito.query.get_or_404(id)
        db.session.delete(rito)
        db.session.commit()
        
        return jsonify({'message': 'Rito deletado com sucesso'})
    except Exception as e:
        print(f"Erro ao deletar rito: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 