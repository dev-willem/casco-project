from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models import Convite
from app import db

convites_bp = Blueprint('convites', __name__)

@convites_bp.route('/')
def listar_convites():
    if 'user_id' not in session:
        flash('Você precisa fazer login primeiro!', 'warning')
        return redirect(url_for('auth.login'))
    convites = Convite.query.filter_by(usuario_id=session['user_id'], status='pendente').all()
    return render_template('convites.html', convites=convites)

@convites_bp.route('/responder/<int:convite_id>/<acao>', methods=['POST'])
def responder_convite(convite_id, acao):
    if 'user_id' not in session:
        flash('Você precisa fazer login primeiro!', 'warning')
        return redirect(url_for('auth.login'))
    convite = Convite.query.get(convite_id)
    if not convite or convite.usuario_id != session['user_id']:
        flash('Convite não encontrado!', 'danger')
        return redirect(url_for('convites.listar_convites'))
    if acao == 'aceitar':
        convite.status = 'aceito'
    elif acao == 'rejeitar':
        convite.status = 'rejeitado'
    db.session.commit()
    flash('Resposta enviada!', 'success')
    return redirect(url_for('convites.listar_convites'))
