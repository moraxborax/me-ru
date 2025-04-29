import os
from imapclient import IMAPClient
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST", "outlook.office365.com")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def fetch_recent_emails(limit=5):
    with IMAPClient(IMAP_HOST) as client:
        client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        client.select_folder('INBOX')
        messages = client.search(['NOT', 'DELETED'])
        messages = messages[-limit:]
        response = client.fetch(messages, ['ENVELOPE', 'RFC822.TEXT'])
        emails = []
        for msgid, data in response.items():
            envelope = data[b'ENVELOPE']
            subject = envelope.subject.decode() if envelope.subject else ""
            from_addr = envelope.from_[0].mailbox.decode() + "@" + envelope.from_[0].host.decode()
            body = data[b'RFC822.TEXT'].decode(errors='ignore')
            emails.append({
                "subject": subject,
                "from": from_addr,
                "body": body,
            })
        return emails
