from flask import Flask, request, redirect, session, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from models import db, User, Schedule  # Ensure these models are defined in models.py
from notion_api import get_access_token, create_database, add_schedule_to_database  # Custom Notion API integration
from openai_api import generate_schedule  # Custom OpenAI integration

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up Flask app configuration
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable unnecessary signals to improve performance

# Initialize the database
db.init_app(app)

@app.route("/")
def index():
    """
    Landing page of the app.
    """
    return "Welcome to the Notion Scheduler!"

@app.route("/Hackathon1")
def hackathon1():
    return render_template("Hackathon1.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/oauth/authorize")
def authorize():
    """
    Redirects the user to Notion's OAuth authorization page.
    """
    notion_auth_url = (
        f"https://api.notion.com/v1/oauth/authorize?"
        f"client_id={os.getenv('NOTION_CLIENT_ID')}&"
        f"redirect_uri={os.getenv('NOTION_REDIRECT_URI')}&"
        f"response_type=code"
    )
    return redirect(notion_auth_url)

@app.route("/oauth/callback")
def oauth_callback():
    """
    Handles the OAuth callback from Notion, exchanging the code for tokens.
    """
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400

    try:
        # Exchange code for access token
        tokens = get_access_token(code)
        if "access_token" not in tokens or "workspace_id" not in tokens:
            return redirect("/error")

        # Store the tokens in the database
        user = User(
            notion_access_token=tokens["access_token"],
            notion_workspace_id=tokens["workspace_id"],
        )
        db.session.add(user)
        db.session.commit()

        # Store user info in session
        session["user_id"] = user.id
        session["notion_token"] = tokens["access_token"]

        # Redirect to the hackathon planner page after successful authentication
        return redirect("/Hackathon1")
    except Exception as e:
        print(f"Error in OAuth callback: {e}")
        return redirect("/error")


@app.route("/schedule", methods=["POST"])
def create_schedule():
    """
    Creates a schedule based on user input and stores it in Notion.
    """
    # Get data from the POST request
    user_id = request.json.get("user_id")
    user_input = request.json.get("input")

    if not user_id or not user_input:
        return jsonify({"error": "User ID and input are required"}), 400

    # Fetch the user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate a schedule using OpenAI
    ai_response = generate_schedule(user_input)

    # Create a database in the user's Notion workspace
    database = create_database(user.notion_access_token)
    if "id" not in database:
        return jsonify({"error": "Failed to create Notion database"}), 500

    database_id = database["id"]

    # Add the generated schedule to the Notion database
    schedule = add_schedule_to_database(
        user.notion_access_token,
        database_id,
        "Generated Schedule",
        ai_response,
        "2024-11-24"  # Example date; replace with dynamic input if needed
    )

    return jsonify(schedule)

if __name__ == "__main__":
    with app.app_context():
        # Create all tables in the database
        db.create_all()
    # Run the Flask app
    app.run(debug=True)
