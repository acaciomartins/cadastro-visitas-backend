import os
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def init_app(app: Flask):
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY',
        'sua-chave-secreta-aqui'
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hora
    
    jwt.init_app(app) 