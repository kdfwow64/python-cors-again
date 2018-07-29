from functools import wraps

from flask.helpers import make_response
from flask_restful import Resource
from flask import request, jsonify
from werkzeug.security import check_password_hash
from models.user import UserModel


def requires_token():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                token = token.replace("JWT ", "")

            if not token:
                return jsonify({'error': 'Token is missing!'}), 401
            current_user = UserModel.verify_auth_token(token)
            if not current_user:
                return {'error': 'Invalid token!'}, 401

            return f(*args, **kwargs)
        return wrapped
    return wrapper


def requires_permission(*permission):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = None

            # if 'x-access-token' in request.headers:
            #     token = request.headers['x-access-token']

            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                token = token.replace("JWT ", "")

            if not token:
                return jsonify({'error': 'Token is missing!'}), 401

            #try:
                #data = jwt.decode(token, app.secret_key)
                #current_user = UserModel.find_by_username(data['username'])

            current_user = UserModel.verify_auth_token(token)
            if current_user:
                # user_roles = current_user.get_user_roles()

                #return {'message': current_user.get_user_permissions()}, 401

                current_user_permissions = current_user.get_user_permissions()
                current_user_permissions_name = [permission.name for permission in current_user_permissions]

                if not set(permission).issubset(current_user_permissions_name):
                # if permission not in user_role.get_permissions_name():
                    return {'error': "User doesn't have permission"}, 401
            else:
                return {'error': 'Invalid token!'}, 401
            #except:
                #return jsonify({'message': 'Token is invalid!'}), 401

            return f(*args, **kwargs)
        return wrapped
    return wrapper


class Login(Resource):
    def get(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = UserModel.find_by_username(auth.username)

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        #return {'user': user.json(), 'auth': auth} , 201
        if check_password_hash(user.password, auth.password):
            #token = jwt.encode({'username': user.public_id, 'password': user.password}, app.secret_key)
            token = user.generate_auth_token()

            #return jsonify({'token': token.decode('UTF-8')})
            return jsonify({'access_token': token.decode('UTF-8'), 'duration': 600})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})