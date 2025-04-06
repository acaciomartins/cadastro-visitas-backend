from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Sessao, User
from app import db

bp = Blueprint('sessoes', __name__, url_prefix='/api/sessoes')

@bp.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_sessoes():
    sessoes = Sessao.query.all()
    return jsonify([sessao.to_dict() for sessao in sessoes])

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_sessao(id):
    sessao = Sessao.query.get_or_404(id)
    return jsonify(sessao.to_dict())

@bp.route('', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_sessao():
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        return jsonify({'error': 'Apenas administradores podem criar sessões'}), 403
    
    data = request.get_json()
    sessao = Sessao(descricao=data['descricao'])
    
    db.session.add(sessao)
    db.session.commit()
    
    return jsonify(sessao.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_sessao(id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        return jsonify({'error': 'Apenas administradores podem atualizar sessões'}), 403
    
    sessao = Sessao.query.get_or_404(id)
    data = request.get_json()
    
    sessao.descricao = data.get('descricao', sessao.descricao)
    db.session.commit()
    
    return jsonify(sessao.to_dict())

@bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_sessao(id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        return jsonify({'error': 'Apenas administradores podem deletar sessões'}), 403
    
    sessao = Sessao.query.get_or_404(id)
    db.session.delete(sessao)
    db.session.commit()
    
    return jsonify({'message': 'Sessão deletada com sucesso'}) 