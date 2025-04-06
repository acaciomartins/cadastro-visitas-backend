from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Loja, User, Potencia, Rito, Oriente
from app import db
import logging

bp = Blueprint('lojas', __name__, url_prefix='/api/lojas')

@bp.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_lojas():
    try:
        print("Listando lojas...")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Se for admin, retorna todas as lojas
        if user.is_admin:
            lojas = Loja.query.all()
        else:
            # Se não for admin, retorna apenas as lojas do usuário
            lojas = Loja.query.filter_by(user_id=user_id).all()
            
        print(f"Encontradas {len(lojas)} lojas")
        return jsonify([loja.to_dict() for loja in lojas])
    except Exception as e:
        print(f"Erro ao listar lojas: {str(e)}")
        return jsonify({'error': 'Erro ao listar lojas'}), 500

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_loja(id):
    try:
        print(f"Buscando loja com ID {id}")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        loja = Loja.query.get(id)
        if not loja:
            print(f"Loja com ID {id} não encontrada")
            return jsonify({'error': 'Loja não encontrada'}), 404
            
        # Verificar se o usuário é admin ou se a loja pertence ao usuário
        if not user.is_admin and loja.user_id != user_id:
            print("Usuário não tem permissão para ver esta loja")
            return jsonify({'error': 'Você não tem permissão para ver esta loja'}), 403
            
        return jsonify(loja.to_dict())
    except Exception as e:
        print(f"Erro ao buscar loja: {str(e)}")
        return jsonify({'error': 'Erro ao buscar loja'}), 500

@bp.route('', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_loja():
    try:
        print("Recebendo requisição POST para /api/lojas")
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        # Validar campos obrigatórios
        if not data.get('nome'):
            print("Campo nome não fornecido")
            return jsonify({'error': 'O campo nome é obrigatório'}), 400
        if not data.get('numero'):
            print("Campo numero não fornecido")
            return jsonify({'error': 'O campo numero é obrigatório'}), 400
        if not data.get('potencia_id'):
            print("Campo potencia_id não fornecido")
            return jsonify({'error': 'O campo potencia_id é obrigatório'}), 400
        if not data.get('rito_id'):
            print("Campo rito_id não fornecido")
            return jsonify({'error': 'O campo rito_id é obrigatório'}), 400
        if not data.get('oriente_nome'):
            print("Campo oriente_nome não fornecido")
            return jsonify({'error': 'O campo oriente_nome é obrigatório'}), 400
        if not data.get('oriente_uf'):
            print("Campo oriente_uf não fornecido")
            return jsonify({'error': 'O campo oriente_uf é obrigatório'}), 400
        
        # Verificar se potência existe
        potencia = Potencia.query.get(data['potencia_id'])
        if not potencia:
            print(f"Potência com ID {data['potencia_id']} não encontrada")
            return jsonify({'error': 'Potência não encontrada'}), 404
        
        # Verificar se rito existe
        rito = Rito.query.get(data['rito_id'])
        if not rito:
            print(f"Rito com ID {data['rito_id']} não encontrado")
            return jsonify({'error': 'Rito não encontrado'}), 404
        
        # Criar ou encontrar oriente
        oriente = Oriente.query.filter_by(
            nome=data['oriente_nome'],
            uf=data['oriente_uf']
        ).first()
        
        if not oriente:
            print(f"Criando novo oriente: {data['oriente_nome']} - {data['oriente_uf']}")
            oriente = Oriente(
                nome=data['oriente_nome'],
                uf=data['oriente_uf']
            )
            db.session.add(oriente)
            db.session.flush()  # Para obter o ID do oriente
        
        # Obter o ID do usuário do token
        user_id = get_jwt_identity()
        
        # Criar loja
        print("Criando nova loja")
        loja = Loja(
            nome=data['nome'],
            numero=data['numero'],
            potencia_id=data['potencia_id'],
            rito_id=data['rito_id'],
            oriente_id=oriente.id,
            user_id=user_id
        )
        
        db.session.add(loja)
        db.session.commit()
        print(f"Loja criada com sucesso: {loja.to_dict()}")
        
        return jsonify(loja.to_dict()), 201
    except Exception as e:
        print(f"Erro ao criar loja: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_loja(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        loja = Loja.query.get(id)
        if not loja:
            return jsonify({'error': 'Loja não encontrada'}), 404
            
        # Verificar se o usuário é admin ou se a loja pertence ao usuário
        if not user.is_admin and loja.user_id != user_id:
            return jsonify({'error': 'Você não tem permissão para atualizar esta loja'}), 403
            
        data = request.get_json()
        
        # Validar campos obrigatórios
        if not data.get('nome'):
            return jsonify({'error': 'O campo nome é obrigatório'}), 400
        if not data.get('numero'):
            return jsonify({'error': 'O campo numero é obrigatório'}), 400
        if not data.get('potencia_id'):
            return jsonify({'error': 'O campo potencia_id é obrigatório'}), 400
        if not data.get('rito_id'):
            return jsonify({'error': 'O campo rito_id é obrigatório'}), 400
        if not data.get('oriente_nome'):
            return jsonify({'error': 'O campo oriente_nome é obrigatório'}), 400
        if not data.get('oriente_uf'):
            return jsonify({'error': 'O campo oriente_uf é obrigatório'}), 400
        
        # Verificar se potência existe
        potencia = Potencia.query.get(data['potencia_id'])
        if not potencia:
            return jsonify({'error': 'Potência não encontrada'}), 404
        
        # Verificar se rito existe
        rito = Rito.query.get(data['rito_id'])
        if not rito:
            return jsonify({'error': 'Rito não encontrado'}), 404
        
        # Criar ou encontrar oriente
        oriente = Oriente.query.filter_by(
            nome=data['oriente_nome'],
            uf=data['oriente_uf']
        ).first()
        
        if not oriente:
            oriente = Oriente(
                nome=data['oriente_nome'],
                uf=data['oriente_uf']
            )
            db.session.add(oriente)
            db.session.flush()  # Para obter o ID do oriente
        
        # Atualizar loja
        loja.nome = data['nome']
        loja.numero = data['numero']
        loja.potencia_id = data['potencia_id']
        loja.rito_id = data['rito_id']
        loja.oriente_id = oriente.id
        
        db.session.commit()
        
        return jsonify(loja.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_loja(id):
    try:
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        loja = Loja.query.get(id)
        if not loja:
            print(f"Loja com ID {id} não encontrada")
            return jsonify({'error': 'Loja não encontrada'}), 404
            
        # Verificar se o usuário é admin ou se a loja pertence ao usuário
        if not user.is_admin and loja.user_id != user_id:
            print("Usuário não tem permissão para deletar esta loja")
            return jsonify({'error': 'Você não tem permissão para deletar esta loja'}), 403
            
        print(f"Deletando loja: {loja.to_dict()}")
        db.session.delete(loja)
        db.session.commit()
        print("Loja deletada com sucesso")
        
        return jsonify({'message': 'Loja deletada com sucesso'})
    except Exception as e:
        print(f"Erro ao deletar loja: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar loja'}), 500 