from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def create_jwt_token(user_id):
    return create_access_token(identity=user_id)