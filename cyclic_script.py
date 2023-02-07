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
    return oshort[-2]


def fetch_signals():
    tickers_list = os.environ.get('TICKERS').split(',')
    signal_data = {}
    for ticker in tickers_list:

        # Fetch the data from yfinace
        ticker = yf.Ticker(ticker)
        data = ticker.history(interval="5m")

        short_cycle_lenght = 20
        medium_cycle_lenght = 50
        short_cycle_multiplier = 1.0
        medium_cycle_multipler = 3.0

        oshort = get_current_candle_oshort(
            data, short_cycle_lenght, medium_cycle_lenght, short_cycle_multiplier, medium_cycle_multipler)

        if(oshort > 1.0):
            signal_data.update({ticker.info['shortName'] : "LONG"})
        elif(oshort < 0.0):
            signal_data.update({ticker.info['shortName'] : "SHORT"})
    return signal_data