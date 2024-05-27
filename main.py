import os
import json
import datetime
import base64
import pickle
import asyncio
import telegram
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.pickle'

async def send_telegram_message(token, chat_id, message):
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

def authenticate_gmail():
    creds = None
    token_needs_refresh = False
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_needs_refresh = True
        else:
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

            if not client_id or not client_secret:
                raise ValueError("Client ID or Client Secret not set in environment variables.")

            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds, token_needs_refresh

def get_email_summary(service):
    query = 'newer_than:1d'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    today = datetime.datetime.now(datetime.timezone.utc).date()
    summary = f"Email summary for {today}:\n\n"
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])

        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        from_ = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')

        summary += f"From: {from_}\nSubject: {subject}\n\n"

    if not messages:
        summary += "No new emails today."

    return summary

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
async def main():
    creds, token_needs_refresh = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    summary = get_email_summary(service)

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not telegram_token or not telegram_chat_id:
        raise ValueError("Telegram bot token or chat ID not set in environment variables.")

    if token_needs_refresh:
        await send_telegram_message(telegram_token, telegram_chat_id, "Gmail token has been refreshed.")

    await send_telegram_message(telegram_token, telegram_chat_id, summary)

if __name__ == '__main__':
    asyncio.run(main())
