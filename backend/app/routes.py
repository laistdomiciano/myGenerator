from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Employee, ContractType, FinalContract, db

routes = Blueprint('routes', __name__)


@routes.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required.'}), 400

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid username or password.'}), 401

        access_token = create_access_token(identity=user.id)

        user_data = {
            'username': user.username
        }

        return jsonify({'token': access_token, 'user': user_data})

    return jsonify({'message': 'Login page'}), 200


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


@routes.route('/create_employee', methods=['POST'])
@jwt_required()
def create_employee():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        position = data['position']
        department = data['department']

        if not name or not position or not department:
            return jsonify(success=False, error="Name, position, and department are required.")

        new_employee = Employee(name=name, position=position, department=department)

        try:
            db.session.add(new_employee)
            db.session.commit()
            return jsonify(success=True, message=f"New employee {name} successfully registered.")
        except IntegrityError:
            db.session.rollback()
            return jsonify(success=False, error="Employee already exists.")

    return jsonify(success=False, error="Invalid request.")


@routes.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 401

    data = request.get_json()  # Use `request.get_json()` to parse JSON data

    if not data:
        return jsonify({'error': 'No data provided.'}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password, method='sha256')

    db.session.commit()
    return jsonify({'message': 'User updated successfully.'})


@routes.route('/get_contract_type/<int:contract_id>', methods=['GET'])
@jwt_required()
def get_contract_type(contract_id):
    contract_type = ContractType.query.get(contract_id)
    if not contract_type:
        return jsonify({'error': 'Contract type not found.'}), 404

    contract_type_data = {
        'id': contract_type.id,
        'name': contract_type.name,
        'template': contract_type.template
    }

    return jsonify({'contract_type': contract_type_data}), 200


@routes.route('/employee_wo_contract/<int:employee_id>', methods=['GET'])
@jwt_required()
def employee_wo_contract(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found.'}), 404

    contract_exists = FinalContract.query.filter_by(employee_id=employee_id).first()

    if contract_exists:
        return jsonify({'error': 'Employee already has a contract.'}), 400

    return jsonify({'new_employee_id': employee.id}), 200


@routes.route('/create_contract/<int:contract_type_id>/<int:employee_id>', methods=['POST'])
@jwt_required()
def create_contract(contract_type_id, employee_id):
    data = request.get_json()

    # Ensure the JSON data is correctly formatted
    user_id = data.get('user_id')
    content = data.get('content')

    if not user_id or not content:
        return jsonify({'error': 'User ID and contract content are required.'}), 400

    # Fetch records from the database
    user = User.query.get(user_id)
    employee = Employee.query.get(employee_id)
    contract_type = ContractType.query.get(contract_type_id)

    if not user or not employee or not contract_type:
        return jsonify({'error': 'Invalid user, employee, or contract type.'}), 404

    # Create the new contract
    new_contract = FinalContract(
        user_id=user_id,
        employee_id=employee.id,
        contract_type_id=contract_type.id,
        content=content
    )

    db.session.add(new_contract)
    db.session.commit()

    return jsonify({'message': 'Contract created successfully.', 'contract_id': new_contract.id}), 201


@routes.route('/update_employee/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    pass
