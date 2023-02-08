from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os
from cyclic_script import fetch_signals
import time
import datetime

# Load the .env file
load_dotenv('.env')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def send_signal(signals_dict):
    bot = Bot(token=TOKEN)
    if signals_dict:
        for key in signals_dict.keys():
            await bot.send_message(chat_id=CHAT_ID, text="{} - {}".format(key, signals_dict.get(key)), write_timeout=120, read_timeout=120, connect_timeout=120, pool_timeout=120)
        await bot.send_message(chat_id=CHAT_ID, text="---------------------------------------")


def is_time():
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute >= 20:
        return True
    elif now.hour > 9 and now.hour < 15:
        return True
    elif now.hour == 15 and now.minute <= 15:
        return True
    else:
        return False


while True:
    if is_time():
        signals_dict = fetch_signals()
        asyncio.run(send_signal(signals_dict))
        time.sleep(300)
    else:
        time.sleep(10)
