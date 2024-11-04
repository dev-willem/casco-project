import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///casco.db'  # URL do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
