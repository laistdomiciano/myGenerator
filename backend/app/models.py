from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    is_active = db.Column(db.Boolean(), default=True)
    final_contracts = db.relationship('FinalContract', backref='user', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    position = db.Column(db.String(150))
    department = db.Column(db.String(100))
    contracts = db.relationship("FinalContract", backref="employee", lazy=True)

class ContractType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    template = db.Column(db.Text, nullable=False)

class FinalContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contract_type.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('final_contracts', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('final_contracts', lazy=True))
    contract_type = db.relationship('ContractType', backref=db.backref('final_contracts', lazy=True))

