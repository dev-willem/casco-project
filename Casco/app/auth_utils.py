import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from .models import User
from . import db
from werkzeug.security import check_password_hash

# Secret Key para JWT
SECRET_KEY = "sua_chave_secreta_aqui"

def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"user_id": user_id, "exp": expiration}, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def logout():
    response = jsonify({"message": "Logout efetuado com sucesso!"})
    response.delete_cookie("token")
    return response
