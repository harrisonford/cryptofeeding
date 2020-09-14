#%% Loading data
import finplot as fplt
import numpy as np
import pandas as pd

symbol = 'FUTURES BTC-USDT'

#df = pd.read_csv('Binance_BTCUSDT_1m_1596240000000-1598918400000.csv')
df = pd.read_csv('Binance_BTCUSDT_1m_1567987200000-1598918400000.csv')
df = df.rename(columns={'Open_time':'time', 'Open':'open', 'Close':'close', 'High':'high', 'Low':'low', 'Volume':'volume'})
df

#%% Calculate volatility in various timeframes
windows = [3, 5, 10, 30, 60, 60*4, 60*12, 60*24, 60*24*3, 60*24*7, 60*24*30]

maxim = []
minim = []
center = []
volatility_diff = []
volatility = []

for window in windows: 
    ma = df['high'].rolling(window).max() # volatility box top
    mi = df['low'].rolling(window).min()  # volatility box bottom}
    c  = ma-mi # volatility box center
    vol = c/ma # volatility
    diff = vol.diff()
    
    volatility.append(vol)
    volatility_diff.append(diff)
    #volatility = volatility.rolling(60*6).mean()
    #open_price_position_relative_to_volatility_box = (df['open']-df['low'])/center
#%% Plot

# create two plots
ax, ax2, ax3 = fplt.create_plot(symbol, rows=3)

# plot candle sticks
candles = df[['time','open','close','high','low']]
fplt.candlestick_ochl(candles, ax=ax)

# overlay volume on the top plot
volumes = df[['time','open','close','volume']]
fplt.volume_ocv(volumes, ax=ax.overlay())

# put an MA on the close price
#fplt.plot(df['time'], df['close'].rolling(window).mean(), ax=ax, legend='ma-25')
#fplt.plot(df['time'], maxim, ax=ax, legend='maxim')
#fplt.plot(df['time'], minim, ax=ax, legend='minim')

# draw second plot
for i, window in enumerate(windows): 
    if(i<5):
        fplt.plot(df['time'], volatility[i], ax=ax2, legend='volatility ' + str(window))
    if(i>=5):
        fplt.plot(df['time'], volatility[i], ax=ax3, legend='volatility ' + str(window))
#fplt.set_y_range(0, 0.005, ax=ax2) # hard-code y-axis range limitation

# draw third plot
#fplt.plot(df['time'], volatility_diff, ax=ax3, color='#927', legend='volatility_diff')

# draw fourth plot
#fplt.plot(df['time'], open_price_position_relative_to_volatility_box, ax=ax4, color='#927', legend='open_price_position_relative_to_volatility_box')

# restore view (X-position and zoom) if we ever run this example again
fplt.autoviewrestore()

# we're done
fplt.show()

# %%
i = 1