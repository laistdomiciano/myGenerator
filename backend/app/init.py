import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes import routes
from models import db

DB_NAME = 'mygenerator.db'
migrate = Migrate()
jwt = JWTManager()


def create_app():
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'mysupersecretkey'
    myapp.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://username:password@localhost/{DB_NAME}'

    db.init_app(myapp)

    migrate.init_app(myapp, db)
    jwt.init_app(myapp)

    myapp.register_blueprint(routes, url_prefix='/')

    create_database(myapp)

    return myapp


def create_database(myapp):
    if not os.path.exists(DB_NAME):
        with myapp.app_context():
            db.create_all()
        print('Created Database!')


myapp = create_app()

