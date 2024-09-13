from flask_swagger_ui import get_swaggerui_blueprint
import os
import psycopg2
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes import routes
from models import db, User
from flask_cors import CORS

DB_NAME = 'mygeneratordb'
migrate = Migrate()
jwt = JWTManager()


def create_database():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('SERVER', 'mygeneratordb.cv86uy0q8cze.eu-north-1.rds.amazonaws.com'),
            port=5432,
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'Simbera22')
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE {DB_NAME}')
            print('Database created successfully!')

        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating the database: {e}")
        raise


def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    create_database()

    myapp = Flask(__name__, static_folder='static')
    CORS(myapp)

    myapp.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysupersecretkey')

    host = os.environ.get('SERVER', 'mygeneratordb.cv86uy0q8cze.eu-north-1.rds.amazonaws.com')
    user = os.environ.get('DB_USER', 'postgres')
    password = os.environ.get('DB_PASSWORD', 'Simbera22')

    myapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        f'postgresql://{user}:{password}@{host}:5432/{DB_NAME}'
    )
    myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(myapp)
    migrate.init_app(myapp, db)
    jwt.init_app(myapp)

    myapp.register_blueprint(routes, url_prefix='/')

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "EC-Generator"
        }
    )
    myapp.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with myapp.app_context():
        db.create_all()

    return myapp


myapp = create_app()


if __name__ == "__main__":
    myapp.run(host="0.0.0.0", port=5002)
