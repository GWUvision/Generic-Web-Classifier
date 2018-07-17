import os
import requests
from flask import Flask, render_template, request, redirect, url_for, g, flash


STATIC_FOLDER = 'static'
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = 'secret_key'


@app.route('/')
def index():
    flash('Please enter a word!')
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():

    if request.form['name'] is not None:

        user_word = request.form['name']

        return render_template('index.html', user_word=request.form['name'])

    elif request.form['name'] is None:
        flash('Please enter a word!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
