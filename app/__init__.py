# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
from .config import Config
from .extensions import db, migrate, jwt, init_app as init_extensions
from .routes.auth_routes import bp as auth_bp
from .routes.visita_routes import bp as visitas_bp
from .routes.sessao_routes import bp as sessoes_bp
from .routes.rito_routes import bp as ritos_bp
from .routes.grau_routes import bp as graus_bp
from .routes.potencia_routes import bp as potencias_bp
from .routes.loja_routes import bp as lojas_bp
from .routes.oriente_routes import bp as oriente_bp

def init_db(app):
    """Inicializa o banco de dados e cria o usuário admin se necessário"""
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("Tabelas criadas com sucesso!")
            
            # Verificar e criar usuário admin
            from app.models import User
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    name='Administrador',
                    email='admin@example.com',
                    password='admin123',  # Senha inicial
                    is_admin=True
                )
                admin.set_password('admin123')  # Hash da senha
                db.session.add(admin)
                db.session.commit()
                print("Usuário admin criado com sucesso!")
                
            # Verificar e criar dados iniciais se necessário
            from app.models import Potencia, Rito, Grau, Sessao, Oriente
            
            # Verificar potências
            if Potencia.query.count() == 0:
                potencias = [
                    Potencia(nome='Grande Oriente do Brasil', sigla='GOB'),
                    Potencia(nome='Grande Loja Maçônica do Brasil', sigla='GLMB'),
                    Potencia(nome='Grande Loja Maçônica do Estado de São Paulo', sigla='GLMESP')
                ]
                db.session.bulk_save_objects(potencias)
                print("Potências iniciais criadas com sucesso!")
            
            # Verificar ritos
            if Rito.query.count() == 0:
                ritos = [
                    Rito(nome='Rito Escocês Antigo e Aceito', descricao='Rito mais praticado no Brasil'),
                    Rito(nome='Rito Brasileiro', descricao='Rito criado no Brasil'),
                    Rito(nome='Rito de York', descricao='Rito praticado em algumas potências')
                ]
                db.session.bulk_save_objects(ritos)
                print("Ritos iniciais criadas com sucesso!")
            
            # Verificar graus
            if Grau.query.count() == 0:
                graus = [
                    Grau(numero=1, descricao='Aprendiz'),
                    Grau(numero=2, descricao='Companheiro'),
                    Grau(numero=3, descricao='Mestre')
                ]
                db.session.bulk_save_objects(graus)
                print("Graus iniciais criadas com sucesso!")
            
            # Verificar sessões
            if Sessao.query.count() == 0:
                sessoes = [
                    Sessao(descricao='Sessão Magna'),
                    Sessao(descricao='Sessão Branca'),
                    Sessao(descricao='Sessão de Instrução')
                ]
                db.session.bulk_save_objects(sessoes)
                print("Sessões iniciais criadas com sucesso!")
            
            # Verificar orientes
            if Oriente.query.count() == 0:
                orientes = [
                    Oriente(nome='São Paulo', uf='SP'),
                    Oriente(nome='Rio de Janeiro', uf='RJ'),
                    Oriente(nome='Minas Gerais', uf='MG')
                ]
                db.session.bulk_save_objects(orientes)
                print("Orientés iniciais criados com sucesso!")
            
            db.session.commit()
            print("Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print("Erro ao inicializar banco de dados: " + str(e))
            db.session.rollback()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar CORS - Permitir todas as origens durante o desenvolvimento
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:3002",
                "http://localhost:3003",
                "http://localhost:3004",
                "http://localhost:3005"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Inicializar extensões
    init_extensions(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(visitas_bp, url_prefix='/api/visitas')
    app.register_blueprint(sessoes_bp, url_prefix='/api/sessoes')
    app.register_blueprint(ritos_bp, url_prefix='/api/ritos')
    app.register_blueprint(graus_bp, url_prefix='/api/graus')
    app.register_blueprint(potencias_bp, url_prefix='/api/potencias')
    app.register_blueprint(lojas_bp, url_prefix='/api/lojas')
    app.register_blueprint(oriente_bp, url_prefix='/api/orientes')
    
    # Inicializar banco de dados
    init_db(app)
    
    return app 