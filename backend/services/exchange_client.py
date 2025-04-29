import os
from exchangelib import Credentials, Account, DELEGATE
from dotenv import load_dotenv

# Only needed in main entry, but safe to call here
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def fetch_recent_emails(limit=5):
    creds = Credentials(EMAIL_ADDRESS, EMAIL_PASSWORD)
    account = Account(EMAIL_ADDRESS, credentials=creds, autodiscover=True, access_type=DELEGATE)
    emails = []
    for item in account.inbox.all().order_by('-datetime_received')[:limit]:
        emails.append({
            "subject": item.subject,
            "from": str(item.sender.email_address) if item.sender else None,
            "body": item.text_body[:500] if item.text_body else "",
            "received": str(item.datetime_received)
        })
    return emails
