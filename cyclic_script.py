import pandas_ta as pd_ta
import talib
from dotenv import load_dotenv
import os
from datetime import date, timedelta
import pandas as pd

# Load the .env file
load_dotenv('.env')

scripts_dict = {
    "999920000": "NIFTY 50",
    "999920005": "BANK NIFTY"
}

def get_current_candle_oshort(data, short_cycle_length, medium_cycle_length, short_cycle_multiplier, medium_cycle_multiplier):

    scl = short_cycle_length//2
    mcl = medium_cycle_length//2

    rma_scl = pd_ta.rma(data["Close"], scl)
    rma_mcl = pd_ta.rma(data["Close"], mcl)

    scm_off = short_cycle_multiplier * \
        talib.ATR(data["High"], data["Low"], data["Close"], timeperiod=scl)

    mcm_off = medium_cycle_multiplier * \
        talib.ATR(data["High"], data["Low"], data["Close"], timeperiod=mcl)

    scl_2 = scl/2
    mcl_2 = mcl/2

    sct = rma_scl.shift(int(scl_2)).fillna(data["Close"]) + scm_off
    scb = rma_scl.shift(int(scl_2)).fillna(data["Close"]) - scm_off
    mct = rma_mcl.shift(int(mcl_2)).fillna(data["Close"]) + mcm_off
    mcb = rma_mcl.shift(int(mcl_2)).fillna(data["Close"]) - mcm_off

    scmm = (sct + scb)/2

    omed = (scmm-mcb)/(mct-mcb)
    oshort = (data["Close"]-mcb)/(mct-mcb)
    return oshort, omed

def get_data_by_script(client, script_code):
    to_date = date.today()
    # Calculate the date 60 days ago
    days_ago = timedelta(days=60)
    from_date = (to_date - days_ago).strftime("%Y-%m-%d")
    to_date = to_date.strftime("%Y-%m-%d")

    df=client.historical_data('N','C',script_code,'5m',from_date,to_date)

    # Convert 'Datetime' column to datetime type
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Filter rows based on time range
    start_time = pd.to_datetime('9:15').time()
    end_time = pd.to_datetime('15:30').time()
    filtered_df = df[(df['Datetime'].dt.time >= start_time) & (df['Datetime'].dt.time <= end_time)]
    return filtered_df


def fetch_signals(trigger_type,client):
    if trigger_type == "type1":
        script_list = os.environ.get('SCRIPTS').split(',')
    else:
        script_list = os.environ.get('INDEX_SCRIPTS').split(',')
    current_iteration = os.environ.get('ITERATION')
    signal_data = {}
    for script in script_list:

        data = get_data_by_script(client, script)

        short_cycle_lenght = 20
        medium_cycle_lenght = 50
        short_cycle_multiplier = 1.0
        medium_cycle_multipler = 3.0

        oshort, omed = get_current_candle_oshort(
            data, short_cycle_lenght, medium_cycle_lenght, short_cycle_multiplier, medium_cycle_multipler)

        if trigger_type == "type1":
            if int(current_iteration) == 1:
                if(oshort.iloc[-2] > 1.0):
                    signal_data.update({scripts_dict.get(script) : "LONG"})
                elif(oshort.iloc[-2] < 0.0):
                    signal_data.update({scripts_dict.get(script) : "SHORT"})
            else:
                if(oshort.iloc[-2] > 1.0 and oshort.iloc[-3] < 1.0 ):
                    signal_data.update({scripts_dict.get(script) : "LONG"})
                elif(oshort.iloc[-2] < 0.0 and oshort.iloc[-3] > 0.0):
                    signal_data.update({scripts_dict.get(script) : "SHORT"})
        else:
            if int(current_iteration) == 1:
                if(oshort.iloc[-2] > omed.iloc[-2]):
                    signal_data.update({scripts_dict.get(script) : "LONG"})
                elif(oshort.iloc[-2] < omed.iloc[-2]):
                    signal_data.update({scripts_dict.get(script) : "SHORT"})
            else:
                if(oshort.iloc[-2] > omed.iloc[-2] and oshort.iloc[-3] < omed.iloc[-3] ):
                    signal_data.update({scripts_dict.get(script) : "LONG"})
                elif(oshort.iloc[-2] < omed.iloc[-2] and oshort.iloc[-3] > omed.iloc[-3]):
                    signal_data.update({scripts_dict.get(script) : "SHORT"})
    
    return signal_data