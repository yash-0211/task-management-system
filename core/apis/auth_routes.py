from flask import Blueprint, request, current_app
from core.models.user import User
from .response import APIResponse
import jwt
import datetime

auth_resource = Blueprint('auth_resource', __name__)

@auth_resource.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return APIResponse.respond({'message': 'Username and password are required', 'WWW-Authenticate': 'Basic realm="Login required!"'}, status_code=401)

    user = User.get_user_by_username(auth.get('username'))

    if not user or not user.check_password(auth.get('password')):
        return APIResponse.respond({'message': 'Wrong username or password', 'WWW-Authenticate': 'Basic realm="Login required!"'}, status_code=401)

    # Generate JWT token
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return APIResponse.respond({'token': token})

@auth_resource.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return APIResponse.respond({'message': 'Username and password are required'}, status_code=400)

    if User.get_user_by_username(username):
        return APIResponse.respond({'message': 'Username already exists'}, status_code=409)

    new_user = User(username=username)
    new_user.set_password(password)
    new_user.save()

    # Generate JWT token
    token = jwt.encode({
        'id': new_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return APIResponse.respond({'token': token})
