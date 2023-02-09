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
CYCLIC_CHAT_ID = os.environ.get("CYCLIC_CHAT_ID")
CROSSOVER_CHAT_ID = os.environ.get("CROSSOVER_CHAT_ID")

async def send_cyclic_signal(cyclic_signals_dict):
    bot = Bot(token=TOKEN)
    if cyclic_signals_dict:
        for key in cyclic_signals_dict.keys():
            await bot.send_message(chat_id=CYCLIC_CHAT_ID, text="{} - {}".format(key, cyclic_signals_dict.get(key)), write_timeout=60, read_timeout=60, connect_timeout=60, pool_timeout=60)
        await bot.send_message(chat_id=CYCLIC_CHAT_ID, text="---------------------------------------")

async def send_crossover_signal(crossover_signals_dict):
    bot = Bot(token=TOKEN)
    if crossover_signals_dict:
        for key in crossover_signals_dict.keys():
            await bot.send_message(chat_id=CROSSOVER_CHAT_ID, text="{} - {}".format(key, crossover_signals_dict.get(key)), write_timeout=20, read_timeout=20, connect_timeout=20, pool_timeout=20)
        await bot.send_message(chat_id=CROSSOVER_CHAT_ID, text="---------------------------------------")

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


def get_sleep_time():
    now = datetime.datetime.now()
    next_5th_minute = (now.minute - now.minute % 5 + 5) % 60
    sleep_time = (60 - now.second) + (next_5th_minute - now.minute) * 60
    if sleep_time < 0:
        sleep_time += 60 * 60
    return sleep_time


while True:
    if is_time():
        current_iteration = os.environ.get('ITERATION')
        cyclic_signals_dict = fetch_signals('type1')
        asyncio.run(send_cyclic_signal(cyclic_signals_dict))
        crossover_signals_dict = fetch_signals('type2')
        asyncio.run(send_crossover_signal(crossover_signals_dict))
        os.environ['ITERATION'] = str(int(current_iteration) + 1)
        time.sleep(get_sleep_time() + 5)
    else:
        time.sleep(10)
