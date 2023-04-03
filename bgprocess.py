import yfinance as yf, threading, time, pandas as pd, os
from datetime import date
import pandas_ta as ta
from datetime import datetime
import pytz

CompanyNames = pd.read_csv("CompanyNames.csv")
suddenpt7list = []
sudden2perlist = []
vwaplist = []
rsi30list = []
rsi70list = []

def lstostr(list):
    strii = ""
    for names in list:
        strii = strii + "#" + names
    return str(strii)


currentMin = datetime.now().minute
while True:
    if currentMin is not datetime.now().minute:
        currentMin = datetime.now().minute
        suddenpt7list = []
        sudden2perlist = []
        vwaplist = []
        rsi30list = []
        rsi70list = []
        for Company in CompanyNames.iloc[:, 0]:
            try:
                data = yf.download(
                    tickers=Company, start=date.today(), interval="1m"
                )
                vwapdatalist = ta.vwap(
                    data.iloc[:, 1],
                    data.iloc[:, 2],
                    data.iloc[:, 3],
                    data.iloc[:, 5],
                )
                rsidatalist = ta.rsi(data.iloc[:, 3])
                Timeopen = data.iloc[-10, 0]
                Timeclose = data.iloc[-1, 3]

                percentchange = 0
                if Timeopen >= Timeclose:
                    percentchange = ((Timeopen - Timeclose) / Timeclose) * 100
                else:
                    percentchange = ((Timeclose - Timeopen) / Timeopen) * 100

                if 2 > percentchange >= 0.7:
                    suddenpt7list.append(Company)
                if percentchange >= 2:
                    sudden2perlist.append(Company)
                if (
                    vwapdatalist[-1] + (vwapdatalist[-1] * (0.05 / 100))
                    >= Timeclose
                    >= vwapdatalist[-1] - (vwapdatalist[-1] * (0.05 / 100))
                ):
                    vwaplist.append(Company)
                if rsidatalist[-1] < 30:
                    rsi30list.append(Company)
                if rsidatalist[-1] > 70:
                    rsi70list.append(Company)

            except:
                pass
        print("sdkjfdsj fs flkj sfkl jaskl fsdjkfh lkas fjkahkfhsk f") 
        # saving lists
        with open("Results/suddenpt7.txt", "w") as file:
            file.write(lstostr(suddenpt7list))
        with open("Results/sudden2per.txt", "w") as file:
            file.write(lstostr(sudden2perlist))
        with open("Results/vwap.txt", "w") as file:
            file.write(lstostr(vwaplist))
        with open("Results/rsi30.txt", "w") as file:
            file.write(lstostr(rsi30list))
        with open("Results/rsi70.txt", "w") as file:
            file.write(lstostr(rsi70list))
        with open("Results/minute.txt", "w") as file:
            file.write(datetime.now(pytz.timezone("Asia/Calcutta")).strftime("%H:%M:%S"))
        

