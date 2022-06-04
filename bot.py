import pandas as pd
from binance.client import Client
from binance import ThreadedWebsocketManager
import datetime as dt
import sys
from config import api_key, api_secret
from pprint import pprint

# Messages are received as a dictionary with this structure
# Kline information
#  "e": "kline",     // Event type
#  "E": 123456789,   // Event time
#  "s": "BNBBTC",    // Symbol
#  "k": {
#    "t": 123400000, // Kline start time
#    "T": 123460000, // Kline close time
#    "s": "BNBBTC",  // Symbol
#    "i": "1m",      // Interval
#    "f": 100,       // First trade ID
#    "L": 200,       // Last trade ID
#    "o": "0.0010",  // Open price
#    "c": "0.0020",  // Close price
#    "h": "0.0025",  // High price
#    "l": "0.0015",  // Low price
#    "v": "1000",    // Base asset volume
#    "n": 100,       // Number of trades
#    "x": false,     // Is this kline closed?
#    "q": "1.0000",  // Quote asset volume
#    "V": "500",     // Taker buy base asset volume
#    "Q": "0.500",   // Taker buy quote asset volume
#    "B": "123456"   // Ignore

closes = []
candles = []
green_candles = []
red_candles = []
prev_color = ''
consecutive_g = 1
consecutive_r = 1
in_position = False
max_trades = 9
num_trades = 0
position_price = 0

class Bot:
    """ Basic Bot Object """
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret, tld = 'us')
        self.price = 0

    def open_socket(self):
        # Establush a socket with Binance API
        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        self.twm.start()

    def get_historical(self):
        # Create a pandas dataframe with historical kline data.
        print("Getting Historical Data...")
        self.kline_history = self.client.get_historical_klines(self.symbol, self.interval, '1 Jan, 2021')
        self.kline_history = pd.DataFrame(self.kline_history)
        self.kline_history.columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']

        # Format Dates from timestamps in milliseconds
        self.kline_history['open_time'] = pd.to_datetime(self.kline_history['open_time'], unit='ms', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        self.kline_history['close_time'] = pd.to_datetime(self.kline_history['close_time'], unit='ms', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')

        # Add columns for SMA's
        if self.interval == '5m':
            mult = 288
        elif self.interval == '10m':
            mult = 144
        elif self.interval == '30m':
            mult = 48
        elif self.interval == '1h':
            mult=24
        else: mult = 0

        smas = [5, 20, 50, 200]
        for n in smas:
            sma_name = 'sma_' + str(n)
            self.kline_history[sma_name] = self.kline_history.iloc[:,1].rolling(window = mult * n).mean()
        print("Retreived {:,} records.".format(len(self.kline_history)))

    def handle_socket_msg(self, msg):
        """ Callback function when a message is received from Binance """

        global closes
        global candles
        global green_candles
        global red_candles
        global prev_color
        global consecutive_g
        global consecutive_r
        global in_position
        global max_trades
        global num_trades
        global position_price

        candle = msg['k']
        self.price = candle['c']

        if(candle['x']):
            candles.append(candle)
            open_price = float(candle['o'])
            close_price = float(candle['c'])
            poc = (close_price - open_price) / open_price * 100

            print("Open Price: ${:,.2f}".format(open_price))
            print("Close Price: ${:,.2f}".format(close_price))
            print("Percent Change: {}%".format(round(poc, 4)))

        current_price = float(candle['c'])

    def start(self):
        twm = self.twm
        symbol = self.symbol
        interval = self.interval
        twm.start_kline_socket(callback=self.handle_socket_msg, symbol = symbol, interval= interval)

    def stop(self):
        self.twm.stop()

    def save(self):
        pass


