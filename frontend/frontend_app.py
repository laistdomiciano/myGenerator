from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import requests
import os

app = Flask(__name__, template_folder='public', static_folder='static')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = os.environ.get('FRONTEND_SECRET_KEY', 'your-frontend-secret-key')


BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:5002')

@login_manager.user_loader
def load_user(user_id):
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'username': request.form.get('username'),
            'password1': request.form.get('password1'),
            'password2': request.form.get('password2')
        }

        response = requests.post(f"{BACKEND_API_URL}/signup", json=data)
        result = response.json()

        if response.status_code == 200 and result.get('success'):
            return redirect(url_for('login'))
        else:
            error = result.get('error', 'An error occurred during signup.')
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        response = requests.post(f"{BACKEND_API_URL}/login", json=data)
        result = response.json()

        if response.status_code == 200 and 'token' in result:
            session['access_token'] = result['token']
            session['user'] = result['user']
            return redirect(url_for('dashboard'))
        else:
            error = result.get('error', 'Invalid credentials.')
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('access_token', None)
    session.pop('user', None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session.get('user'))

@app.route('/create_employee', methods=['GET', 'POST'])
@login_required
def create_employee():
    if request.method == 'POST':
        # Collect the form data from the HTML form
        form_data = {
            'employee_name': request.form.get('employee_name'),
            'company_name': request.form.get('company_name'),
            'start_date': request.form.get('start_date'),
            'job_title': request.form.get('job_title'),
            'job_responsibilities': request.form.get('job_responsibilities'),
            'salary': request.form.get('salary'),
            'benefits': request.form.get('benefits'),
            'work_hours': request.form.get('work_hours'),
            'leave_days': request.form.get('leave_days'),
            'notice_period': request.form.get('notice_period'),
            'hourly_rate': request.form.get('hourly_rate'),
            'number_of_hours': request.form.get('number_of_hours'),
            'description_of_services': request.form.get('description_of_services'),
            'fee_amount': request.form.get('fee_amount'),
            'payment_schedule': request.form.get('payment_schedule'),
            'ownership_terms': request.form.get('ownership_terms'),
            'company_representative': request.form.get('company_representative'),
            'client_representative': request.form.get('client_representative')
        }

        # Prepare the headers, including the token for authorization
        headers = {
            'Authorization': f"Bearer {session.get('access_token')}"
        }

        # Send a POST request to the backend API to create the employee
        response = requests.post(f"{BACKEND_API_URL}/create_employee", json=form_data, headers=headers)
        result = response.json()

        if response.status_code == 201:
            # If employee creation was successful, flash a success message and redirect to dashboard
            flash(f"Employee {form_data['employee_name']} created successfully.", 'success')
            return redirect(url_for('dashboard'))
        else:
            # If there was an error, render the form again and display the error message
            error = result.get('error', 'An error occurred while creating the employee.')
            return render_template('create_employee.html', error=error)

    # If it's a GET request, simply render the create_employee form
    return render_template('create_employee.html')



@app.route('/employees_wo_contract', methods=['GET'])
@login_required
def employees_wo_contract():
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}"
    }

    response = requests.get(f"{BACKEND_API_URL}/employees_wo_contract", headers=headers)
    employees = response.json()

    if response.status_code == 200:
        return render_template('employees_wo_contract.html', employees=employees)
    else:
        error = employees.get('error', 'An error occurred while retrieving employees.')
        return render_template('employees_wo_contract.html', error=error)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password')  # Optional
        }

        headers = {
            'Authorization': f"Bearer {session.get('access_token')}"
        }

        response = requests.put(f"{BACKEND_API_URL}/update_user/{user_id}", json=form_data, headers=headers)
        result = response.json()

        if response.status_code == 200:
            flash("User information updated successfully.")
            return redirect(url_for('dashboard'))
        else:
            error = result.get('error', 'An error occurred while updating the user.')
            return render_template('update_user.html', error=error, user=session.get('user'))

    return render_template('update_user.html', user=session.get('user'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)



