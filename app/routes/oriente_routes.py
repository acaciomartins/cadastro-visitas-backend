from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Oriente, User
from app import db
import logging

bp = Blueprint('orientes', __name__, url_prefix='/api/orientes')

@bp.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orientes():
    try:
        print("Listando orientes...")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        orientes = Oriente.query.all()
        print(f"Encontrados {len(orientes)} orientes")
        return jsonify([oriente.to_dict() for oriente in orientes])
    except Exception as e:
        print(f"Erro ao listar orientes: {str(e)}")
        return jsonify({'error': 'Erro ao listar orientes'}), 500

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_oriente(id):
    try:
        print(f"Buscando oriente com ID {id}")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        oriente = Oriente.query.get(id)
        if not oriente:
            print(f"Oriente com ID {id} não encontrado")
            return jsonify({'error': 'Oriente não encontrado'}), 404
        return jsonify(oriente.to_dict())
    except Exception as e:
        print(f"Erro ao buscar oriente: {str(e)}")
        return jsonify({'error': 'Erro ao buscar oriente'}), 500

@bp.route('', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_oriente():
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        if not user.is_admin:
            print("Usuário não é administrador")
            return jsonify({'error': 'Apenas administradores podem criar orientes'}), 403
        
        if not request.is_json:
            print("Requisição não contém JSON")
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        campos_obrigatorios = ['nome', 'uf']
        for campo in campos_obrigatorios:
            if campo not in data:
                print(f"Campo obrigatório não fornecido: {campo}")
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
            
        if not isinstance(data['nome'], str) or len(data['nome'].strip()) == 0:
            print("Nome inválido")
            return jsonify({'error': 'Nome é obrigatório e deve ser uma string não vazia'}), 400
            
        if not isinstance(data['uf'], str) or len(data['uf'].strip()) != 2:
            print("UF inválida")
            return jsonify({'error': 'UF deve ter exatamente 2 caracteres'}), 400
        
        oriente = Oriente(
            nome=data['nome'].strip(),
            uf=data['uf'].strip().upper()
        )
        print(f"Criando oriente: {oriente.to_dict()}")
        
        db.session.add(oriente)
        db.session.commit()
        print("Oriente criado com sucesso")
        
        return jsonify(oriente.to_dict()), 201
    except Exception as e:
        print(f"Erro ao criar oriente: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar oriente'}), 500

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_oriente(id):
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        if not user.is_admin:
            print("Usuário não é administrador")
            return jsonify({'error': 'Apenas administradores podem atualizar orientes'}), 403
        
        oriente = Oriente.query.get(id)
        if not oriente:
            print(f"Oriente com ID {id} não encontrado")
            return jsonify({'error': 'Oriente não encontrado'}), 404

        if not request.is_json:
            print("Requisição não contém JSON")
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        print(f"Dados recebidos para atualização: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Dados não fornecidos'}), 400
                
        if 'nome' in data:
            if not isinstance(data['nome'], str) or len(data['nome'].strip()) == 0:
                print("Nome inválido")
                return jsonify({'error': 'Nome deve ser uma string não vazia'}), 400
            oriente.nome = data['nome'].strip()
            
        if 'uf' in data:
            if not isinstance(data['uf'], str) or len(data['uf'].strip()) != 2:
                print("UF inválida")
                return jsonify({'error': 'UF deve ter exatamente 2 caracteres'}), 400
            oriente.uf = data['uf'].strip().upper()
            
        db.session.commit()
        print("Oriente atualizado com sucesso")
        
        return jsonify(oriente.to_dict())
    except Exception as e:
        print(f"Erro ao atualizar oriente: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar oriente'}), 500

@bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_oriente(id):
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        if not user.is_admin:
            print("Usuário não é administrador")
            return jsonify({'error': 'Apenas administradores podem deletar orientes'}), 403
        
        oriente = Oriente.query.get(id)
        if not oriente:
            print(f"Oriente com ID {id} não encontrado")
            return jsonify({'error': 'Oriente não encontrado'}), 404
            
        print(f"Deletando oriente: {oriente.to_dict()}")
        db.session.delete(oriente)
        db.session.commit()
        print("Oriente deletado com sucesso")
        
        return jsonify({'message': 'Oriente deletado com sucesso'})
    except Exception as e:
        print(f"Erro ao deletar oriente: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar oriente'}), 500 