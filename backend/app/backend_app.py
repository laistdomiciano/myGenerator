import os
import psycopg2
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from routes import routes
from models import db, User
from flask_cors import CORS

DB_NAME = 'mygeneratordb'
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()

def create_database():
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '2206')
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

    myapp = Flask(__name__)
    CORS(myapp)

    myapp.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysupersecretkey')
    myapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        f'postgresql://postgres:2206@localhost:5432/{DB_NAME}'
    )
    myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(myapp)
    migrate.init_app(myapp, db)
    jwt.init_app(myapp)

    # Initialize LoginManager
    login_manager.init_app(myapp)
    login_manager.login_view = 'routes.login'  # Redirects to login view if not authenticated
    login_manager.user_loader(load_user)  # Loads user from the database by user_id

    myapp.register_blueprint(routes, url_prefix='/')

    with myapp.app_context():
        db.create_all()
        print('All tables created successfully!')

    return myapp

mybapp = create_app()

if __name__ == "__main__":
    mybapp.run(host="0.0.0.0", port=5002, debug=True)