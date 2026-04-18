from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals
import string

# Create a new Blueprint for comments functionality.
comments_bp = Blueprint("comments_bp", __name__)

# Initialize database collections.
matches = globals.db.matches
teams = globals.db.teams
users = globals.db.users


# Helper function: Converts ObjectId instances to strings within nested documents and lists.
def convert_objectid_to_str(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value) # Convert ObjectId to string.
            elif isinstance(value, list):
                doc[key] = [convert_objectid_to_str(item) for item in value] # Recursively handle lists.
            elif isinstance(value, dict):
                doc[key] = convert_objectid_to_str(value) # Recursively handle nested dictionaries.
    elif isinstance(doc, list):
        doc = [convert_objectid_to_str(item) for item in doc] # Handle root-level lists.
    return doc
    

# API endpoint: Add a new comment to a specific match.
@comments_bp.route("/api/v1.0/matches/<string:id>/comments", methods=["POST"])
def add_new_comment_to_match(id):
    # Validate the format of the match ID.
    if len(id) != 24 or not all(c in string.hexdigits for c in id):
        return make_response(jsonify({"error": "Invalid match ID"}), 400)
    
    # Ensure required fields are present in the request.
    required_fields = ["username", "text"]
    for field in required_fields:
        if field not in request.form:
            return make_response(jsonify({"error": f"Missing form data: {field}"}), 400)
    
    # Create a new comment object with a unique ObjectId.
    new_comment = {
        "_id": ObjectId(),
        "username": request.form["username"],
        "text": request.form["text"],
    }
    # Add the new comment to the "Comments" array in the match document.
    matches.update_one(
        { "_id": ObjectId(id) },
        { "$push": { "Comments": new_comment } }
    )
    # Generate a URL linking to the newly created comment.
    new_comment_link = f"http://localhost:5000/api/v1.0/matches/{id}/comments/{str(new_comment['_id'])}"
    return make_response(jsonify({"url": new_comment_link}), 201)


# API endpoint: Fetch all comments for a specific match.
@comments_bp.route("/api/v1.0/matches/<string:id>/comments", methods=["GET"])
def fetch_all_comments_for_match(id):
    # Validate the format of the match ID.
    if len(id) != 24 or not all(c in string.hexdigits for c in id):
        return make_response(jsonify({"error": "Invalid match ID"}), 400)
    
    # Initialize the response list for comments.
    data_to_return = []
    # Query the database to fetch the match document's "Comments" array.
    match = matches.find_one(
        { "_id": ObjectId(id) },
        { "Comments": 1, "_id": 0 }
    )
    # If comments are found, format and return them.
    if match and "Comments" in match:
        for comment in match["Comments"]:
            comment["_id"] = str(comment["_id"]) # Convert ObjectId to string for the comment ID.
            data_to_return.append(comment)
        return make_response(jsonify(data_to_return), 200)
    else:
        return make_response(jsonify({"error": "Invalid match ID or no comments found"}), 404)


# API endpoint: Fetch a specific comment for a specific match.
@comments_bp.route("/api/v1.0/matches/<string:id>/comments/<string:commentID>", methods=["GET"])
def fetch_one_comment_for_match(id, commentID):
    # Validate the format of the match and comment IDs.
    if (len(id) != 24 or not all(c in string.hexdigits for c in id) or
        len(commentID) != 24 or not all(c in string.hexdigits for c in commentID)):
        return make_response(jsonify({"error": "Invalid match ID or comment ID"}), 400)

    # Query the database for the specific comment within the match document.
    match = matches.find_one(
        { "Comments._id": ObjectId(commentID) },
        { "_id": 0, "Comments.$": 1 }
    )
    if match is None:
        return make_response(jsonify({"error": "Invalid match ID or comment ID"}), 404)
    
    # Convert the comment's ObjectId to a string before returning the response.
    match['Comments'][0]['_id'] = str(match['Comments'][0]['_id'])
    return make_response(jsonify(match['Comments'][0]), 200)


# API endpoint: Delete a specific comment from a specific match.
@comments_bp.route("/api/v1.0/matches/<string:id>/comments/<string:commentID>", methods=["DELETE"])
def delete_comment_for_match(id, commentID):
    # Validate the format of the match and comment IDs.
    if (len(id) != 24 or not all(c in string.hexdigits for c in id) or
        len(commentID) != 24 or not all(c in string.hexdigits for c in commentID)):
        return make_response(jsonify({"error": "Invalid match ID or comment ID"}), 400)

    # Use the `$pull` operator to remove the specified comment from the match document.
    result = matches.update_one(
        { "_id": ObjectId(id) },
        { "$pull": { "Comments": { "_id": ObjectId(commentID) } } }
    )

    # Check if the comment was successfully deleted
    if result.modified_count == 1:
        return make_response(jsonify({}), 204) # Successful deletion, no content returned.
    else:
        return make_response(jsonify({"error": "Invalid match ID or comment ID"}), 404)



