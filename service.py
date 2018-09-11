from datetime import datetime 
from flask import Flask
import os, glob
from flask import jsonify
from flask import redirect, url_for
app= Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route("/pictures")
def pictures():
    files = list(filter(os.path.isfile, glob.glob("static/img/*.jpg")))
    files.sort(key=lambda picture: os.path.getmtime(picture))
    filesInfo = [{"name":filename[7:],"date":datetime.fromtimestamp(os.path.getmtime(filename)).isoformat()} for filename in files]
    
    return jsonify(filesInfo[::-1])
