from .auth import auth_bp
from .dashboard import dashboard_bp
from .equipes import equipes_bp
from .convites import convites_bp

# Lista de Blueprints com seus respectivos prefixos de URL
blueprints = [
    (auth_bp, '/auth'),
    (dashboard_bp, '/'),
    (equipes_bp, '/equipes'),
    (convites_bp, '/convites'),
]
