from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Employee, ContractType, FinalContract, db
from utils import generate_pdf, upload_to_s3
import os
import uuid

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
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

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
    data = request.get_json()

    required_fields = ['employee_name', 'company_name', 'start_date', 'job_title', 'job_responsibilities',
        'salary', 'benefits', 'work_hours', 'leave_days', 'notice_period', 'hourly_rate', 'number_of_hours',
        'description_of_services', 'fee_amount', 'payment_schedule', 'ownership_terms', 'company_representative', 'client_representative'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify(success=False, error=f"Missing required field: {field}."), 400

    # Extract data
    try:
        new_employee = Employee(
            employee_name=data['employee_name'],
            company_name=data['company_name'],
            start_date=data['start_date'],
            job_title=data['job_title'],
            job_responsibilities=data['job_responsibilities'],
            salary=data['salary'],
            benefits=data['benefits'],
            work_hours=data['work_hours'],
            leave_days=data['leave_days'],
            notice_period=data['notice_period'],
            hourly_rate=data['hourly_rate'],
            number_of_hours=data['number_of_hours'],
            description_of_services=data['description_of_services'],
            fee_amount=data['fee_amount'],
            payment_schedule=data['payment_schedule'],
            ownership_terms=data['ownership_terms'],
            company_representative=data['company_representative'],
            client_representative=data['client_representative'],
            has_contract=data.get('has_contract', False)
        )

        db.session.add(new_employee)
        db.session.commit()
        return jsonify(success=True, message=f"New employee {data['employee_name']} successfully registered."), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify(success=False, error="Employee with this ID or unique fields already exists."), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500


@routes.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 401

    data = request.get_json()

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
    user_id = get_jwt_identity()  # Get the user_id from the JWT

    contract_type = ContractType.query.get(contract_type_id)
    if not contract_type:
        return jsonify({'error': 'Invalid contract type.'}), 404

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Invalid employee ID.'}), 404
    print(employee.employee_name)

    try:
        formatted_content = contract_type.template \
            .replace("{Employee Name}", employee.employee_name) \
            .replace("{Start Date}", employee.start_date) \
            .replace("{Company Name}", employee.company_name) \
            .replace("{Job Title}", employee.job_title) \
            .replace("{Job Responsibilities}", employee.job_responsibilities) \
            .replace("{Salary Amount}", str(employee.salary)) \
            .replace("{List of Benefits}", employee.benefits) \
            .replace("{Work Hours}", str(employee.work_hours)) \
            .replace("{Leave Days}", str(employee.leave_days)) \
            .replace("{Notice Period}", employee.notice_period) \
            .replace("{Hourly Rate}", str(employee.hourly_rate)) \
            .replace("{Number of Hours}", str(employee.number_of_hours)) \
            .replace("{Description of Services}", employee.description_of_services) \
            .replace("{Fee Amount}", str(employee.fee_amount)) \
            .replace("{Payment Schedule}", employee.payment_schedule) \
            .replace("{Ownership Terms}", employee.ownership_terms) \
            .replace("{Company Representative}", employee.company_representative) \
            .replace("{Client Representative}", employee.client_representative)

    except KeyError as e:
        return jsonify({'error': f'Missing or incorrect data for contract template: {e}'}), 400

    # Generate PDF
    pdf_path, pdf_filename = generate_pdf(formatted_content, uuid.uuid4(), employee.employee_name)

    # Upload PDF to S3
    s3_url = upload_to_s3(pdf_path, pdf_filename)

    # Create the contract object, now with the user_id
    new_contract = FinalContract(
        user_id=user_id,  # Pass the user_id here
        employee_id=employee.id,
        contract_type_id=contract_type.id,
        content=s3_url
    )

    employee.has_contract = True
    db.session.add(new_contract)
    db.session.commit()

    # Cleanup temporary file
    os.remove(pdf_path)

    return jsonify(
        {'message': 'Contract created successfully.', 'contract_id': new_contract.id, 'pdf_url': s3_url}), 201


@routes.route('/update_employee/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    pass

