from flask import Flask, redirect, url_for, request , jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf, threading , time , pandas as pd , os
from datetime import date
app = Flask(__name__ , template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sudden.db'
dbsudden = SQLAlchemy(app) 

CompanyNames = pd.read_csv('StockData/CompanyNames.csv')
CompanyDataList = os.listdir(os.getcwd()+"/StockData") 

class User(dbsudden.Model):
   id = dbsudden.Column(dbsudden.Integer, primary_key=True)
   Stockname = dbsudden.Column(dbsudden.String(30), nullable=False)
   # percentage = dbsudden.Column(dbsudden.Integer, nullable=False)
   Minute = dbsudden.Column(dbsudden.String(20), nullable=False)
   
   def __repr__(self):
      return '<User %r>' % self.username

def bgtask():
   """background task of getting yfinance data and storing in data base with formatting"""
   while True:
      # searching for all the companies in the companynames
      for Company in CompanyNames.iloc[:,0]:
         # getting stock prices data and getting the 
         try: 
            data = yf.download(tickers=Company,start=date.today(), interval='1m')
            Timeopen = data.iloc[-10,0]
            Timeclose = data.iloc[-1,3]
         except:
            pass
         
         percentchange = 0
         if Timeopen >= Timeclose:
            percentchange = ((Timeopen-Timeclose)/Timeclose)*100
         else:
            percentchange = ((Timeclose-Timeopen)/Timeopen)*100

         if percentchange > 0.5:
            print(Company)
            print(percentchange)
            

@app.route('/suddench',methods = ['POST', 'GET'])
def hello_world():
   if request.method == 'GET':
      return jsonify( {"message": "hellllldsflkjp", "severity": "danger"})

if __name__ == '__main__':  
   threading.Thread(target=bgtask).start()
   app.run(debug=True)