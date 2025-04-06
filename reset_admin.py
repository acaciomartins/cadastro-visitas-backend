from app import create_app, db
from app.models import User, Loja, Visita
import uuid

def reset_admin():
    app = create_app()
    with app.app_context():
        # Primeiro, atualiza todas as lojas e visitas para o novo admin
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # Atualiza todas as lojas que pertencem ao admin atual
            lojas = Loja.query.filter_by(user_id=admin.id).all()
            visitas = Visita.query.filter_by(user_id=admin.id).all()
            print(f"Encontradas {len(lojas)} lojas e {len(visitas)} visitas para o admin atual")
            
            # Cria um usuário temporário para as lojas e visitas
            temp_email = f"temp_{uuid.uuid4()}@example.com"
            temp_admin = User(
                username=f"temp_{uuid.uuid4()}",
                email=temp_email,
                is_admin=True
            )
            temp_admin.set_password('temp123')
            db.session.add(temp_admin)
            db.session.commit()
            
            # Atualiza as lojas e visitas para o usuário temporário
            for loja in lojas:
                loja.user_id = temp_admin.id
            for visita in visitas:
                visita.user_id = temp_admin.id
            db.session.commit()
            
            # Remove o admin antigo
            db.session.delete(admin)
            db.session.commit()
            print("Usuário admin antigo removido com sucesso")
            
            # Cria o novo admin
            new_admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            
            # Atualiza as lojas e visitas para o novo admin
            for loja in lojas:
                loja.user_id = new_admin.id
            for visita in visitas:
                visita.user_id = new_admin.id
            db.session.commit()
            
            # Remove o admin temporário
            db.session.delete(temp_admin)
            db.session.commit()
            
            print("Novo usuário admin criado com sucesso")
            print("Username: admin")
            print("Password: admin123")
            print("Hash da senha:", new_admin.password_hash)
        else:
            # Se não existe admin, apenas cria um novo
            new_admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            print("Novo usuário admin criado com sucesso")
            print("Username: admin")
            print("Password: admin123")
            print("Hash da senha:", new_admin.password_hash)

if __name__ == '__main__':
    reset_admin() 