from app.routes.auth_routes import bp as auth_bp
from app.routes.loja_routes import bp as loja_bp
from app.routes.potencia_routes import bp as potencia_bp
from app.routes.rito_routes import bp as rito_bp
from app.routes.visita_routes import bp as visita_bp
from app.routes.sessao_routes import bp as sessao_bp
from app.routes.grau_routes import bp as grau_bp
from app.routes.oriente_routes import bp as oriente_bp

__all__ = ['auth_bp', 'loja_bp', 'potencia_bp', 'rito_bp', 'visita_bp', 'sessao_bp', 'grau_bp', 'oriente_bp'] 