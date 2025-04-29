import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from fastapi import HTTPException
import json
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRET_JSON = os.getenv("CLIENT_SECRET_JSON_PATH", "client_secret.json")
TOKEN_PATH = os.getenv("TOKEN_PATH", "token.pickle")

# This function manages OAuth2 and returns a Gmail API service instance
def get_gmail_service():
    creds = None
    
    # Check if token file exists
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading token: {str(e)}")
    
    # If credentials are not available or invalid, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {str(e)}")
                creds = None
        
        # If still no valid credentials, need to authenticate
        if not creds:
            # Check if client secret file exists
            if not os.path.exists(CLIENT_SECRET_JSON):
                raise HTTPException(status_code=500, detail="Gmail client secret file not found. Please set up OAuth2 credentials.")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_JSON, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(TOKEN_PATH, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"OAuth2 authentication failed: {str(e)}")
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build Gmail service: {str(e)}")

# LEGACY: Fetch recent emails from inbox only
# def fetch_recent_emails(limit=5):
#     ...

def get_label_id_by_name(label_name):
    service = get_gmail_service()
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    raise HTTPException(status_code=404, detail=f"Label '{label_name}' not found.")

def fetch_recent_emails(limit=5, label_name=None, label_id=None):
    service = get_gmail_service()
    query_params = {'userId': 'me', 'maxResults': limit}
    if label_name:
        label_id = get_label_id_by_name(label_name)
    if label_id:
        query_params['labelIds'] = [label_id]
    results = service.users().messages().list(**query_params).execute()
    messages = results.get('messages', [])
    
    if not messages:
        return []
            
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        snippet = msg_data.get('snippet', '')
        emails.append({
            'subject': subject,
            'from': sender,
            'snippet': snippet
        })
    return emails

def list_labels():
    try:
        service = get_gmail_service()
        results = service.users().labels().list(userId='me').execute()
        return results.get('labels', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing labels: {str(e)}")
