import os
import json
import datetime
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
import telegram
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    user_to_impersonate = os.getenv('GOOGLE_USER_TO_IMPERSONATE')

    if not service_account_json or not user_to_impersonate:
        raise ValueError("Service account JSON or user to impersonate not set in environment variables.")

    service_account_info = json.loads(service_account_json)
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES, subject=user_to_impersonate)

    return creds

def get_email_summary(service):
    query = 'newer_than:1d'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    today = datetime.datetime.utcnow().date()
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

def send_telegram_message(token, chat_id, message):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    summary = get_email_summary(service)

    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not telegram_token or not telegram_chat_id:
        raise ValueError("Telegram bot token or chat ID not set in environment variables.")

    send_telegram_message(telegram_token, telegram_chat_id, summary)

if __name__ == '__main__':
    main()
