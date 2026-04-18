from flask import Flask
from flask_cors import CORS
from blueprints.matches.matches import matches_bp
from blueprints.teams.teams import teams_bp
from blueprints.comments.comments import comments_bp
from blueprints.users.users import users_bp
from blueprints.auth.auth import auth_bp


app = Flask(__name__)
CORS(app)


app.register_blueprint(matches_bp)

app.register_blueprint(teams_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True)