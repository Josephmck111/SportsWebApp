from flask import request, jsonify, make_response
from bson import ObjectId
from flask import request, jsonify
from functools import wraps
import jwt
import globals

blacklist = globals.db.blacklist
users = globals.db.users 
matches = globals.db.matches

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message' : 'Token is missing'}), 401)
        try:
            data = jwt.decode(token, globals.secret_key ,algorithms="HS256")
        except:
            return make_response(jsonify({'message' : 'Token is invalid'}), 401)
        bl_token = blacklist.find_one({"token":token})
        if bl_token is not None:
            return make_response(jsonify( {'message' : 'Token has been cancelled' } ), 401)
        return func(*args, **kwargs)
    return jwt_required_wrapper


def admin_required(f):
    @wraps(f)
    def admin_function(*args, **kwargs):
        user_id = request.headers.get('UserID')
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user or not user.get("admin", False):  # Check if 'admin' is True
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return admin_function


def login_required(f):
    @wraps(f)
    def login_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return jsonify({"error": "Authentication required"}), 403
        return f(*args, **kwargs)
    return login_function