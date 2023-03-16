import pandas_ta as ta
import yfinance as yf 
from datetime import date
data = yf.download(tickers="HDFC.NS",start=date.today(), interval='1m')
print(data)
# h = ta.vwap(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3],data.iloc[:,5])
h = ta.rsi(data.iloc[:,3])
print(h)


