from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/crack', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        hash = request.form['hash']

        if not hash:
            flash('Hash is required')

    return render_template('crack.html')
