import telegram
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
async def send_telegram_message(token, chat_id, message):
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)
