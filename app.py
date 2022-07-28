from datetime import date, timedelta
from sys import implementation
from winreg import QueryInfoKey
from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from sqlalchemy import VARCHAR, String
from wtforms import StringField, SubmitField
from geopy.distance import geodesic
from sqlalchemy.sql import text
import redis
import time
import pyodbc
import hashlib
import pickle

app = Flask(__name__)

app.config['SECRET_KEY']='secretKey'

driver = '{ODBC Driver 17 for SQL Server}'
databse='darshan'
server='darshanadb.database.windows.net'
username='darshanadb'
password='Rootroot@'

with pyodbc.connect(
    'DRIVER='+driver+ ';SERVER='+server+ ';PORT=1433;DATABASE='+databse+';UID='+username+ ';PWD='+password) as conn:
     with conn.cursor() as cursor:
        temp=[]

'''cursor.execute("SELECT * FROM quiz")

rst = []
while True:
    rwData = cursor.fetchone()
    if not rwData:
        break
    rst.append(rwData)
print(rst)'''     


r=redis.StrictRedis(host='darshanadbredis.redis.cache.windows.net', port=6380, password='7IC62WqWrkfigQQXvxPeyyXumgvS48irGAzCaIXED8k=',ssl=True)


@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

class taskone(FlaskForm):
    num1 = StringField(label="Enter Number for range =")
    num2 = StringField(label="Enter Number for range =")
    num=StringField(label="Enter the number=")
    subMit = SubmitField(label="Submit")

@app.route('/funone', methods=['GET', 'POST'])
def funone():
    task = taskone()
    if task.validate_on_submit():

        num1=float(task.num1.data)
        num2=float(task.num2.data)
        num=int(task.num.data)

        t=[]
        for i in range(num):
            t1=time.time()
            cursor.execute("SELECT TOP "+str(num)+" * from quiz where D between "+str(num1)+" and "+str(num2)+"")    
            rst = []
            while True:
                rwData = cursor.fetchone()
                if not rwData:
                    break
                rst.append(rwData)
            t2=time.time()
            t.append(t2-t1)
            
        return render_template('taskone.html',rst=rst, task=task,num=num,num1=num1,num2=num2,t=t,data=1)
    return render_template('taskone.html', task=task)

class tasktwo(FlaskForm):
    num1 = StringField(label="Enter Number for range =")
    num2 = StringField(label="Enter Number for range =")
    num=StringField(label="Enter the number=")
    subMit = SubmitField(label="Submit")

@app.route('/funtwo', methods=['GET', 'POST'])
def funtwo():
    task = tasktwo()
    if task.validate_on_submit():

        num1=float(task.num1.data)
        num2=float(task.num2.data)
        num=int(task.num.data)

        t=[]
        for i in range(num):
            t1=time.time()
            
            query=f'SELECT TOP {num} * from quiz where D between {num1} and {num2}'  
            hash=hashlib.sha256(query.encode()).hexdigest()
            key="darshan_rd" +hash
            rst=[]

            if(r.get(key)):
                pass
            else:
                 cursor.execute(query)
                 rows=cursor.fetchall()

                 r.set(key,pickle.dumps(rows))
                 r.expire(key,360)

                 rst.append(rows)
            t2=time.time()
            t.append(t2-t1)
            
        return render_template('tasktwo.html',rst=rst, task=task,num=num,num1=num1,num2=num2,t=t,data=1)
    return render_template('tasktwo.html', task=task)    


if __name__=="__main__":
    app.run(debug=True)