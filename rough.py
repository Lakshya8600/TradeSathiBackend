import yfinance as yf 
from datetime import date
data = yf.download(tickers="HDFC.NS",start=date.today(), interval='1m')
print(data)