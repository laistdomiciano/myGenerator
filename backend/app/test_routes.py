from conftest import client
import json


def login_user(client):
    data = {"username": "other.person", "password": "1234"}
    response = client.post('/login', content_type='application/json', data=json.dumps(data))

    assert response.status_code == 200
    return response


def test_login_route(client):
    response = login_user(client)

    assert response.status_code == 200


def test_signup(client):
    data = {'name': 'John Doe', 'email': 'john@example.com', 'username': 'johndoe', 'password1': 'password123',
            'password2': 'password123'}
    response = client.post('/signup', content_type='application/json', data=json.dumps(data))

    assert response.status_code == 200


def test_create_employee(client):
    login_data = login_user(client)
    response_dict = json.loads(login_data.data.decode())
    token = response_dict.get('token')

    employee_data = {
        "employee_name": "Jane Doe",
        "company_name": "Acme Inc.",
        "start_date": "2023-01-01",
        "job_title": "Software Engineer",
        "job_responsibilities": "Develop software",
        "salary": "90000",
        "benefits": "Health insurance, Dental",
        "work_hours": 40,
        "leave_days": 30,
        "notice_period": "2 months",
        "hourly_rate": 50,
        "number_of_hours": 160,
        "description_of_services": "Software development services",
        "fee_amount": 10000,
        "payment_schedule": "Monthly",
        "ownership_terms": "Company retains IP rights",
        "company_representative": "Alice Smith",
        "client_representative": "Bob Johnson"
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post('/create_employee', content_type='application/json',
                           headers=headers, data=json.dumps(employee_data))

    assert response.status_code == 201


def test_update_user(client):
    login_data = login_user(client)
    response_dict = json.loads(login_data.data.decode())
    token = response_dict.get('token')

    update_data = {
        "name": "John Updated",
        "email": "johnupdated@example.com",
        "password": "newpassword123"
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f'/update_user/1', content_type='application/json',
                          headers=headers, data=json.dumps(update_data))

    assert response.status_code == 200


def test_get_contract_type(client):
    login_data = login_user(client)
    response_dict = json.loads(login_data.text)
    token = response_dict.get('token')

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get('/get_contract_type/1', content_type='application/json', headers=headers)

    assert response.status_code == 200


def test_employees_wo_contract(client):
    login_data = login_user(client)
    response_dict = json.loads(login_data.text)
    token = response_dict.get('token')
    print(token)

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get('/employees_wo_contract', content_type='application/json', headers=headers)

    assert response.status_code == 200


def test_create_contract(client):
    login_data = login_user(client)
    response_dict = json.loads(login_data.data.decode())
    token = response_dict.get('token')

    contract_type_id = 1
    employee_id = 1

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f'/create_contract/1/1', headers=headers)

    assert response.status_code == 201
