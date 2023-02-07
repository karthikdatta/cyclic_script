from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os
from cyclic_script import fetch_signals

# Load the .env file
load_dotenv('.env')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def send_signal(bot):
    signals_dict = fetch_signals()
    if signals_dict:
        for key in signals_dict.keys():
            await bot.send_message(chat_id=CHAT_ID,text="{} - {}".format(key,signals_dict.get(key)))
        await bot.send_message(chat_id=CHAT_ID,text="---------------------------------------")


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    try:
        asyncio.run(send_signal(bot))
    except KeyboardInterrupt:
        pass
    