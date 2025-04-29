import openai
from typing import List
import os

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

class OpenAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def extract_events(self, email_text: str) -> List[dict]:
        # LEGACY CODE: Old GPT-3.5-turbo implementation (commented out)
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are an assistant that extracts calendar events from emails."},
        #         {"role": "user", "content": email_text}
        #     ]
        # )
        # events = []
        # return events

        # NEW: Use OpenAI GPT-4o for event extraction
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Updated to use GPT-4o
            messages=[
                {"role": "system", "content": "You are Meru-chan, an AI assistant that extracts calendar event details from emails. Return a JSON array of events, each with subject, date, start_time, end_time, and location if available. If no event, return an empty array."},
                {"role": "user", "content": email_text}
            ],
            temperature=0.2,
            max_tokens=512
        )
        # Parse response
        content = response.choices[0].message['content']
        try:
            import json
            events = json.loads(content)
            if isinstance(events, list):
                return events
            else:
                return []
        except Exception:
            return []
