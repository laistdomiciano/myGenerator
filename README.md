# Employment Contract Generator API

## Overview
This is a Flask-based API that allows users to generate employment contracts. Users can choose from three types of contracts: Full-Time Employment, Part-Time Employment, and Freelance Contract. The application uses JWT for authentication and PostgreSQL for data storage.

## Features
- User registration and authentication
- Three types of contract templates
- Generate contracts based on user input
- Input validation and sanitization
- Secure endpoints with JWT
- Deployment configuration for Vercel/Render
- Unit testing with pytest
- API documentation with Swagger

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/contract-generator.git
    cd contract-generator
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```bash
    cp .env.example .env
    ```
   Update `.env` with your configuration.

5. Run the application:
    ```bash
    flask run
    ```

## Endpoints

- `/auth/register` - Register a new user
- `/auth/login` - Login and receive a JWT
- `/contract/generate` - Generate a contract based on selected type and user input (Authenticated)

## Deployment

To deploy the application to Vercel or Render, follow the respective platform's deployment instructions. Ensure to set the environment variables on the deployment platform.

## Testing

Run unit tests using pytest:
```bash
pytest


//////
Explanation of Each File and Directory
app/
__init__.py: Initializes the Flask application, sets up extensions like SQLAlchemy, Migrate, and JWT, and registers the blueprint for routes.
models.py: Defines the database models (User, Employee, ContractType).
routes.py: Contains the route definitions for the API endpoints.
config.py: Configuration file for the application, including database URI and secret keys.
utils.py: Utility functions, such as input sanitization.
migrations/
Directory for database migration files managed by Flask-Migrate.
tests/
test_app.py: Contains unit tests for the application.
static/
swagger.json: Swagger documentation file for API documentation.
seed.py
Script to seed the database with initial data (users, employees, contract types).
run.py
Entry point to run the Flask application.
requirements.txt
Lists the Python dependencies required for the project.
Procfile
Specifies the commands that are executed by the app on the platform (for deployment purposes).
.env
Environment variables file containing sensitive information like database URI and secret keys.
.gitignore
Specifies files and directories that should be ignored by Git (e.g., venv/, .env, __pycache__/).


Project Directories Strucure:

/employment_contract_generator
├── backend/
│   ├── app/     
│   │   ├── auth.py             
│   │   ├── config.py  
│   │   ├── init.py     
│   │   ├── models.py           
│   │   ├── routes.py                 
│   │   ├── utils.py            
│   ├── migrations/             
│   ├── tests/                  
│   ├── .env                           
│   ├── .pylintrc     
│   ├── requirements.txt           
│   └── wsgi.py                 
├── frontend/
│   ├── static
│   │   ├── home.png          
│   │   ├── script.js 
│   │   ├── styles.css                      
│   ├── public/  
│   │   ├── dashboard.html    
│   │   ├── freelance.html       
│   │   ├── full-time.html
│   │   ├── home.html     
│   │   ├── login.html
│   │   ├── part-time.html
│   │   ├── signup.html
├── venv/
├── .gitignore
└── README.md  
