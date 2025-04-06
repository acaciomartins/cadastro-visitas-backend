from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Grau, User
from app import db
from werkzeug.exceptions import NotFound
import logging

bp = Blueprint('graus', __name__, url_prefix='/api/graus')

@bp.route('', methods=['GET'])
@jwt_required()
def get_graus():
    try:
        print("Listando graus...")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        graus = Grau.query.all()
        print(f"Encontrados {len(graus)} graus")
        return jsonify([grau.to_dict() for grau in graus])
    except Exception as e:
        print(f"Erro ao listar graus: {str(e)}")
        return jsonify({'error': 'Erro ao listar graus'}), 500

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_grau(id):
    try:
        print(f"Buscando grau com ID {id}")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        grau = Grau.query.get(id)
        if not grau:
            print(f"Grau com ID {id} não encontrado")
            return jsonify({'error': 'Grau não encontrado'}), 404
        return jsonify(grau.to_dict())
    except Exception as e:
        print(f"Erro ao buscar grau: {str(e)}")
        return jsonify({'error': 'Erro ao buscar grau'}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_grau():
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
            return jsonify({'error': 'Apenas administradores podem criar graus'}), 403
        
        if not request.is_json:
            print("Requisição não contém JSON")
            return jsonify({'error': 'O conteúdo deve ser JSON'}), 400
            
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        if 'numero' not in data or 'descricao' not in data:
            print("Dados incompletos")
            return jsonify({'error': 'Número e descrição são obrigatórios'}), 400
            
        try:
            numero = int(data['numero'])
        except (ValueError, TypeError):
            print("Número inválido")
            return jsonify({'error': 'Número deve ser um valor inteiro'}), 400
            
        if not isinstance(data['descricao'], str) or len(data['descricao'].strip()) == 0:
            print("Descrição inválida")
            return jsonify({'error': 'Descrição é obrigatória e deve ser uma string não vazia'}), 400
        
        grau = Grau(numero=numero, descricao=data['descricao'].strip())
        print(f"Criando grau: {grau.to_dict()}")
        
        db.session.add(grau)
        db.session.commit()
        print("Grau criado com sucesso")
        
        return jsonify(grau.to_dict()), 201
    except Exception as e:
        print(f"Erro ao criar grau: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar grau'}), 500

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_grau(id):
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
            return jsonify({'error': 'Apenas administradores podem atualizar graus'}), 403
        
        grau = Grau.query.get(id)
        if not grau:
            print(f"Grau com ID {id} não encontrado")
            return jsonify({'error': 'Grau não encontrado'}), 404

        data = request.get_json()
        print(f"Dados recebidos para atualização: {data}")
        
        if not data:
            print("Nenhum dado recebido")
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        if 'numero' in data:
            try:
                grau.numero = int(data['numero'])
            except ValueError:
                print("Número inválido")
                return jsonify({'error': 'Número deve ser um valor inteiro'}), 400
                
        if 'descricao' in data:
            grau.descricao = data['descricao']
            
        db.session.commit()
        print("Grau atualizado com sucesso")
        
        return jsonify(grau.to_dict())
    except Exception as e:
        print(f"Erro ao atualizar grau: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar grau'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_grau(id):
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
            return jsonify({'error': 'Apenas administradores podem deletar graus'}), 403
        
        grau = Grau.query.get(id)
        if not grau:
            print(f"Grau com ID {id} não encontrado")
            return jsonify({'error': 'Grau não encontrado'}), 404
            
        print(f"Deletando grau: {grau.to_dict()}")
        db.session.delete(grau)
        db.session.commit()
        print("Grau deletado com sucesso")
        
        return jsonify({'message': 'Grau deletado com sucesso'})
    except Exception as e:
        print(f"Erro ao deletar grau: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar grau'}), 500 