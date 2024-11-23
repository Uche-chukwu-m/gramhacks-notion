from flask import Flask, redirect, request, session, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set the secret key to manage sessions
app.secret_key = os.urandom(24)

# Notion OAuth credentials from your .env file
NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
NOTION_REDIRECT_URI = os.getenv("http://localhost:5000/oauth/callback")  # Redirect URI after user logs in

# Step 1: Redirect the user to Notion's OAuth page for login
@app.route('/login')
def login():
    authorization_url = (
        f"https://api.notion.com/v1/oauth/authorize?"
        f"client_id={NOTION_CLIENT_ID}&"
        f"redirect_uri={NOTION_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=read write"
    )
    return redirect(authorization_url)

# Step 2: Handle Notion's OAuth callback, get the code, and exchange it for an access token
@app.route('/callback')
def callback():
    # Step 2.1: Get the authorization code from the request URL
    code = request.args.get('code')

    # Step 2.2: Use the authorization code to request an access token from Notion
    token_url = "https://api.notion.com/v1/oauth/token"
    headers = {
        "Content-Type": "application/json"
    }

    # Prepare the data for token exchange
    data = {
        "client_id": NOTION_CLIENT_ID,
        "client_secret": NOTION_CLIENT_SECRET,
        "code": code,
        "redirect_uri": NOTION_REDIRECT_URI
    }

    # Step 2.3: Send the request to Notion to exchange the code for an access token
    response = requests.post(token_url, json=data, headers=headers)
    
    if response.status_code == 200:
        # Step 2.4: Store the access token in session for later use
        access_token = response.json().get("access_token")
        session['access_token'] = access_token
        return "Authentication successful! You can now use the app."
    else:
        return "Authentication failed! Please try again.", 400

if __name__ == '__main__':
    app.run(debug=True)
