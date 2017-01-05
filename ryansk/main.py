from flask import Flask, send_from_directory, redirect, render_template, request
from urllib.request import urlopen
import shutil, os
from time import strftime, localtime
from forms import UploadForm
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)

def retrieveImage(imgUrl, imgName):

    if imgName == '':
        imgName = imgUrl.rsplit('/', 1)[-1]

    fileName = os.path.join(UPLOAD_FOLDER, imgName)

    with urlopen(imgUrl) as response, open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return imgName

def uploadImage(request, fileName):
    file = request.files['file']
    if fileName == '':
        fileName = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, fileName))
    return fileName

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if not os.path.isdir(fn):
                size = "%.2fKB" % (os.path.getsize(fn) / 1000.0)
                time = os.path.getmtime(fn)
                time = strftime("%b %d %Y %H:%M:%S", localtime(time))
                tree['children'].append(dict(name=name, size=size, time=time, path='/browse/' + name))
    return tree

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST' :

        if form.url.data != '' :
            print('retrieve')
            imgName = retrieveImage(form.url.data, form.name.data)
            return redirect("/browse/%s" % imgName)

        elif form.file.data is not None :
            print('upload')
            imgName = uploadImage(request, form.name.data)
            return redirect("/browse/%s" % imgName)

    return render_template('upload.html', form=form)

@app.route('/browse/')
def dirTree():
    return render_template('dirtree.html', tree=make_tree(UPLOAD_FOLDER))

@app.route('/browse/<imgName>')
def browseImage(imgName):
    return render_template('browse.html', imgName=imgName)

@app.route('/<dir>/<imgName>')
def showImage(dir, imgName):
    return send_from_directory(dir, imgName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
