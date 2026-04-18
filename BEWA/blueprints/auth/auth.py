from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
import globals
from decorators import jwt_required
import jwt
import datetime
import bcrypt

# Create a Blueprint for authentication-related routes.
auth_bp = Blueprint("auth_bp", __name__)


# Initialize database collections for blacklist and user management.
blacklist = globals.db.blacklist
users = globals.db.users


# API endpoint: Handles user login and JWT token generation.
@auth_bp.route('/api/v1.0/login', methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        user = users.find_one( {'username':auth.username } )
        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'),user["password"]):
                token = jwt.encode( {
                    'user' : auth.username,
                    'exp' : datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30) 
                    }, globals.secret_key, algorithm="HS256")
                return make_response(
                    jsonify({'token' : token}), 200)
            else:
                return make_response(jsonify( {'message':'Bad password'}), 401)
        else:
            return make_response(jsonify( {'message':'Bad username'}), 401)
    return make_response(jsonify( {'message':'Authentication required'}), 401)


# API endpoint: Handles user logout by blacklisting their JWT token.
@auth_bp.route('/api/v1.0/logout', methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token":token})
    return make_response(jsonify( {'message' : 'Logout successful' } ), 200 )