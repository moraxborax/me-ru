# ME-RU メール
## The AI Email Agent

ME-RU is an AI-powered email assistant that fetches emails from your inbox (Gmail), analyzes them using OpenAI, and extracts calendar events for you.

## Features
- Fetch recent emails via gmail api
- Analyze email content with OpenAI to identify meeting details
- Expose a simple REST API for synchronizing emails
- Future support: calendar integration, custom workflows

## Tech Stack
- **Backend:** Python, FastAPI, gmail, python-dotenv, OpenAI
- **Frontend:** Next.js (coming soon)

## Prerequisites
- Python 3.8+
- Node.js 14+

## Environment Variables
Create a `.env` file in the project root with the following:

```json
OPENAI_API_KEY=your-openai-api-key
EMAIL_ADDRESS=your-email@example.com
EMAIL_PASSWORD=your-email-password-or-app-password
```

> **Note:**
> - For Gmail, enable IMAP and use an App Password if you have 2FA enabled.
> - For Outlook.com or Microsoft 365, generate and use an App Password or Exchange credentials.

## Setup & Running

### Backend
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

### API Usage
Open the Swagger UI at `http://127.0.0.1:8000/docs` or run:
```bash
curl -X GET http://127.0.0.1:8000/sync/emails
```

## Contribution
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
MIT 


