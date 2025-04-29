from fastapi import APIRouter, HTTPException
from backend.services.gmail_client import fetch_recent_emails
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/emails")
def sync_emails():
    try:
        emails = fetch_recent_emails(limit=10)
        return {"status": "success", "emails": emails}
    except HTTPException as e:
        # Re-raise FastAPI HTTPExceptions
        raise e
    except Exception as e:
        logger.error(f"Error syncing emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error syncing emails: {str(e)}")

# @router.post("/calendar")
# def sync_calendar(event: dict):
#     if not account.is_authenticated:
#         return {"error": "Not authenticated with Outlook."}
#     schedule = account.schedule()
#     calendar = schedule.get_default_calendar()
#     # Placeholder: expects event dict with subject, start, end
#     new_event = calendar.new_event()
#     new_event.subject = event.get("subject", "AI Event")
#     new_event.start = event.get("start")
#     new_event.end = event.get("end")
#     new_event.save()
#     return {"message": "Event created!"}
# [IMAP MIGRATION] Calendar endpoint commented out; not supported by IMAP
