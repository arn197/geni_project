from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from threading import Thread
import management_service as manager
from queue import Queue
import hashlib

app = Flask(__name__)
hashList = []
passwordList = {}
activeThreads = {}
#clientManager = manager.start_server(6000)

dataQueue = Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_reload')
def reload():
    if len(passwordList) == 0:
        return jsonify(password="In progress")
    return jsonify(password=passwordList[hashList[0]])


@app.route('/crack', methods=('GET', 'POST'))
def crack():
    if request.method == 'POST':
        pwd = request.form['pwd']
        chars = len(pwd)
        result = hashlib.md5(pwd.encode())
        md5 = result.hexdigest()
        hashList.append(md5)
        workerThread = Thread(target=new_req, args=([md5],chars))
        workerThread.start()
        activeThreads[md5] = workerThread
    return render_template('crack.html',hlength = len(hashList), hashList = hashList, passwordList = passwordList)

# Server can call this to return new found password
def receive_password(md5,password):
    passwordList[md5] = password


# Mock function for new requests
def new_req(md5,chars):
#    clientManager.new_request(md5, 4)
#    password = clientManager.waitForResults()
    receive_password(hashList[-1], "Password")



