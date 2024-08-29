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

        # Check if the username and password are provided
        if not username or not password:
            return jsonify({'error': 'Username and password are required.'}), 400

        # Query the user by username
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid username or password.'}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user.id)

        # Serialize user object to dictionary with only username
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


# @routes.route('/create_contract', methods=['POST'])
#@jwt_required()
# def create_contract():
#     user_id = session.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'User not authenticated.'}), 401
#
#     data = request.form
#     employee_id = data.get('employee_id')
#     contract_type_id = data.get('contract_type_id')
#     content = data.get('content')

    # @routes.route('/create_contract')
    # @jwt_required()
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

    # new_contract = FinalContract(user_id=user_id, employee_id=employee_id, contract_type_id=contract_type_id,
    #                              content=content)
    # db.session.add(new_contract)
    # db.session.commit()
    #
    # pdf_path = generate_pdf(content)
    # return jsonify({'pdf_path': pdf_path})
