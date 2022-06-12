import pandas as pd
from binance.client import Client
from binance import ThreadedWebsocketManager
import datetime as dt
import sys
from pprint import pprint
import config
import ccxt
import ta

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

class Bot:
    """ Basic Bot Object """
    def __init__(self, pair):
        self.pair = pair
        self.interval = '1d'
        self.keys = {
            'apiKey': config.KUCOIN_KEY,
            'secret': config.KUCOIN_SECRET,
            'password': config.KUCOIN_PWD
        }
        self.exchange = ccxt.kucoin( self.keys )

    def get_history(self):
        # Create a pandas dataframe with historical kline data.
        cols =['timestamp', 'open', 'high', 'low', 'close', 'volume']
        print("Getting Historical Data...")
        self.history = ( pd.DataFrame( self.exchange.fetch_ohlcv( self.pair, self.interval, limit=365 ), columns = cols ) )
        (close, high, low) = (self.history['close'], self.history['high'], self.history['low'])

        # Add TA Indicators
        # Trend Indicators
        self.history['sma_5'] = ta.trend.sma_indicator( close, 5 )
        self.history['sma_20'] = ta.trend.sma_indicator( close, 20 )
        self.history['sma_50'] = ta.trend.sma_indicator( close, 50 )
        self.history['sma_200'] = ta.trend.sma_indicator( close, 200 )
        self.history['macd'] = ta.trend.macd( close )
        self.history['macd_signal'] = ta.trend.macd_signal( close )

        # Volatility Indicators
        bb_indicator = ta.volatility.BollingerBands( close )
        self.history['bb_upper_band'] = bb_indicator.bollinger_hband()
        self.history['bb_lower_band'] = bb_indicator.bollinger_lband()
        self.history['bb_mavg'] = bb_indicator.bollinger_mavg()

        # Momentum Indicators
        self.history['roc'] = ta.momentum.roc( close )
        self.history['rsi'] = ta.momentum.rsi( close )
        self.history['stoch'] = ta.momentum.stoch( high, low, close )
        self.history['stoch_signal'] = ta.momentum.stoch_signal( high, low, close )
        self.history['stoch_rsi'] = ta.momentum.stochrsi( close )
        self.history['awesome_osc'] = ta.momentum.awesome_oscillator( high, low )
        self.history['ultimate_osc'] = ta.momentum.ultimate_oscillator( high, low, close )

        print("Retreived {} records.".format(len(self.history)))
    def handle_socket_msg(self, msg):
        """ Callback function when a message is received from Binance """

        candle = msg['k']
        self.price = float(candle['c'])
        if(candle['x']): # candle is closed
            self.candles.append(candle)
            open_price = float(candle['o'])
            close_price = float(candle['c'])
            poc = (close_price - open_price) / open_price * 100
            print("{} candle closed".format(self.interval))
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

    def save_history(self):
        csv_file = self.symbol.lower() + '.csv'
        self.kline_history.to_csv(csv_file)

    def save(self):
        pass


