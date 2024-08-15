from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Ensure `app.config.Config` exists

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app

def create_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_database()