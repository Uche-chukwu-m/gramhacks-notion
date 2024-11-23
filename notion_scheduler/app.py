
from flask import Flask, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from models import db, User, Schedule
from notion_api import get_access_token, create_database, add_schedule_to_database
from openai_api import generate_schedule

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

@app.route("/")
def index():
    return "Welcome to the Notion Scheduler!"

@app.route("/oauth/authorize")
def authorize():
    notion_auth_url = (
        f"https://api.notion.com/v1/oauth/authorize?"
        f"client_id={os.getenv('NOTION_CLIENT_ID')}&"
        f"redirect_uri={os.getenv('NOTION_REDIRECT_URI')}&"
        f"response_type=code"
    )
    return redirect(notion_auth_url)

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    tokens = get_access_token(code)
    user = User(
        notion_access_token=tokens["access_token"],
        notion_workspace_id=tokens["workspace_id"],
    )
    db.session.add(user)
    db.session.commit()
    return "OAuth success! Tokens stored securely."

@app.route("/schedule", methods=["POST"])
def create_schedule():
    user_id = request.json.get("user_id")
    user_input = request.json.get("input")
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    ai_response = generate_schedule(user_input)
    database_id = create_database(user.notion_access_token)["id"]
    schedule = add_schedule_to_database(user.notion_access_token, database_id, "Generated Schedule", ai_response, "2024-11-24")

    return jsonify(schedule)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
