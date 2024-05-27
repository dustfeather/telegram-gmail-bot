# gmail_summary/email_summary.py

import datetime

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
        message_id = msg['id']
        email_link = f"https://mail.google.com/mail/u/0/#inbox/{message_id}"

        summary += f"From: {from_}\nSubject: {subject}\nLink: {email_link}\n\n"

    if not messages:
        summary += "No new emails today."

    return summary
