from telegram import Bot
import asyncio
from dotenv import load_dotenv
import os
from cyclic_script import fetch_signals
import time

# Load the .env file
load_dotenv('.env')

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


async def send_signal(signals_dict):
    bot = Bot(token=TOKEN)
    if signals_dict:
        for key in signals_dict.keys():
            await bot.send_message(chat_id=CHAT_ID,text="{} - {}".format(key,signals_dict.get(key)))
        await bot.send_message(chat_id=CHAT_ID,text="---------------------------------------")
    

while True:
    signals_dict = fetch_signals()
    asyncio.run(send_signal(signals_dict))
    time.sleep(300)
    