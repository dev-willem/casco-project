from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('Email já registrado!', 'danger')
            return redirect(url_for('auth.register'))
        hashed_senha = generate_password_hash(senha, method='sha256')
        novo_usuario = Usuario(username=username, email=email, senha=hashed_senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Deslogado com sucesso!', 'success')
    return redirect(url_for('auth.login'))
