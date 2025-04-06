from app import create_app, db
from app.models import User, Potencia, Rito, Grau, Sessao, Oriente

app = create_app()

with app.app_context():
    # Verificar usuário admin
    admin = User.query.filter_by(username='admin').first()
    print("\n=== Usuário Admin ===")
    if admin:
        print(f"Admin encontrado: {admin.username} (ID: {admin.id})")
        print(f"Email: {admin.email}")
        print(f"É admin: {admin.is_admin}")
    else:
        print("Admin não encontrado!")
    
    # Verificar dados iniciais
    print("\n=== Dados Iniciais ===")
    print(f"Potências: {Potencia.query.count()}")
    print(f"Ritos: {Rito.query.count()}")
    print(f"Graus: {Grau.query.count()}")
    print(f"Sessões: {Sessao.query.count()}")
    print(f"Orientés: {Oriente.query.count()}")
    
    # Listar todos os usuários
    print("\n=== Todos os Usuários ===")
    for user in User.query.all():
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Admin: {user.is_admin}") 