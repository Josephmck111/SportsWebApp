import json
import os
from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals
import string 
from bson.errors import InvalidId

# Create a Blueprint for team-related routes.
teams_bp = Blueprint("teams_bp", __name__)

# Initialize the teams collection from the global database.
teams = globals.db.teams

# Helper function: Recursively converts ObjectId to string in nested structures.
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

# API endpoint: Retrieve all teams with pagination.
@teams_bp.route("/api/v1.0/teams", methods=["GET"])
def show_all_teams():
    # Set default pagination values.
    page_num, page_size = 1, 10
    if request.args.get('pn'): # Page number from query parameters.
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'): # Page size from query parameters.
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    # Retrieve paginated teams from the database.
    data_to_return = []
    for team in teams.find().skip(page_start).limit(page_size):
        data_to_return.append(convert_objectid_to_str(team))
    return make_response(jsonify(data_to_return), 200)

# API endpoint: Retrieve details of a specific team by its ID.
@teams_bp.route("/api/v1.0/teams/<string:id>", methods=["GET"])
def show_one_team(id):
    # Validate the team ID format.
    if len(id) != 24 or not all(c in string.hexdigits for c in id):
        return make_response(jsonify({"error": "Invalid team ID"}), 404)
    # Fetch the team from the database.
    team = teams.find_one({'_id': ObjectId(id)})
    if team is not None:
        team = convert_objectid_to_str(team)
        return make_response(jsonify(team), 200)
    else:
        return make_response(jsonify({"error": "Invalid team ID"}), 404)

# API endpoint: Get the total count of teams in the database.
@teams_bp.route('/api/v1.0/teams/count', methods=['GET'])
def get_teams_count():
    total_teams = teams.count_documents({})  # Count matches in the database
    return jsonify({"total_count": total_teams})

# API endpoint: Add a new team to the database.
@teams_bp.route("/api/v1.0/teams", methods=["POST"])
def add_team():
    try:
        # Verify required fields and check for blank values
        required_fields = ["Team", "Division", "Players"]
        for field in required_fields:
            if field not in request.form or not request.form[field].strip():
                print(f"Missing or blank form data: {field}")  # Debugging message
                return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

        # Create the new team object
        new_team = {
            "Team": request.form["Team"].strip(),
            "Division": request.form["Division"].strip(),
            "Players": request.form["Players"].strip(),
            "Comments": []  # Initialize empty comments
        }

        # Insert the new team into the MongoDB database
        new_team_id = teams.insert_one(new_team)
        new_team["_id"] = str(new_team_id.inserted_id)  # Add MongoDB ID to the team document

        # Write to or update the JSON file
        try:
            if not os.path.exists('teams.json'):
                print("teams.json file not found. Creating a new file.")
                with open('teams.json', 'w') as file:
                    json.dump([new_team], file, indent=4)
            else:
                with open('teams.json', 'r+') as file:
                    try:
                        data = json.load(file)  # Load existing teams
                    except json.JSONDecodeError:
                        print("JSON decode error: Initializing new list.")  # Handle corrupted JSON
                        data = []  # Default to empty list
                    data.append(new_team)  # Add the new team
                    file.seek(0)  # Reset file pointer
                    json.dump(data, file, indent=4)  # Write updated data
        except IOError as e:
            print("I/O error during file operations:", str(e))
            return make_response(jsonify({"error": f"Failed to update JSON file: {str(e)}"}), 500)

        # Create and return the success response
        new_team_link = f"http://localhost:5000/api/v1.0/teams/{new_team['_id']}"
        return make_response(jsonify({"url": new_team_link}), 201)

    except Exception as e:
        print("Critical error in add_team:", str(e))
        return make_response(jsonify({"error": "An unexpected error occurred. Please try again."}), 500)

# API endpoint: Edit an existing team's details.
@teams_bp.route("/api/v1.0/teams/<string:id>", methods=["PUT"])
def edit_team(id):
    # Validate ObjectId
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({"error": "Invalid team ID"}), 404)

    # Check for required fields
    required_fields = ["Division", "Team"]
    for field in required_fields:
        if field not in request.form or not request.form[field].strip():
            return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

    # Update team in database
    result = teams.update_one(
        { "_id": object_id },
        {
            "$set": {
                "Team": request.form['Team'],
                "Division": request.form['Division'],
                "Players": request.form['Players']
            }
        }
    )

    # Handle update result
    if result.matched_count == 1:
        edited_team_link = f"http://localhost:5000/api/v1.0/teams/{id}"
        return make_response(jsonify({"url": edited_team_link}), 200)
    else:
        return make_response(jsonify({"error": "Invalid team ID"}), 404)

# API endpoint: Delete a team by its ID.
@teams_bp.route("/api/v1.0/teams/<string:id>", methods=["DELETE"])
def delete_team(id):
    result = teams.delete_one( { "_id" : ObjectId(id) } )
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 204)
    else:
        return make_response( jsonify( { "error" : "Invalid team ID" } ), 404)
    