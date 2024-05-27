# main.py

import asyncio
from googleapiclient.discovery import build
from gmail_summary.auth import authenticate_gmail
from gmail_summary.email_summary import get_email_summary
from gmail_summary.telegram_notifier import send_telegram_message
from gmail_summary.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def main():
    creds, token_needs_refresh = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    summary = get_email_summary(service)

    if token_needs_refresh:
        await send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Gmail token has been refreshed.")

    await send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, summary)

if __name__ == '__main__':
    asyncio.run(main())
