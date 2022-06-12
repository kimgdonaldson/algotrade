AlgoTrade

This purpose of this project is to use historical data and indicators to trade algorithmically using Binace API.

To run bot.py you will need to create a set of API keys on Binace.
Then you will store those in a config.py
api_key = 'your api key'
api_secret = 'your api secret'

To create a boy from python console try:
>>> from bot import *
>>> btc = Bot('BTCUSDT', '1h') 
>>> btc.open_socket()
>>> btc.get_historical()

Once you run get_historical your bot will now have pandas dataframe with historical data including SMA's 

                 open_time            open            high             low           close       volume           close_time  ... taker_base_vol  taker_quote_vol ignore         sma_5        sma_20        sma_50       sma_200
0      2021-01-01 00:00:00  28933.86000000  29034.02000000  28708.39000000  29012.30000000  13.66908000  2021-01-01 00:59:59  ...     4.32474800  125138.69002030      0           NaN           NaN           NaN           NaN
1      2021-01-01 01:00:00  28999.37000000  29475.57000000  28961.27000000  29405.80000000  24.40311200  2021-01-01 01:59:59  ...    11.95001500  350663.05552274      0           NaN           NaN           NaN           NaN
2      2021-01-01 02:00:00  29434.69000000  29465.08000000  29122.75000000  29187.35000000  16.71701500  2021-01-01 02:59:59  ...     4.37230400  127906.82311025      0           NaN           NaN           NaN           NaN
3      2021-01-01 03:00:00  29213.39000000  29356.23000000  29149.88000000  29282.51000000   8.10174800  2021-01-01 03:59:59  ...     4.06921900  119145.64818090      0           NaN           NaN           NaN           NaN
4      2021-01-01 04:00:00  29280.63000000  29405.54000000  29071.86000000  29215.39000000   6.42811000  2021-01-01 04:59:59  ...     1.95458900   57228.36168763      0           NaN           NaN           NaN           NaN
...                    ...             ...             ...             ...             ...          ...                  ...  ...            ...              ...    ...           ...           ...           ...           ...
12444  2022-06-03 22:00:00  29805.48000000  29888.38000000  29701.00000000  29735.61000000   3.56545000  2022-06-03 22:59:59  ...     1.52711900   45551.26707132      0  30690.452333  29881.082396  34374.871883  42187.627306
12445  2022-06-03 23:00:00  29735.61000000  29735.61000000  29642.85000000  29704.16000000   2.13997200  2022-06-03 23:59:59  ...     0.48234400   14324.34309091      0  30692.957750  29879.972854  34366.464708  42180.489760
12446  2022-06-04 00:00:00  29713.66000000  29757.14000000  29686.12000000  29707.33000000   0.70761000  2022-06-04 00:59:59  ...     0.25610300    7616.64777254      0  30694.965417  29879.163667  34357.940783  42173.427660
12447  2022-06-04 01:00:00  29671.40000000  29673.03000000  29551.45000000  29575.93000000   3.20201000  2022-06-04 01:59:59  ...     0.90314000   26720.42276330      0  30697.843167  29878.529458  34349.462242  42166.580598
12448  2022-06-04 02:00:00  29573.59000000  29623.74000000  29485.25000000  29506.23000000   2.29341500  2022-06-04 02:59:59  ...     1.02695300   30300.76376749      0  30696.253583  29877.744229  34340.831042  42159.801833

Once you run start() the bot will start pulling real time candle data from Binance. This is where buy/sell logic will go to make real time trading decisions.
In it's current state start() will just print the closed candle data to the console. 
