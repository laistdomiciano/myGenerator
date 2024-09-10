from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import requests
import os

app = Flask(__name__, template_folder='public', static_folder='static')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = os.environ.get('FRONTEND_SECRET_KEY', 'your-frontend-secret-key')


BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:5002')

@login_manager.user_loader
def load_user(user_id):
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'username': request.form.get('username'),
            'password1': request.form.get('password1'),
            'password2': request.form.get('password2')
        }

        response = requests.post(f"{BACKEND_API_URL}/signup", json=data)
        result = response.json()

        if response.status_code == 200 and result.get('success'):
            return redirect(url_for('login'))
        else:
            error = result.get('error', 'An error occurred during signup.')
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        response = requests.post(f"{BACKEND_API_URL}/login", json=data)
        result = response.json()

        if response.status_code == 200 and 'token' in result:
            session['access_token'] = result['token']
            session['user'] = result['user']
            return redirect(url_for('dashboard'))
        else:
            error = result.get('error', 'Invalid credentials.')
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('access_token', None)
    session.pop('user', None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('user'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)



