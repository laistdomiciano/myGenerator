from sqlite3 import IntegrityError

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import login_required

from utils import generate_pdf
from auth import create_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Employee, ContractType, FinalContract, db

routes = Blueprint('routes', __name__)


@routes.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_jwt_token(user.id)
            session['access_token'] = access_token
            return jsonify({'token': access_token, 'user': user})
        return jsonify(success=False, error="Invalid credentials.")


@routes.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2:
            return jsonify(success=False, error="Passwords do not match.")

        hashed_password = generate_password_hash(password1, method='sha256')

        new_user = User(name=name, email=email, username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True, message=f"New user {username} successfully registered.")
        except IntegrityError:
            db.session.rollback()
            return jsonify(success=False, error="Username or email already exists.")

    return jsonify(success=False, error="Invalid request.")

@
# @routes.route('/create_contract')
# @login_required
# def create_contract():
#     contract_type = request.args.get('type')
#     # Assume you have logic to create the contract
#     # For example, generate a contract and store it in the database
#     # or generate a file for download
#
#     if contract_type in ["full-time", "part-time", "freelance"]:
#         # Create the contract logic here
#         return jsonify(success=True)
#     else:
#         return jsonify(success=False, error="Invalid contract type.")

#
# @routes.route('/contract_form', methods=['GET'])
# def contract_form():
#     contract_type = request.args.get('type')
#     if not contract_type:
#         return jsonify({'error': 'Contract type is required.'}), 400
#
#     if contract_type in ['Full-time', 'Part-time', 'Freelance']:
#         return render_template(f'{contract_type}_form.html', contract_type=contract_type)
#     else:
#         return jsonify({'error': 'Invalid contract type.'}), 400


@routes.route('/create_contract', methods=['POST'])
@login_required
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
