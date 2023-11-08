from datetime import date
from app import db

class Perfil(db.Model):
    __tablename__ = 'perfil'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True)
    usuarios = db.Relationship('Usuario', backref='perfil')

    def __repr__(self):
        return f"Papel: {self.nome}"

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(20), unique=True, index=True)
    senha = db.Column(db.String(20))
    id_perfil = db.Column(db.Integer, db.ForeignKey('perfil.id'))

    def __repr__(self):
        return f"Usuário: {self.usuario}"

usuario_projeto = db.Table('usuario_projeto',
            db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
            db.Column('projeto_id', db.Integer, db.ForeignKey('projeto.id'))
            )

class Projeto(db.Model):
    __tablename__ = 'projeto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=True, index=True)
    inicio = db.Column(db.Date, default=date.today())
    participantes = db.relationship('Usuario', secondary=usuario_projeto, backref='participantes')

    def __repr__(self):
        return f"Projeto: {self.nome}"