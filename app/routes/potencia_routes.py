from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Potencia, User
from app import db
import logging

bp = Blueprint('potencias', __name__, url_prefix='/api/potencias')

@bp.route('', methods=['GET'])
@jwt_required()
def get_potencias():
    print("Recebendo requisição GET para /potencias")
    potencias = Potencia.query.all()
    return jsonify([potencia.to_dict() for potencia in potencias])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_potencia(id):
    potencia = db.session.get(Potencia, id)
    if not potencia:
        return jsonify({'error': 'Potência não encontrada'}), 404
    return jsonify(potencia.to_dict())

@bp.route('', methods=['POST'])
@jwt_required()
def create_potencia():
    print("Recebendo requisição POST para /potencias")
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário do token: {user_id}")
        user = db.session.get(User, user_id)
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado', 'details': 'Token inválido ou usuário não existe'}), 404
        if not user.is_admin:
            print("Usuário não é admin")
            return jsonify({'error': 'Apenas administradores podem criar potências', 'details': 'Usuário não é admin'}), 403
        
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        if not data:
            print("Dados não fornecidos")
            return jsonify({'error': 'Dados não fornecidos', 'details': 'O corpo da requisição está vazio'}), 422
            
        if 'nome' not in data:
            print("Nome não fornecido")
            return jsonify({'error': 'O nome é obrigatório', 'details': 'Campo nome não encontrado nos dados'}), 422
            
        if not data['nome'] or not data['nome'].strip():
            print("Nome vazio")
            return jsonify({'error': 'O nome é obrigatório', 'details': 'Campo nome está vazio'}), 422
            
        if 'sigla' not in data:
            print("Sigla não fornecida")
            return jsonify({'error': 'A sigla é obrigatória', 'details': 'Campo sigla não encontrado nos dados'}), 422
            
        if not data['sigla'] or not data['sigla'].strip():
            print("Sigla vazia")
            return jsonify({'error': 'A sigla é obrigatória', 'details': 'Campo sigla está vazio'}), 422
            
        if len(data['sigla']) > 10:
            print("Sigla muito longa")
            return jsonify({'error': 'A sigla deve ter no máximo 10 caracteres', 'details': f"Sigla tem {len(data['sigla'])} caracteres"}), 422
            
        if len(data['nome']) > 100:
            print("Nome muito longo")
            return jsonify({'error': 'O nome deve ter no máximo 100 caracteres', 'details': f"Nome tem {len(data['nome'])} caracteres"}), 422
        
        # Verificar se já existe uma potência com a mesma sigla
        existing_potencia = Potencia.query.filter_by(sigla=data['sigla'].strip()).first()
        if existing_potencia:
            print("Sigla já existe")
            return jsonify({'error': 'Já existe uma potência com esta sigla', 'details': f"Sigla {data['sigla']} já está em uso"}), 422
                
        potencia = Potencia(
            nome=data['nome'].strip(),
            sigla=data['sigla'].strip()
        )
        
        db.session.add(potencia)
        db.session.commit()
        
        print(f"Potência criada com sucesso: {potencia.to_dict()}")
        return jsonify(potencia.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar potência: {str(e)}")
        return jsonify({'error': f'Erro ao criar potência', 'details': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_potencia(id):
    user = db.session.get(User, get_jwt_identity())
    if not user:
        return jsonify({'error': 'Usuário não encontrado', 'details': 'Token inválido ou usuário não existe'}), 404
    if not user.is_admin:
        return jsonify({'error': 'Apenas administradores podem atualizar potências'}), 403
    
    potencia = db.session.get(Potencia, id)
    if not potencia:
        return jsonify({'error': 'Potência não encontrada'}), 404
        
    data = request.get_json()
    print(f"Dados recebidos para atualização: {data}")
    
    potencia.nome = data.get('nome', potencia.nome)
    potencia.sigla = data.get('sigla', potencia.sigla)
    
    try:
        db.session.commit()
        print(f"Potência atualizada com sucesso: {potencia.to_dict()}")
        return jsonify(potencia.to_dict())
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar potência: {str(e)}")
        return jsonify({'error': f'Erro ao atualizar potência', 'details': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_potencia(id):
    user = db.session.get(User, get_jwt_identity())
    if not user:
        return jsonify({'error': 'Usuário não encontrado', 'details': 'Token inválido ou usuário não existe'}), 404
    if not user.is_admin:
        return jsonify({'error': 'Apenas administradores podem deletar potências'}), 403
    
    potencia = db.session.get(Potencia, id)
    if not potencia:
        return jsonify({'error': 'Potência não encontrada'}), 404
        
    try:
        db.session.delete(potencia)
        db.session.commit()
        print(f"Potência {id} deletada com sucesso")
        return jsonify({'message': 'Potência deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar potência: {str(e)}")
        return jsonify({'error': f'Erro ao deletar potência', 'details': str(e)}), 500 