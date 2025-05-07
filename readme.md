# ME-RU メール
## The AI Email Agent

[![GitHub stars](https://img.shields.io/github/stars/moraxborax/me-ru?style=social)](https://github.com/moraxborax/me-ru)
[![GitHub forks](https://img.shields.io/github/forks/moraxborax/me-ru?style=social)](https://github.com/moraxborax/me-ru)
[![GitHub watchers](https://img.shields.io/github/watchers/moraxborax/me-ru?style=social)](https://github.com/moraxborax/me-ru)

ME-RU is an AI-powered email assistant that fetches emails from your Gmail inbox, analyzes them using OpenAI, and extracts calendar events for you. Built with modern Python and the power of GPT models, it helps you stay on top of your email-based scheduling.

## Features
- OAuth2 authentication with Gmail API for secure email access
- Fetch and analyze recent emails from your Gmail inbox
- Smart meeting detail extraction powered by OpenAI
- RESTful API endpoints for email synchronization and analysis
- Swagger UI documentation for easy API testing

## Tech Stack
### Backend
- **Framework:** FastAPI
- **Email Integration:** Gmail API (google-auth, google-api-python-client)
- **AI Processing:** OpenAI API
- **Other Dependencies:** Pydantic, python-dotenv, uvicorn

### Frontend
- **Framework:** Next.js
- **UI Library:** React
- **HTTP Client:** Axios

## Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend)
- Gmail Account
- OpenAI API Key
- Google Cloud Project with Gmail API enabled

## Environment Variables
Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your-openai-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=your-oauth-redirect-uri
```

## Setup & Running

### Backend Setup
1. Install dependencies:
```zsh
pip install -r requirements.txt
```

2. Start the FastAPI server:
```zsh
uvicorn backend.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the frontend directory:
```zsh
cd frontend
```

2. Install dependencies:
```zsh
npm install
```

3. Start the development server:
```zsh
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### API Endpoints
- `GET /sync/emails` - Fetch and analyze recent emails
- `GET /auth/login` - Initiate Gmail OAuth2 flow
- `GET /auth/callback` - Handle OAuth2 callback

## Project Structure
```
me-ru/
├── backend/
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic (Gmail, OpenAI)
│   └── main.py        # FastAPI application entry
├── frontend/          # Next.js frontend application
│   ├── pages/         # Next.js pages
│   ├── components/    # React components
│   └── public/        # Static assets
├── requirements.txt   # Python dependencies
└── .env               # Environment variables
```

## Contribution
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License 

<a href="https://github.com/moraxborax/me-ru/tree/backend">
<img src="./python-powered-w.svg" alt="drawing" style="width:192px;"/>
</a>

<a href="https://github.com/moraxborax/me-ru/tree/frontend">
<img src="./nextjs-icon-dark-background.svg" alt="drawing" style="width:64px;"/>
</a>
