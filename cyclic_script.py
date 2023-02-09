import yfinance as yf
import pandas_ta as pd_ta
import talib
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv('.env')


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


def fetch_signals(trigger_type):
    if trigger_type == "type1":
        tickers_list = os.environ.get('TICKERS').split(',')
    else:
        tickers_list = os.environ.get('INDEX_TICKERS').split(',')
    current_iteration = os.environ.get('ITERATION')
    signal_data = {}
    for ticker in tickers_list:
        # Fetch the data from yfinace
        yticker = yf.Ticker(ticker)
        data = yticker.history(interval="5m")

        short_cycle_lenght = 20
        medium_cycle_lenght = 50
        short_cycle_multiplier = 1.0
        medium_cycle_multipler = 3.0

        oshort, omed = get_current_candle_oshort(
            data, short_cycle_lenght, medium_cycle_lenght, short_cycle_multiplier, medium_cycle_multipler)

        if trigger_type == "type1":
            if int(current_iteration) == 1:
                if(oshort[-2] > 1.0):
                    signal_data.update({ticker : "LONG"})
                elif(oshort[-2] < 0.0):
                    signal_data.update({ticker : "SHORT"})
            else:
                if(oshort[-2] > 1.0 and oshort[-3] < 1.0 ):
                    signal_data.update({ticker : "LONG"})
                elif(oshort[-2] < 0.0 and oshort[-3] > 0.0):
                    signal_data.update({ticker : "SHORT"})
        else:
            if int(current_iteration) == 1:
                if(oshort[-2] > omed[-2]):
                    signal_data.update({ticker : "LONG"})
                elif(oshort[-2] < omed[-2]):
                    signal_data.update({ticker : "SHORT"})
            else:
                if(oshort[-2] > omed[-2] and oshort[-3] < omed[-3] ):
                    signal_data.update({ticker : "LONG"})
                elif(oshort[-2] < omed[-2] and oshort[-3] > omed[-3]):
                    signal_data.update({ticker : "SHORT"})
    
    return signal_data