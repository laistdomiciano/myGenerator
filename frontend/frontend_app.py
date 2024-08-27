from flask import request, session, Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from backend.app.models import User

myapp = Flask(__name__, template_folder='public')

# Set up the LoginManager
login_manager = LoginManager()
login_manager.init_app(myapp)
login_manager.login_view = 'login'
myapp.secret_key = 'your-secret-key-here'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@myapp.route('/')
def home():
    return render_template('home.html')

@myapp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2:
            return render_template('signup.html', error="Passwords do not match.")

        hashed_password = generate_password_hash(password1, method='sha256')

        new_user = User(name=name, email=email, username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return render_template('signup.html', error="Username or email already exists.")

    return render_template('signup.html')

@myapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_jwt_token(user.id)
            session['access_token'] = access_token
            login_user(user)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials.")

    return render_template('login.html')

@myapp.route('/logout')
def logout():
    session.pop('access_token', None)
    logout_user()
    return redirect(url_for('login'))

@myapp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    myapp.run(host="0.0.0.0", port=5001, debug=True)


