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
    name = db.Column(db.String(150))
    position = db.Column(db.String(150))
    department = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    job_title = db.Column(db.String(150))
    salary = db.Column(db.Float)
    benefits = db.Column(db.String(255))
    work_hours = db.Column(db.String(50))
    leave_days = db.Column(db.Integer)
    notice_period = db.Column(db.String(50))
    has_contract = db.Column(db.Boolean, default=False)

    # Relationship to FinalContract, using backref for reverse access
    contracts = db.relationship("FinalContract", backref="employee", lazy=True)

    def to_json(self):
        return {
            "id": int(self.id),
            "name": self.name,
            "position": self.position,
            "department": self.department,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "job_title": self.job_title,
            "salary": float(self.salary) if self.salary else None,
            "benefits": self.benefits,
            "work_hours": self.work_hours,
            "leave_days": int(self.leave_days) if self.leave_days else None,
            "notice_period": self.notice_period,
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