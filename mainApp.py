from flask import Flask
from flask_apscheduler import APScheduler
import ntplib, os, sqlite3
from time import ctime

app = Flask(__name__)
scheduler = APScheduler()

DB_NAME = 'timeDB.db'

@app.route("/")
def index():
    return "<a href='webdatetime'>web datetime</a>"

@app.route("/webdatetime")
def webdatetime():
    con = sqlite3.connect(DB_NAME)
    cursorObj = con.cursor()
    sql = 'SELECT * FROM tbl_time WHERE id = 0'
    cursorObj.execute(sql)
    data = cursorObj.fetchall()
    con.close()
    return data[0][1]


def scheduledTask():
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    strTime = ctime(response.tx_time)
    
    print(strTime)
    
    con = sqlite3.connect(DB_NAME)
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE tbl_time SET time = ' + "'" + strTime + "'" +' WHERE id = 0')
    con.commit()

if __name__ == '__main__':
    #Make current dir working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    #Start the task
    scheduler.add_job(id='scheduled task', func=scheduledTask, trigger='interval', seconds=30)
    scheduler.start()

    #start the server
    app.run(host='0.0.0.0', port = 8080, debug=True)