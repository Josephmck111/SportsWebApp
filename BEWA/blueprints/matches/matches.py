from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required, login_required
import globals
import string
import os
import json
from werkzeug.utils import secure_filename
from flask import send_from_directory
from bson.errors import InvalidId

# Create a new Blueprint for match-related routes.
matches_bp = Blueprint("matches_bp", __name__)

# Initialize database collections.
matches = globals.db.matches
videos = globals.db.videos

# Helper function: Recursively converts ObjectId to string within nested structures (e.g., dicts/lists).
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

# API endpoint: List all matches with pagination.
@matches_bp.route("/api/v1.0/matches", methods=["GET"])
def show_all_matches():
    # Default pagination values.
    page_num, page_size = 1, 10
    if request.args.get('pn'): # Page number from query params.
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'): # Page size from query params.
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))

    # Retrieve matches from the database with pagination.
    data_to_return = []
    for match in matches.find().skip(page_start).limit(page_size):
        data_to_return.append(convert_objectid_to_str(match))
    return make_response(jsonify(data_to_return), 200)

    
# API endpoint: Retrieve details of a single match by its ID.
@matches_bp.route("/api/v1.0/matches/<string:id>", methods=["GET"])
def show_one_match(id):
    # Validate match ID format.
    if len(id) != 24 or not all(c in string.hexdigits for c in id):
        return make_response(jsonify({"error": "Invalid match ID"}), 404)
      # Fetch match from the database.
    match = matches.find_one({'_id': ObjectId(id)})
    if match is not None:
        match = convert_objectid_to_str(match)
        return make_response(jsonify(match), 200)
    else:
        return make_response(jsonify({"error": "Invalid match ID"}), 404)
    
# API endpoint: Get the total count of matches in the database.
@matches_bp.route('/api/v1.0/matches/count', methods=['GET'])
def get_matches_count():
    total_matches = matches.count_documents({})  # Count matches in the database
    return jsonify({"total_count": total_matches})

# API endpoint: Add a new match to the database.
@matches_bp.route("/api/v1.0/matches", methods=["POST"])
def add_match():
    try:
        # Verify required fields and check for blank values
        required_fields = ["HomeTeam", "AwayTeam", "Date"]
        for field in required_fields:
            if field not in request.form or not request.form[field].strip():
                print(f"Missing or blank form data: {field}")  # Debugging message
                return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

        # Create the new match object
        new_match = {
            "HomeTeam": request.form["HomeTeam"].strip(),
            "AwayTeam": request.form["AwayTeam"].strip(),
            "Date": request.form["Date"].strip(),
            "VideoURL": request.form["VideoURL"].strip(),
            "Comments": []  # Initialize empty comments
        }

        # Insert the new match into the MongoDB database
        new_match_id = matches.insert_one(new_match)
        new_match["_id"] = str(new_match_id.inserted_id)  # Add MongoDB ID to the match document

        # Write to or update the JSON file
        try:
            if not os.path.exists('matches.json'):
                print("matches.json file not found. Creating a new file.")
                with open('matches.json', 'w') as file:
                    json.dump([new_match], file, indent=4)
            else:
                with open('matches.json', 'r+') as file:
                    try:
                        data = json.load(file)  # Load existing matches
                    except json.JSONDecodeError:
                        print("JSON decode error: Initializing new list.")  # Handle corrupted JSON
                        data = []  # Default to empty list
                    data.append(new_match)  # Add the new match
                    file.seek(0)  # Reset file pointer
                    json.dump(data, file, indent=4)  # Write updated data
        except IOError as e:
            print("I/O error during file operations:", str(e))
            return make_response(jsonify({"error": f"Failed to update JSON file: {str(e)}"}), 500)

        # Create and return the success response
        new_match_link = f"http://localhost:5000/api/v1.0/matches/{new_match['_id']}"
        print("Match Successfully Added:", new_match_link)
        return make_response(jsonify({"url": new_match_link}), 201)

    except Exception as e:
        print("Critical error in add_match:", str(e))
        return make_response(jsonify({"error": "An unexpected error occurred. Please try again."}), 500)

# API endpoint: Edit details of an existing match.
@matches_bp.route("/api/v1.0/matches/<string:id>", methods=["PUT"])
def edit_match(id):
    # Validate ObjectId
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({"error": "Invalid match ID"}), 404)

    # # Check for required fields
    # if "HomeTeam" not in request.form or "AwayTeam" not in request.form or "Date" not in request.form:
    #     return make_response(jsonify({"error": "Missing form data"}), 400)
    
    required_fields = ["HomeTeam", "AwayTeam", "Date"]
    for field in required_fields:
        if field not in request.form or not request.form[field].strip():
            return make_response(jsonify({"error": f"Field '{field}' is missing or blank"}), 400)

    # Perform the update operation
    result = matches.update_one(
        { "_id": object_id },
        {
            "$set": {
                "HomeTeam": request.form['HomeTeam'],
                "AwayTeam": request.form['AwayTeam'],
                "Date": request.form['Date']
            }
        }
    )

    # Handle the result
    if result.matched_count == 1:
        edited_match_link = f"http://localhost:5000/api/v1.0/matches/{id}"
        return make_response(jsonify({"url": edited_match_link}), 200)
    else:
        return make_response(jsonify({"error": "Invalid match ID"}), 404)

# API endpoint: Delete a match by its ID.
@matches_bp.route("/api/v1.0/matches/<string:id>", methods=["DELETE"])
def delete_match(id):
    result = matches.delete_one({ "_id": ObjectId(id) })
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({ "error": "Invalid match ID" }), 404)
    
# Folder to store uploaded files.
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# API endpoint: Serve video files by filename.
@matches_bp.route('/uploads/<filename>', methods=['GET'])
def serve_video(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, mimetype='video/mp4')
    except FileNotFoundError:
        return make_response(jsonify({"error": "File not found"}), 404)
    
# API endpoint: Upload a video and associate it with a match.
@matches_bp.route("/api/v1.0/matches/<string:id>/uploads", methods=["POST"])
def upload_video(id):
    if "file" not in request.files:
        return make_response(jsonify({"error": "No file part"}), 400)
    file = request.files["file"]
    if file.filename == "":
        return make_response(jsonify({"error": "No selected file"}), 400)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        video_url = f"/uploads/{filename}"

        result = matches.update_one(
            {"_id": ObjectId(id)},  
            {"$set": {"VideoURL": video_url}}
        )

        if result.matched_count == 0:
            return make_response(jsonify({"error": "Match not found"}), 404)

        return make_response(jsonify({"message": "Video uploaded", "video_url": video_url}), 201)

# API endpoint: Retrieve a video associated with a match.
@matches_bp.route("/api/v1.0/matches/<string:id>/uploads", methods=["GET"])
def get_video_by_match_id(id):
    match = matches.find_one({"_id": ObjectId(id)})
    if not match or "VideoURL" not in match:
        return make_response(jsonify({"error": "Video not found"}), 404)

    video_url = match["VideoURL"]  
    filename = video_url.replace("/uploads/", "")  
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, mimetype="video/mp4")
    except FileNotFoundError:
        return make_response(jsonify({"error": "File not found"}), 404)


# API endpoint: Delete a video associated with a match.
@matches_bp.route("/api/v1.0/matches/<string:id>/uploads", methods=["DELETE"])
def delete_video(id):
    match = matches.find_one({"_id": ObjectId(id)})
    if not match or "VideoURL" not in match:
        return make_response(jsonify({"error": "Video not found"}), 404)

    video_url = match["VideoURL"]
    filename = video_url.replace("/uploads/", "")  
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        os.remove(file_path)
    except FileNotFoundError:
        return make_response(jsonify({"error": "File not found on server"}), 404)

    matches.update_one(
        {"_id": ObjectId(id)},
        {"$unset": {"VideoURL": ""}}
    )

    return make_response(jsonify({"message": "Video deleted successfully"}), 200)




