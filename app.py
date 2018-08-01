import os
import requests
from flask import Flask, render_template, request, redirect, url_for, g, flash
import shutil
import time
from flask_uploads import UploadSet, configure_uploads, IMAGES


STATIC_FOLDER = 'static'
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = 'secret_key'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
configure_uploads(app, photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        
        results = 0
        
        return render_template('upload.html', filename=filename, results=results)
        
    return render_template('upload.html')


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

        # grab urls
        # for suraj
        # command = "python google_images_download.py --keywords " + user_word + \
        #     " --limit 200 --chromedriver '/home/suraj/Documents/GWU/Generic-Web-Classifier/chromedriver2'"

        # for kyle
        command = "python google_images_download.py --keywords " + user_word + \
            " --limit 200 --chromedriver '/Users/kylerood/Generic-Web-Classifier/chromedriver'"

        os.system(command)

        # download images
        command = "python imagedownload.py " + user_word
        os.system(command)

        # train network
        command = "python train_network.py"
        os.system(command)

        # reset the stuff
        # print("Deleting Directory...")
        # shutil.rmtree('256_ObjectCategories/258.{0}/'.format(user_word))

        # timing
        end = time.time()
        print('Total time: ', end - begin)

        return render_template('index.html', user_word=request.form['name'])

    elif request.form['name'] is None:
        flash('Please enter a word!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
