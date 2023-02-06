from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os
from cyclic_script import fetch_signal

# Load the .env file
load_dotenv('.env')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def send_signal(bot):
    signal = fetch_signal()
    if not signal:
        await bot.send_message(chat_id=CHAT_ID,text="No signal found")
    else:
        await bot.send_message(chat_id=CHAT_ID,text=signal)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    try:
        asyncio.run(send_signal(bot))
    except KeyboardInterrupt:
        pass
    