import os
import requests
from flask import Flask, render_template, request, redirect, url_for, g, flash
import shutil
import time


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
        begin = time.time()

        user_word = request.form['name']
        user_word = user_word.replace(" ", "-")
        print("Creating Directory")
        os.makedirs(
            '256_ObjectCategories/258.{0}/'.format(user_word), exist_ok=True)

            #grab urls
        command = "python google_images_download.py --keywords " + user_word + \
            " --limit 150 --chromedriver '/Users/kylerood/Generic-Web-Classifier/chromedriver'"
        os.system(command)

        #download images
        command = "python imagedownload.py " + user_word
        os.system(command)

        #train network
        command = "python train_network.py"
        os.system(command)

        print("Deleting Directory")
        shutil.rmtree('256_ObjectCategories/258.{0}/'.format(user_word))

        #timing
        end = time.time()
        print('Total time: ', end-begin)

        return render_template('index.html', user_word=request.form['name'])

    elif request.form['name'] is None:
        flash('Please enter a word!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
