from app import db

class Visita(db.Model):
    __tablename__ = 'visitas'
    
    id = db.Column(db.Integer, primary_key=True)
    data_visita = db.Column(db.Date, nullable=False)
    loja_id = db.Column(db.Integer, db.ForeignKey('lojas.id'), nullable=False)
    sessao_id = db.Column(db.Integer, db.ForeignKey('sessoes.id'), nullable=False)
    grau_id = db.Column(db.Integer, db.ForeignKey('graus.id'), nullable=False)
    rito_id = db.Column(db.Integer, db.ForeignKey('ritos.id'), nullable=False)
    potencia_id = db.Column(db.Integer, db.ForeignKey('potencias.id'), nullable=False)
    prancha_presenca = db.Column(db.Boolean, default=False)
    possui_certificado = db.Column(db.Boolean, default=False)
    registro_loja = db.Column(db.Boolean, default=False)
    data_entrega_certificado = db.Column(db.Date)
    certificado_scaniado = db.Column(db.Boolean, default=False)
    observacoes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    loja = db.relationship('Loja', backref=db.backref('visitas', lazy=True))
    sessao = db.relationship('Sessao', backref=db.backref('visitas', lazy=True))
    grau = db.relationship('Grau', backref=db.backref('visitas', lazy=True))
    rito = db.relationship('Rito', backref=db.backref('visitas', lazy=True))
    potencia = db.relationship('Potencia', backref=db.backref('visitas', lazy=True))
    user = db.relationship('User', backref=db.backref('visitas', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'data_visita': self.data_visita.isoformat() if self.data_visita else None,
            'loja_id': self.loja_id,
            'sessao_id': self.sessao_id,
            'grau_id': self.grau_id,
            'rito_id': self.rito_id,
            'potencia_id': self.potencia_id,
            'prancha_presenca': self.prancha_presenca,
            'possui_certificado': self.possui_certificado,
            'registro_loja': self.registro_loja,
            'data_entrega_certificado': self.data_entrega_certificado.isoformat() if self.data_entrega_certificado else None,
            'certificado_scaniado': self.certificado_scaniado,
            'observacoes': self.observacoes,
            'user_id': self.user_id,
            'loja': self.loja.to_dict() if self.loja else None,
            'sessao': self.sessao.to_dict() if self.sessao else None,
            'grau': self.grau.to_dict() if self.grau else None,
            'rito': self.rito.to_dict() if self.rito else None,
            'potencia': self.potencia.to_dict() if self.potencia else None
        } 