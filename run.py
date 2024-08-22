from backend.app.init import myapp
from flask import send_from_directory

@myapp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend/static', filename)

@myapp.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory('frontend/public', filename)

@myapp.route('/')
def root():
    return send_from_directory('frontend/public', 'home.html')

if __name__ == "__main__":
    myapp.run(debug=True)

