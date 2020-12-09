from flask import Flask, render_template, request, url_for, flash, redirect
from threading import Thread
import management_service as manager

app = Flask(__name__)
hashList = []
passwordList = {}
activeThreads = {}
clientManager = manager.start_server(6000)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=('GET', 'POST'))
def crack():
    if request.method == 'POST':
        md5 = request.form['hash']
        hashList.append(md5)
        workerThread = Thread(target=new_req, args=[md5])
        workerThread.start()
        activeThreads[md5] = workerThread
    return render_template('crack.html',hlength = len(hashList), hashList = hashList, passwordList = passwordList)

# Server can call this to return new found password
def receive_password(md5,password):
    passwordList[md5] = password


# Mock function for new requests
def new_req(md5):
    clientManager.new_request(md5, 3)
    password = clientManager.waitForResults()
    receive_password(hashList[-1], password)



