from flask import Blueprint, request, jsonify, session
from .models import User, Team, TeamMember, Turtle, Nest
from . import db
from .utils import validate_password
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# Função para criar um novo usuário
@main.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email já cadastrado."}), 400

    password = data.get('password')
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"error": message}), 400

    new_user = User(
        username=data.get('username'),
        email=email,
        password=generate_password_hash(password),
        is_leader=data.get('is_leader', False)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso!"}), 201


# Função para login do usuário
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

# Função de Login com JWT
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        token = generate_token(user.id)
        response = make_response(jsonify({"message": "Login realizado com sucesso!"}), 200)
        response.set_cookie("token", token)
        return response
    return jsonify({"error": "Credenciais inválidas"}), 401

# Logout
@main.route('/logout', methods=['POST'])
def logout_route():
    return logout()

# Função para alterar a senha do usuário autenticado
@main.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    data = request.get_json()
    new_password = data.get('new_password')

    is_valid, message = validate_password(new_password)
    if not is_valid:
        return jsonify({"error": message}), 400

    user = User.query.get(session['user_id'])
    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Senha alterada com sucesso!"}), 200

# Função para criar uma nova equipe (somente para líderes)
@main.route('/create_team', methods=['POST'])
def create_team():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    user = User.query.get(session['user_id'])
    if not user.is_leader:
        return jsonify({"error": "Acesso negado. Apenas líderes podem criar equipes."}), 403

    data = request.get_json()
    team_name = data.get('team_name')
    new_team = Team(name=team_name, leader_id=user.id)
    db.session.add(new_team)
    db.session.commit()

    return jsonify({"message": "Equipe criada com sucesso!"}), 201

# Função para adicionar um membro à equipe (somente líderes)
@main.route('/add_team_member', methods=['POST'])
def add_team_member():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    user = User.query.get(session['user_id'])
    if not user.is_leader:
        return jsonify({"error": "Acesso negado. Apenas líderes podem adicionar membros à equipe."}), 403

    data = request.get_json()
    team_id = data.get('team_id')
    member_id = data.get('member_id')
    team = Team.query.get(team_id)

    if team.leader_id != user.id:
        return jsonify({"error": "Você só pode adicionar membros a equipes que lidera."}), 403

    new_member = TeamMember(team_id=team_id, user_id=member_id)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Membro adicionado à equipe com sucesso!"}), 201

# Função para renomear uma equipe (somente para líderes)
@main.route('/rename_team', methods=['POST'])
def rename_team():
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    user = User.query.get(session['user_id'])
    if not user.is_leader:
        return jsonify({"error": "Acesso negado. Apenas líderes podem renomear equipes."}), 403

    data = request.get_json()
    team_id = data.get('team_id')
    new_name = data.get('new_name')
    team = Team.query.get(team_id)

    if team.leader_id != user.id:
        return jsonify({"error": "Você só pode renomear equipes que lidera."}), 403

    team.name = new_name
    db.session.commit()

    return jsonify({"message": "Equipe renomeada com sucesso!"}), 200


# Rota protegida com verificação de token para gerenciamento de equipes (exemplo)
@main.route('/protected_route', methods=['GET'])
def protected_route():
    token = request.cookies.get("token")
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Token inválido ou expirado"}), 401
    # Exemplo de uso do ID de usuário validado
    user = User.query.get(user_id)
    return jsonify({"message": f"Bem-vindo, {user.username}!"}), 200

# Registro de atividades para auditoria
def log_activity(action, user_id):
    log_entry = LogEntry(action=action, user_id=user_id)
    db.session.add(log_entry)
    db.session.commit()

# Função para registrar uma nova tartaruga
@main.route('/register_turtle', methods=['POST'])
def register_turtle():
    data = request.get_json()
    name = data.get('name')
    tag = data.get('tag')
    species = data.get('species')
    location = data.get('location')

    new_turtle = Turtle(name=name, tag=tag, species=species, location=location)
    db.session.add(new_turtle)
    db.session.commit()

    return jsonify({"message": "Tartaruga registrada com sucesso!"}), 201

# Função para atualizar informações de uma tartaruga
@main.route('/update_turtle', methods=['POST'])
def update_turtle():
    data = request.get_json()
    turtle_id = data.get('turtle_id')
    turtle = Turtle.query.get(turtle_id)

    if not turtle:
        return jsonify({"error": "Tartaruga não encontrada"}), 404

    turtle.name = data.get('name', turtle.name)
    turtle.tag = data.get('tag', turtle.tag)
    turtle.species = data.get('species', turtle.species)
    turtle.location = data.get('location', turtle.location)
    db.session.commit()

    return jsonify({"message": "Informações da tartaruga atualizadas com sucesso!"}), 200