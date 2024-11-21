from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Equipe, Convite, Usuario
from app import db

equipes_bp = Blueprint('equipes', __name__)

@equipes_bp.route('/')
def index():
    if 'user_id' not in session:
        flash('Você precisa fazer login primeiro!', 'warning')
        return redirect(url_for('auth.login'))
    equipes = Equipe.query.all()
    return render_template('equipes.html', equipes=equipes)

@equipes_bp.route('/criar', methods=['GET', 'POST'])
def criar_equipe():
    if 'user_id' not in session:
        flash('Você precisa fazer login primeiro!', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nome = request.form['nome']
        equipe_existente = Equipe.query.filter_by(nome=nome).first()
        if equipe_existente:
            flash('Já existe uma equipe com esse nome!', 'danger')
            return redirect(url_for('equipes.criar_equipe'))

        nova_equipe = Equipe(nome=nome, lider_id=session['user_id'])
        db.session.add(nova_equipe)
        db.session.commit()
        flash('Equipe criada com sucesso!', 'success')
        return redirect(url_for('equipes.index'))
    return render_template('criar_equipe.html')
