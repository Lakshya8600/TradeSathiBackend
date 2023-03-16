from flask import Flask, redirect, url_for, request , jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf, threading , time , pandas as pd , os
from datetime import date
import pandas_ta as ta
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__ , template_folder='templates')
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

CompanyNames = pd.read_csv('StockData/CompanyNames.csv')
CompanyDataList = os.listdir(os.getcwd()+"/StockData") 
suddenpt7list = []
sudden2perlist = []
vwaplist = []
rsi30list = []
rsi70list = []

def lstostr(list):
   strii = ""
   for names in list:
      strii = strii + '#' + names
   return str(strii)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Minute = db.Column(db.Integer)
    suddenpt7 = db.Column(db.String(1500))
    sudden2per = db.Column(db.String(1500))
    vwap = db.Column(db.String(1500))
    rsi30 = db.Column(db.String(1500))
    rsi70 = db.Column(db.String(1500))
   #  volup = db.Column(db.String(1500), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Minute

def bgtask():
   """background task of getting yfinance data and storing in data base with formatting"""
   currentMin = datetime.now().minute
   while True:
      if currentMin is not datetime.now().minute:
         currentMin = datetime.now().minute
         for Company in CompanyNames.iloc[:,0]:
            try: 
               data = yf.download(tickers=Company,start=date.today(), interval='1m')
               vwapdatalist = ta.vwap(data.iloc[:,1],data.iloc[:,2],data.iloc[:,3],data.iloc[:,5])
               rsidatalist = ta.rsi(data.iloc[:,3]) 
               Timeopen = data.iloc[-10,0]
               Timeclose = data.iloc[-1,3]

               percentchange = 0
               if Timeopen >= Timeclose:
                  percentchange = ((Timeopen-Timeclose)/Timeclose)*100
               else:
                  percentchange = ((Timeclose-Timeopen)/Timeopen)*100

               if 2 > percentchange >= 0.7:
                  suddenpt7list.append(Company)
               if percentchange >= 2:
                  sudden2perlist.append(Company)
               if vwapdatalist.iloc[-1,0]+(vwapdatalist.iloc[-1,0]*(0.05/100)) >= Timeclose >= vwapdatalist.iloc[-1,0]-(vwapdatalist.iloc[-1,0]*(0.05/100)):
                  vwaplist.append(Company)
               if rsidatalist.iloc[-1,0] < 30:
                  rsi30list.append(Company)
               if rsidatalist.iloc[-1,0] > 70:
                  rsi70list.append(Company)

            except:
               pass

         with app.app_context():
            databaserow = User(Minute=datetime.now().minute, suddenpt7=lstostr(suddenpt7list), sudden2per=lstostr(sudden2perlist), vwap=lstostr(vwaplist), rsi30=lstostr(rsi30list), rsi70=lstostr(rsi70list))
            db.session.add(databaserow)
            db.session.commit()
         

@app.route('/getinfo',methods = ['POST', 'GET'])
def hello_world():
   if request.method == 'GET':
      with app.app_context():
         returndata = User.query.all()
         # print(returndata[-1].Minute)
      
      return jsonify( {"Minute": returndata[-1].Minute , "suddenpt7": returndata[-1].suddenpt7,"sudden2per": returndata[-1].sudden2per, "vwap": returndata[-1].vwap, "rsi30": returndata[-1].rsi30, "rsi70": returndata[-1].rsi70})

if __name__ == '__main__':    
   with app.app_context():
      threading.Thread(target=bgtask).start()
      app.run(debug=True)