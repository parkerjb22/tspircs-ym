from flask import Flask, send_from_directory, redirect, render_template, request, url_for
from urllib.request import urlopen
import shutil
import os
from forms import UploadForm

app = Flask(__name__)

def retrieveImage(imgUrl):
    imgName = imgUrl.rsplit('/', 1)[-1]
    fileName = "uploads/%s" % imgName
    with urlopen(imgUrl) as response, open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return imgName

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if not os.path.isdir(fn):
                tree['children'].append(dict(name=name, path='/browse/' + name))
    return tree

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST' :
        imgName = retrieveImage(form.url.data)
        return redirect("/browse/%s" % imgName)
    return render_template('upload.html', form=form)

@app.route('/browse/')
def dirTree():
    return render_template('dirtree.html', tree=make_tree('uploads'))

@app.route('/browse/<imgName>')
def browseImage(imgName):
    return render_template('browse.html', imgName=imgName)

@app.route('/<dir>/<imgName>')
def showImage(dir, imgName):
    return send_from_directory(dir, imgName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
