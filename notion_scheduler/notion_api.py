import requests
import os

NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"

def get_access_token(auth_code):
    url = f"{NOTION_BASE_URL}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": os.getenv("NOTION_REDIRECT_URI"),
        "client_id": os.getenv("NOTION_CLIENT_ID"),
        "client_secret": os.getenv("NOTION_CLIENT_SECRET"),
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def create_database(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
    }
    payload = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": "AI-Generated Schedules"}}],
        "properties": {
            "Title": {"title": {}},
            "Date": {"date": {}},
            "Details": {"rich_text": {}},
        },
    }
    response = requests.post(f"{NOTION_BASE_URL}/databases", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def add_schedule_to_database(token, database_id, title, details, date):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
    }
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Date": {"date": {"start": date}},
            "Details": {"rich_text": [{"text": {"content": details}}]},
        },
    }
    response = requests.post(f"{NOTION_BASE_URL}/pages", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
