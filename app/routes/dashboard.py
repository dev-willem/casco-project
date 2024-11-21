from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import Usuario, Equipe, Convite

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        flash('Você precisa fazer login primeiro!', 'warning')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(session['user_id'])
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('auth.login'))

    equipes_participantes = Equipe.query.join(Convite).filter(
        (Convite.usuario_id == usuario.id) & (Convite.status == 'aceito')
    ).all()

    equipes_lideradas = Equipe.query.filter_by(lider_id=usuario.id).all()

    return render_template('dashboard.html', usuario=usuario,
                           equipes_participantes=equipes_participantes,
                           equipes_lideradas=equipes_lideradas)
