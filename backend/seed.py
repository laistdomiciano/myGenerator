from datetime import datetime
from .backend_app import create_app, db
from .models import User, Employee, ContractType, FinalContract


def seed():
    app = create_app()
    with app.app_context():
        if not ContractType.query.all():
            contract_types = [
                {
                    'name': 'Full-Time',
                    'template': """
             FULL-TIME EMPLOYMENT CONTRACT

             This Full-Time Employment Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Employer") and [Employee Name] ("Employee").

             Position
             Employer agrees to employ Employee as [Job Title]. Employee's duties and responsibilities will include [Job Responsibilities].

             Compensation
             Employer will pay Employee a salary of [Salary Amount] per year, payable in accordance with the company's standard payroll schedule.

             Benefits
             Employee will be entitled to participate in the company's benefits plans, including [List of Benefits].

             Work Hours
             Employee is expected to work [Work Hours] hours per week.

             Leave Policy
             Employee will be entitled to [Leave Days] days of paid leave per year.

             Termination
             This Contract may be terminated by either party upon [Notice Period] notice.

             Confidentiality
             Employee agrees to keep all company information confidential.

             Signed,
             [Company Representative]
             [Employee Name]

             """
                },
                {
                    'name': 'Part-Time',
                    'template': """
             PART-TIME EMPLOYMENT CONTRACT

             This Part-Time Employment Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Employer") and [Employee Name] ("Employee").

             Position
             Employer agrees to employ Employee as [Job Title] on a part-time basis. Employee's duties and responsibilities will include [Job Responsibilities].

             Compensation
             Employer will pay Employee at a rate of [Hourly Rate] per hour, payable in accordance with the company's standard payroll schedule.

             Hours of Work
             Employee is expected to work [Number of Hours] hours per week.

             Benefits
             Employee will be entitled to [List of Benefits] on a pro-rated basis.

             Leave Policy
             Employee will be entitled to [Leave Days] days of paid leave per year on a pro-rated basis.

             Termination
             This Contract may be terminated by either party upon [Notice Period] notice.

             Confidentiality
             Employee agrees to keep all company information confidential.

             Signed,
             [Company Representative]
             [Employee Name]
             """
                },
                {
                    'name': 'Freelance',
                    'template': """
             FREELANCE EMPLOYMENT CONTRACT

             This Freelance Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Client") and [Freelancer Name] ("Freelancer").

             Services
             Freelancer agrees to perform the following services for Client: [Description of Services].

             Compensation
             Client will pay Freelancer a fee of [Fee Amount], payable upon completion of the services or as otherwise agreed upon by the parties.

             Payment Schedule
             Payment will be made according to the following schedule: [Payment Schedule].

             Independent Contractor
             Freelancer is an independent contractor and not an employee of Client.

             Confidentiality
             Freelancer agrees to keep all client information confidential.

             Intellectual Property
             All intellectual property developed during the project will belong to [Ownership Terms].

             Termination
             This Contract may be terminated by either party upon [Notice Period] notice.

             Signed,
             [Client Representative]
             [Freelancer Name]
             """
                }
            ]

            for ct in contract_types:
                contract_type = ContractType(name=ct['name'], template=ct['template'])
                db.session.add(contract_type)

            db.session.commit()
            print("Database seeded with initial contract types.")

        # Seed initial users
        if not User.query.all():
            user1 = User(name='John Doe', email='john@example.com', username='johndoe', password='hashed_password')
            user2 = User(name='Jane Smith', email='jane@example.com', username='janesmith', password='hashed_password')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            print("Database seeded with initial users.")

        # Seed initial employees
        if not Employee.query.all():
            employee1 = Employee(name='Alice Brown', position='Software Engineer', department='Engineering')
            employee2 = Employee(name='Bob Johnson', position='Product Manager', department='Product')
            db.session.add(employee1)
            db.session.add(employee2)
            db.session.commit()
            print("Database seeded with initial employees.")

        # Seed initial final contracts
        if not FinalContract.query.all():
            user1 = User.query.filter_by(username='johndoe').first()
            user2 = User.query.filter_by(username='janesmith').first()
            employee1 = Employee.query.filter_by(name='Alice Brown').first()
            employee2 = Employee.query.filter_by(name='Bob Johnson').first()
            contract_type1 = ContractType.query.filter_by(name='Full-Time').first()
            contract_type2 = ContractType.query.filter_by(name='Part-Time').first()

            final_contract1 = FinalContract(
                user_id=user1.id,
                employee_id=employee1.id,
                contract_type_id=contract_type1.id,
                content=contract_type1.template.replace('[Employee Name]', employee1.name).replace('[Company Name]', 'TechCorp'),
                created_at=datetime.utcnow()
            )

            final_contract2 = FinalContract(
                user_id=user2.id,
                employee_id=employee2.id,
                contract_type_id=contract_type2.id,
                content=contract_type2.template.replace('[Employee Name]', employee2.name).replace('[Company Name]', 'InnovateX'),
                created_at=datetime.utcnow()
            )

            db.session.add(final_contract1)
            db.session.add(final_contract2)
            db.session.commit()
            print("Database seeded with initial final contracts.")


if __name__ == '__main__':
    seed()



# contract_types = [
#      {
#          'name': 'Full-Time',
#          'template': """
#              FULL-TIME EMPLOYMENT CONTRACT
#
#              This Full-Time Employment Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Employer") and [Employee Name] ("Employee").
#
#              Position
#              Employer agrees to employ Employee as [Job Title]. Employee's duties and responsibilities will include [Job Responsibilities].
#
#              Compensation
#              Employer will pay Employee a salary of [Salary Amount] per year, payable in accordance with the company's standard payroll schedule.
#
#              Benefits
#              Employee will be entitled to participate in the company's benefits plans, including [List of Benefits].
#
#              Work Hours
#              Employee is expected to work [Work Hours] hours per week.
#
#              Leave Policy
#              Employee will be entitled to [Leave Days] days of paid leave per year.
#
#              Termination
#              This Contract may be terminated by either party upon [Notice Period] notice.
#
#              Confidentiality
#              Employee agrees to keep all company information confidential.
#
#              Signed,
#              [Company Representative]
#              [Employee Name]
#
#              """
#      },
#      {
#          'name': 'Part-Time',
#          'template': """
#              PART-TIME EMPLOYMENT CONTRACT
#
#              This Part-Time Employment Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Employer") and [Employee Name] ("Employee").
#
#              Position
#              Employer agrees to employ Employee as [Job Title] on a part-time basis. Employee's duties and responsibilities will include [Job Responsibilities].
#
#              Compensation
#              Employer will pay Employee at a rate of [Hourly Rate] per hour, payable in accordance with the company's standard payroll schedule.
#
#              Hours of Work
#              Employee is expected to work [Number of Hours] hours per week.
#
#              Benefits
#              Employee will be entitled to [List of Benefits] on a pro-rated basis.
#
#              Leave Policy
#              Employee will be entitled to [Leave Days] days of paid leave per year on a pro-rated basis.
#
#              Termination
#              This Contract may be terminated by either party upon [Notice Period] notice.
#
#              Confidentiality
#              Employee agrees to keep all company information confidential.
#
#              Signed,
#              [Company Representative]
#              [Employee Name]
#              """
#      },
#      {
#          'name': 'Freelance',
#          'template': """
#              FREELANCE EMPLOYMENT CONTRACT
#
#              This Freelance Contract ("Contract") is made effective as of [Start Date], by and between [Company Name] ("Client") and [Freelancer Name] ("Freelancer").
#
#              Services
#              Freelancer agrees to perform the following services for Client: [Description of Services].
#
#              Compensation
#              Client will pay Freelancer a fee of [Fee Amount], payable upon completion of the services or as otherwise agreed upon by the parties.
#
#              Payment Schedule
#              Payment will be made according to the following schedule: [Payment Schedule].
#
#              Independent Contractor
#              Freelancer is an independent contractor and not an employee of Client.
#
#              Confidentiality
#              Freelancer agrees to keep all client information confidential.
#
#              Intellectual Property
#              All intellectual property developed during the project will belong to [Ownership Terms].
#
#              Termination
#              This Contract may be terminated by either party upon [Notice Period] notice.
#
#              Signed,
#              [Client Representative]
#              [Freelancer Name]
#              """
#      }
#  ]


