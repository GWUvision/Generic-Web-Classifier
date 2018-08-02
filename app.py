import os
import requests
from flask import Flask, render_template, request, redirect, url_for, g, flash, session
import shutil
import time
from flask_uploads import UploadSet, configure_uploads, IMAGES
import test_network

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

        cwd = os.getcwd()
        session['filepath'] = cwd + "/static/" + filename

        return redirect(url_for('result'))

        # return render_template('upload.html', filename=filename, results=results)

    return render_template('upload.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    
    path = '256_ObjectCategories'
    categories = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            categories[name.split('.')[0]] = name.split('.')[-1]

    print(categories)
    output = test_network.test_network_classifier(str(session['filepath']), 'example_model')

    # print(str(output).zfill(3))

    result = categories[str(output).zfill(3)]
    
    # print(categories[str(output)])

    return render_template('result.html', result=result)



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
        #chromedriver is for mac, chromedriver2 is for linux
        cwd = os.getcwd()
        command = "python google_images_download.py --keywords " + user_word + \
            " --limit 200 --chromedriver '{0}/chromedriver'".format(cwd)

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
        # os.remove("output.csv")

        # timing
        end = time.time()
        print('Total time: ', end - begin)

        return redirect(url_for('upload'))

    elif request.form['name'] is None:
        flash('Please enter a word!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
