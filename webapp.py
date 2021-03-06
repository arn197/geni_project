from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from threading import Thread
from geni_project import management_service as manager
from queue import Queue
import hashlib

app = Flask(__name__)
hashList = []
passwordList = {}
plist = []
activeThreads = {}
clientManager = manager.start_server(6001)
dataQueue = Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_reload')
def reload():
        return jsonify(password=passwordList, hashList=hashList,count=len(plist))


@app.route('/crack', methods=('GET', 'POST'))
def crack():
    if request.method == 'POST':
        pwd = request.form['pwd']
        chars = len(pwd)
        result = hashlib.md5(pwd.encode())
        md5 = result.hexdigest()
        hashList.append(md5)
        workerThread = Thread(target=new_req, args=(md5,chars))
        workerThread.start()
        activeThreads[md5] = workerThread
    return render_template('crack.html',hlength = len(hashList), hashList = hashList, passwordList = passwordList)

# Add password to list
def receive_password(md5,password):
    print(md5, password)
    passwordList[md5] = password
    plist.append(password)


# Function for new requests
def new_req(md5,chars):
    clientManager.new_request(md5, chars)
    md5_new, password = clientManager.waitForResults()
    receive_password(md5_new,password)


if __name__ == "__main__":
    app.run()
