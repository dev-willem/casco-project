from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Inicializa o banco de dados
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configura banco de dados
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa e registra o blueprint de rotas
    from .routes import main
    app.register_blueprint(main)

    return app
