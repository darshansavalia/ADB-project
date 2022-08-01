from datetime import date, timedelta
from itertools import count
from sys import implementation
from unittest import result
from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from sqlalchemy import VARCHAR
from wtforms import StringField, SubmitField
from geopy.distance import geodesic
from sqlalchemy.sql import text
import pyodbc

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


#r=redis.StrictRedis(host='darshanadbredis.redis.cache.windows.net', port=6380, password='7IC62WqWrkfigQQXvxPeyyXumgvS48irGAzCaIXED8k=',ssl=True)


@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

class taskone(FlaskForm):
    magnitude = StringField(label="Enter magnitude =")
    subMit = SubmitField(label="Submit")

@app.route('/funone', methods=['GET', 'POST'])
def funone():
    task = taskone()
    cnt=0
           
    #cursor.execute('SELECT count(*) as "Mag less than 1.0" from all_month where mag < 1 UNION SELECT count(*) as "Mag. between 1.0 to 2.0" from all_month where mag >= 1.0 and  mag <2.0 UNION SELECT count(*) as "Mag. between 2.0 to 3.0" from all_month where mag >= 2.0 and mag < 3.0 UNION SELECT count(*) as "Mag. between 3.0 to 4.0" from all_month where mag >= 3.0 and mag < 4.0 UNION SELECT count(*) as "Mag. between 4.0 to 5.0" from all_month where mag >= 4.0 and mag < 5.0 UNION SELECT count(*) as "Mag. grater than 5.0" from all_month where mag >= 5.0')

    cursor.execute('SELECT count(*) as "Mag. less than 1.0" from all_month where mag < 1')
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        result = {columns[0]: row[0]}
        cnt += row[0]

        cursor.execute('SELECT count(*) as "Mag. between 1.0 to 2.0" from all_month where mag >= 1.0 and  mag <2.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            cnt += row[0]

        cursor.execute('SELECT count(*) as "Mag. between 2.0 to 3.0" from all_month where mag >= 2.0 and mag < 3.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            cnt += row[0]

        cursor.execute('SELECT count(*) as "Mag. between 3.0 to 4.0" from all_month where mag >= 3.0 and mag < 4.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            cnt += row[0]

        cursor.execute('SELECT count(*) as "Mag. between 4.0 to 5.0" from all_month where mag >= 4.0 and mag < 5.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            cnt += row[0]

        cursor.execute('SELECT count(*) as "Mag. grater than 5.0" from all_month where mag >= 5.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            cnt += row[0]


        return render_template('taskone.html', result=result, cnt=cnt, data=1)   
    return render_template('taskone.html', task=task)


if __name__=="__main__":
    app.run(debug=True)