from datetime import datetime
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='participante')
    admin = db.Column(db.Boolean, default=False)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    lider = db.relationship('Usuario', backref='equipes')

class Convite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    equipe = db.relationship('Equipe', backref='convites')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='convites')
    status = db.Column(db.String(20), nullable=False, default='pendente')
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
