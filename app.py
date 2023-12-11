from flask import Flask, make_response, session, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models.model_config import db
from game.ai.test_openai_response import TestOpenAIResponse

# Initialize Flask app and SQLAlchemy database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)
CORS(app, supports_credentials=True)
app.secret_key = "secret" # TODO: Change this to something more secure, like a randomly generated UUID

# Testing code for OpenAI response
AI = TestOpenAIResponse()

########################################################################
########################### API entry point ############################
########################################################################

# API entry point without authorization
@app.route("/", methods=["GET"])
def index():
    return make_response({"message": "Immemoria server is running."})

# API entry point with authorization
# TODO: Add different authorization levels, e.g. admin, user, etc.
# TODO: For now, this is just a placeholder
@app.route("/auth", methods=["GET"])
def auth():
    return make_response({"message": "You are authorized."})

########################################################################
############################ AI response ###############################
########################################################################

# Test endpoint for generating AI response
@app.route("/ai", methods=["POST"])
def ai_route():
    # Get prompt from request body
    prompt = request.json["prompt"]

    # Get the response from OpenAI
    response = AI.generate_response(prompt)

    # Check if response is not None and has the expected structure
    if response is not None and isinstance(response, str):
        return make_response(jsonify({"response": response}), 200)
    else:
        # Handle the case where response is None or malformed
        return make_response(jsonify({"error": "Failed to get AI response"}), 500)

########################################################################
########################## Error Handling ##############################
########################################################################

# Error handling for 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

########################################################################
############################# Run the app ##############################
########################################################################

if __name__ == "__main__":
    app.run(debug=True)