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


@routes.route('/employees_wo_contract', methods=['GET'])
@jwt_required()
def employees_wo_contract():
    employees = Employee.query.filter(Employee.has_contract.is_(False)).all()
    if not employees:
        return jsonify({'error': 'Employee not found.'}), 404
    employees_list = []
    for emp in employees:
        employees_list.append(emp.to_json())

    return jsonify(employees_list), 200


@routes.route('/create_contract/<int:contract_type_id>/<int:employee_id>', methods=['POST'])
@jwt_required()
def create_contract(contract_type_id, employee_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    # Call the employees_wo_contract function to get the list of employees without a contract
    response = employees_wo_contract()
    if response[1] != 200:  # Check if the response status is not 200 OK
        return response

    employees_list = response[0].get_json()

    # Check if the specified employee is in the list of employees without a contract
    if not any(emp['id'] == employee_id for emp in employees_list):
        return jsonify({'error': 'Employee already has a contract or does not exist.'}), 400

    # Proceed to create the contract
    contract_type = ContractType.query.get(contract_type_id)
    if not contract_type:
        return jsonify({'error': 'Invalid contract type.'}), 404

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Invalid employee ID.'}), 404

    # Validate required data fields
    required_fields = ['start_date', 'company_name', 'job_title']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required.'}), 400

    # Format the contract template with the provided data
    try:
        formatted_content = contract_type.template.format(
            Start_Date=data.get('start_date', 'TBD'),
            Company_Name=data.get('company_name', 'TBD'),
            Employee_Name=employee.name,
            Job_Title=data.get('job_title', 'TBD'),
            Job_Responsibilities=data.get('job_responsibilities', 'TBD'),
            Salary_Amount=data.get('salary_amount', 'TBD'),
            List_of_Benefits=data.get('benefits', 'TBD'),
            Work_Hours=data.get('work_hours', 'TBD'),
            Leave_Days=data.get('leave_days', 'TBD'),
            Notice_Period=data.get('notice_period', 'TBD'),
            Hourly_Rate=data.get('hourly_rate', 'TBD'),
            Number_of_Hours=data.get('number_of_hours', 'TBD'),
            Description_of_Services=data.get('description_of_services', 'TBD'),
            Fee_Amount=data.get('fee_amount', 'TBD'),
            Payment_Schedule=data.get('payment_schedule', 'TBD'),
            Ownership_Terms=data.get('ownership_terms', 'TBD')
        )
    except KeyError as e:
        return jsonify({'error': f'Missing or incorrect data for contract template: {e}'}), 400

    # Create the contract
    new_contract = FinalContract(
        user_id=user_id,
        employee_id=employee.id,
        contract_type_id=contract_type.id,
        content=formatted_content
    )

    # Mark the employee as having a contract
    employee.has_contract = True
    db.session.add(new_contract)
    db.session.commit()

    return jsonify({'message': 'Contract created successfully.', 'contract_id': new_contract.id}), 201


@routes.route('/update_employee/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    pass
