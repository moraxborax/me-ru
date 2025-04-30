from fastapi import FastAPI
from backend.routers import sync
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check required environment variables
required_vars = ["OPENAI_API_KEY"]
recommended_vars = ["CLIENT_SECRET_JSON_PATH", "TOKEN_PATH"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
missing_recommended = [var for var in recommended_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")

if missing_recommended:
    logger.warning(f"Missing recommended environment variables: {', '.join(missing_recommended)}")
    logger.info("Using default paths for Gmail authentication. Make sure client_secret.json exists.")

app = FastAPI(
    title="ME-RU - AI Email Agent",
    description="An AI-powered email assistant that fetches and analyzes your emails",
    version="0.1.0"
)

app.include_router(sync.router, prefix="/sync")

@app.get("/")
def read_root():
    return {"message": "Welcome to me-ru!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
