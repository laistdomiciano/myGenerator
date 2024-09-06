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

    # Relationship to FinalContract, using backref for reverse access
    final_contracts = db.relationship('FinalContract', backref='user', lazy=True)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(150))
    start_date = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    job_title = db.Column(db.String(150))
    job_responsibilities = db.Column(db.String(255))
    salary = db.Column(db.Float)
    benefits = db.Column(db.String(255))
    work_hours = db.Column(db.String(50))
    leave_days = db.Column(db.Integer)
    notice_period = db.Column(db.String(50))
    hourly_rate = db.Column(db.Float)
    number_of_hours = db.Column(db.Float)
    description_of_services = db.Column(db.Text)
    fee_amount = db.Column(db.Float)
    payment_schedule = db.Column(db.String(100))
    ownership_terms = db.Column(db.Text)
    company_representative = db.Column(db.String(200))
    client_representative = db.Column(db.String(200))
    has_contract = db.Column(db.Boolean, default=False)

    # Relationship to FinalContract, using backref for reverse access
    contracts = db.relationship("FinalContract", backref="employee", lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "employee_name": self.employee_name,
            "company_name": self.company_name,
            "start_date": self.start_date,
            "job_title": self.job_title,
            "job_responsibilities": self.job_responsibilities,
            "salary": float(self.salary),
            "benefits": self.benefits,
            "work_hours": self.work_hours,
            "leave_days": int(self.leave_days),
            "notice_period": self.notice_period,
            "hourly_rate": self.hourly_rate,
            "number_of_hours": int(self.number_of_hours),
            "description_of_services": self.description_of_services,
            "fee_amount": float(self.fee_amount),
            "payment_schedule": self.payment_schedule,
            "ownership_terms": self.ownership_terms,
            "company_representative": self.company_representative,
            "client_representative": self.client_representative,
            "has_contract": bool(self.has_contract)
        }


class ContractType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    template = db.Column(db.Text, nullable=False)

    # Relationship to FinalContract, using backref for reverse access
    final_contracts = db.relationship("FinalContract", backref="contract_type", lazy=True)


class FinalContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contract_type.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)