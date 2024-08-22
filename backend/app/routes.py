from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from .utils import generate_pdf
from .auth import create_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Employee, ContractType, FinalContract, db


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('routes.login'))
        except IntegrityError:
            db.session.rollback()
            return render_template('signup.html', error="Username or email already exists.")

    return render_template('signup.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_jwt_token(user.id)
            session['access_token'] = access_token
            return redirect(url_for('routes.dashboard'))
        return render_template('login.html', error="Invalid credentials.")

    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('routes.login'))

@routes.route('/dashboard')
def dashboard():
    # This should be protected; add authentication check
    return render_template('dashboard.html')

@routes.route('/contract_form', methods=['GET'])
def contract_form():
    contract_type = request.args.get('type')
    if not contract_type:
        return jsonify({'error': 'Contract type is required.'}), 400

    if contract_type in ['fulltime', 'parttime', 'freelance']:
        return render_template(f'{contract_type}_form.html', contract_type=contract_type)
    else:
        return jsonify({'error': 'Invalid contract type.'}), 400

@routes.route('/create_contract', methods=['POST'])
def create_contract():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated.'}), 401

    data = request.form
    employee_id = data.get('employee_id')
    contract_type_id = data.get('contract_type_id')
    content = data.get('content')

    new_contract = FinalContract(user_id=user_id, employee_id=employee_id, contract_type_id=contract_type_id,
                                 content=content)
    db.session.add(new_contract)
    db.session.commit()

    pdf_path = generate_pdf(content)
    return jsonify({'pdf_path': pdf_path})