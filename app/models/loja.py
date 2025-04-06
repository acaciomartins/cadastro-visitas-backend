from app.extensions import db

class Loja(db.Model):
    __tablename__ = 'lojas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    potencia_id = db.Column(db.Integer, db.ForeignKey('potencias.id'), nullable=False)
    rito_id = db.Column(db.Integer, db.ForeignKey('ritos.id'), nullable=False)
    oriente_id = db.Column(db.Integer, db.ForeignKey('orientes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    potencia = db.relationship('Potencia', backref=db.backref('lojas', lazy=True))
    rito = db.relationship('Rito', backref=db.backref('lojas', lazy=True))
    oriente = db.relationship('Oriente', backref=db.backref('lojas', lazy=True))
    user = db.relationship('User', backref=db.backref('lojas', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'numero': self.numero,
            'potencia_id': self.potencia_id,
            'rito_id': self.rito_id,
            'oriente_id': self.oriente_id,
            'user_id': self.user_id,
            'potencia': self.potencia.to_dict() if self.potencia else None,
            'rito': self.rito.to_dict() if self.rito else None,
            'oriente': self.oriente.to_dict() if self.oriente else None
        } 