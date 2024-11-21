from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/casco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa e registra os Blueprints
    from app.routes import blueprints
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

    with app.app_context():
        db.create_all()

    return app
