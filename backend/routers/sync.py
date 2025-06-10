from fastapi import APIRouter, HTTPException, Query
from backend.services.gmail_client import fetch_recent_emails, list_labels
from backend.services.openai_client import OpenAIClient
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
openai_client = OpenAIClient()

@router.get("/emails")
def sync_emails(
    limit: int = Query(10, description="Number of emails to fetch"),
    label_name: str = Query(None, description="Gmail label name to filter emails"),
    label_id: str = Query(None, description="Gmail label ID to filter emails (overrides label_name)")
):
    try:
        emails = fetch_recent_emails(limit=limit, label_name=label_name, label_id=label_id)
        return {"status": "success", "emails": emails}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error syncing emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error syncing emails: {str(e)}")

@router.get("/labels")
def get_labels():
    try:
        labels = list_labels()
        return {"status": "success", "labels": labels}
    except Exception as e:
        logger.error(f"Error fetching labels: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching labels: {str(e)}")

@router.get("/extract-events")
def extract_events(
    limit: int = Query(10, description="Number of emails to fetch"),
    label_name: str = Query(None, description="Gmail label name to filter emails"),
    label_id: str = Query(None, description="Gmail label ID to filter emails (overrides label_name)")
):
    try:
        emails = fetch_recent_emails(limit=limit, label_name=label_name, label_id=label_id)
        all_events = []
        
        for email in emails:
            # Extract events from email content
            email_text = f"Subject: {email['subject']}\n\n{email.get('snippet', '')}"
            events = openai_client.extract_events(email_text)
            if events:
                # Add email metadata to each event
                for event in events:
                    event['source_email'] = {
                        'subject': email['subject'],
                        'from': email['from']
                    }
                all_events.extend(events)
        
        return {"status": "success", "events": all_events}
    except Exception as e:
        logger.error(f"Error extracting events: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting events: {str(e)}")
