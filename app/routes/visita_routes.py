from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Visita, User
from app import db
from datetime import datetime

bp = Blueprint('visitas', __name__, url_prefix='/api/visitas')

@bp.route('', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_visitas():
    try:
        print("Listando visitas...")
        user_id = get_jwt_identity()
        print(f"ID do usuário obtido do token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"Usuário encontrado: {user}")
        
        if not user:
            print("Usuário não encontrado")
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Se for admin, retorna todas as visitas
        if user.is_admin:
            visitas = Visita.query.all()
        else:
            # Se não for admin, retorna apenas as visitas do usuário
            visitas = Visita.query.filter_by(user_id=user_id).all()
            
        print(f"Encontradas {len(visitas)} visitas")
        return jsonify([visita.to_dict() for visita in visitas])
    except Exception as e:
        print(f"Erro ao listar visitas: {str(e)}")
        return jsonify({'error': 'Erro ao listar visitas'}), 500

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_visita(id):
    user_id = get_jwt_identity()
    visita = Visita.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(visita.to_dict())

@bp.route('', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_visita():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    visita = Visita(
        data_visita=datetime.strptime(data['data_visita'], '%Y-%m-%d').date(),
        loja_id=data['loja_id'],
        sessao_id=data['sessao_id'],
        grau_id=data['grau_id'],
        rito_id=data['rito_id'],
        potencia_id=data['potencia_id'],
        prancha_presenca=data.get('prancha_presenca', False),
        possui_certificado=data.get('possui_certificado', False),
        registro_loja=data.get('registro_loja', False),
        data_entrega_certificado=datetime.strptime(data['data_entrega_certificado'], '%Y-%m-%d').date() if data.get('data_entrega_certificado') else None,
        certificado_scaniado=data.get('certificado_scaniado', False),
        observacoes=data.get('observacoes'),
        user_id=user_id
    )
    
    db.session.add(visita)
    db.session.commit()
    
    return jsonify(visita.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_visita(id):
    user_id = get_jwt_identity()
    visita = Visita.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    visita.data_visita = datetime.strptime(data['data_visita'], '%Y-%m-%d').date()
    visita.loja_id = data['loja_id']
    visita.sessao_id = data['sessao_id']
    visita.grau_id = data['grau_id']
    visita.rito_id = data['rito_id']
    visita.potencia_id = data['potencia_id']
    visita.prancha_presenca = data.get('prancha_presenca', False)
    visita.possui_certificado = data.get('possui_certificado', False)
    visita.registro_loja = data.get('registro_loja', False)
    visita.data_entrega_certificado = datetime.strptime(data['data_entrega_certificado'], '%Y-%m-%d').date() if data.get('data_entrega_certificado') else None
    visita.certificado_scaniado = data.get('certificado_scaniado', False)
    visita.observacoes = data.get('observacoes')
    
    db.session.commit()
    return jsonify(visita.to_dict())

@bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_visita(id):
    user_id = get_jwt_identity()
    visita = Visita.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    db.session.delete(visita)
    db.session.commit()
    
    return jsonify({'message': 'Visita deletada com sucesso'}) 