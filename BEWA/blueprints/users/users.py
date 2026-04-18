import json
from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals
import string
from bson.errors import InvalidId
import os
import base64

# Create a Blueprint for user-related routes.
users_bp = Blueprint("users_bp", __name__)

# Initialize the users collection from the global database.
users = globals.db.users

# Helper function: Recursively converts ObjectId instances to strings within documents.
def convert_objectid_to_str(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, list):
                doc[key] = [convert_objectid_to_str(item) for item in value]
            elif isinstance(value, dict):
                doc[key] = convert_objectid_to_str(value)
    elif isinstance(doc, list):
        doc = [convert_objectid_to_str(item) for item in doc]
    return doc

# API endpoint: Retrieve all users with pagination.
@users_bp.route("/api/v1.0/users", methods=["GET"])
def show_all_users():
    # Set default pagination values.
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    # Retrieve paginated users from the database
    data_to_return = []
    for user in users.find().skip(page_start).limit(page_size):
        user = convert_objectid_to_str(user)
        # Decode any binary data (e.g., passwords) to strings for response.
        for key, value in user.items():
            if isinstance(value, bytes):
                user[key] = value.decode('utf-8')
        data_to_return.append(user)
    return make_response(jsonify(data_to_return), 200)

# API endpoint: Retrieve details of a specific user by their ID.
@users_bp.route("/api/v1.0/users/<string:id>", methods=["GET"])
def show_one_user(id):
    # Validate the user ID format.
    if len(id) != 24 or not all(c in string.hexdigits for c in id):
        return make_response(jsonify({"error": "Invalid user ID"}), 404)
    # Fetch the user from the database.
    user = users.find_one({'_id': ObjectId(id)})
    if user is not None:
        user = convert_objectid_to_str(user)
        # Decode any binary data (e.g., passwords) to strings for response.
        for key, value in user.items():
            if isinstance(value, bytes):
                user[key] = value.decode('utf-8')
        return make_response(jsonify(user), 200)
    else:
        return make_response(jsonify({"error": "Invalid user ID"}), 404)

# API endpoint: Count the total number of users in the database.
@users_bp.route("/api/v1.0/users/count", methods=["GET"])
def get_users_count():
    total_users = users.count_documents({})  # Count users in the database
    return jsonify({"total_count": total_users})

# API endpoint: Add a new user to the database.
@users_bp.route("/api/v1.0/users", methods=["POST"])
def add_user():
    try:
        # Debug incoming form data
        print("Form Data Received:", request.form)

        # Verify required fields and blank values
        required_fields = ["name", "username", "password", "email"]
        for field in required_fields:
            if field not in request.form or not request.form[field].strip():
                print(f"Missing or blank form data: {field}")  # Debug missing or blank field
                return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

        # Convert Password to binary for MongoDB storage
        password_binary = request.form["password"].strip().encode('utf-8')  # Convert to binary
        password_encoded = base64.b64encode(password_binary).decode('utf-8')  # Base64 encode for JSON representation

        # Admin status defaults to False if not provided
        is_admin = request.form.get("admin", "false").strip().lower() == "true"

        # Construct the new user object
        new_user = {
            "name": request.form["name"].strip(),
            "username": request.form["username"].strip(),
            "password": password_binary,  # Store binary password in MongoDB
            "email": request.form["email"].strip(),
            "admin": is_admin
        }

        # Insert the new user into MongoDB
        try:
            new_user_id = users.insert_one(new_user)
            print("New User ID from MongoDB:", new_user_id.inserted_id)
        except Exception as e:
            print("Error inserting user into MongoDB:", str(e))
            return make_response(jsonify({"error": "Failed to add user"}), 500)

        # Prepare JSON representation for response and file handling
        json_user = {
            "name": new_user["name"],
            "username": new_user["username"],
            "password": password_encoded,  # Base64 encoded password for JSON
            "email": new_user["email"],
            "admin": new_user["admin"],
            "_id": str(new_user_id.inserted_id)
        }

        # Update the JSON file
        try:
            if not os.path.exists('users.json'):
                # Create new file if it doesn't exist
                with open('users.json', 'w') as file:
                    json.dump([json_user], file, indent=4)
            else:
                # Update existing file
                with open('users.json', 'r+') as file:
                    try:
                        data = json.load(file)  # Load existing data
                    except json.JSONDecodeError:
                        data = []  # Initialize as empty list if file is corrupted
                    data.append(json_user)  # Add new user
                    file.seek(0)
                    json.dump(data, file, indent=4)  # Write updated data
        except IOError as e:
            print("I/O Error:", str(e))
            return make_response(jsonify({"error": f"Failed to update JSON file: {str(e)}"}), 500)

        # Return success response
        new_user_link = f"http://localhost:5000/api/v1.0/users/{str(new_user_id.inserted_id)}"
        print("User Successfully Added:", new_user_link)
        return make_response(jsonify({"url": new_user_link}), 201)

    except Exception as e:
        print("Critical Error in add_user:", str(e))
        return make_response(jsonify({"error": "An unexpected error occurred. Please try again."}), 500)

# API endpoint: Edit the details of an existing user.
@users_bp.route("/api/v1.0/users/<string:id>", methods=["PUT"])
def edit_user(id):
    # Validate ObjectId
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({"error": "Invalid user ID"}), 404)

    # # Check for required fields
    # if "name" not in request.form or "username" not in request.form or "email" not in request.form or "password" not in request.form:
    #     return make_response(jsonify({"error": "Missing form data"}), 400)

    required_fields = ["name", "username", "email", "password"]
    for field in required_fields:
        if field not in request.form or not request.form[field].strip():
            return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

    # Update user in database
    result = users.update_one(
        { "_id": object_id },
        {
            "$set": {
                "name": request.form['name'],
                "username": request.form['username'],
                "password": request.form['password'].encode('utf-8'),  # Convert to binary
                "email": request.form['email'],
                "admin": request.form.get("admin", "false").lower() == "true"  # Default to False if not provided
            }
        }
    )

    # Handle update result
    if result.matched_count == 1:
        edited_user_link = f"http://localhost:5000/api/v1.0/users/{id}"
        return make_response(jsonify({"url": edited_user_link}), 200)
    else:
        return make_response(jsonify({"error": "Invalid user ID"}), 404)

# API endpoint: Delete a user by their ID.
@users_bp.route("/api/v1.0/users/<string:id>", methods=["DELETE"])
def delete_user(id):
    result = users.delete_one({ "_id": ObjectId(id) })
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({ "error": "Invalid user ID" }), 404)
