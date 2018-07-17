from flask import Flask, render_template, request, redirect, url_for, g, flash

STATIC_FOLDER = 'static'

app = Flask(__name__, static_folder=STATIC_FOLDER)

@app.route('/')
def homepage():
    return render_template('index.html')
