from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from .utils import generate_pdf
from .auth import create_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Employee, ContractType, FinalContract, db


routes = Blueprint('routes', __name__)


@routes.route('/contract_form', methods=['GET'])
def contract_form():
    contract_type = request.args.get('type')
    if not contract_type:
        return jsonify({'error': 'Contract type is required.'}), 400

    if contract_type in ['Full-time', 'Part-time', 'Freelance']:
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