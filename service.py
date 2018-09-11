from datetime import datetime 
from flask import Flask
import os, glob
from flask import jsonify
from flask import redirect, url_for, Response
import json
from subprocess import call
import gphoto2 as gphoto

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


@app.route("/pictures/take", methods=['PUT'])
def takeApicture():
    
    #call(["gphoto2", "--capture-image-and-download"])
    camera = gphoto.check_result(gphoto.gp_camera_new())
    gphoto.check_result(gphoto.gp_camera_init(camera))
    print('Capturing image')
    file_path = gphoto.check_result(gphoto.gp_camera_capture(
        camera, gphoto.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    print('Copying image to', target)
    camera_file = gphoto.check_result(gphoto.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gphoto.GP_FILE_TYPE_NORMAL))
    gphoto.check_result(gphoto.gp_file_save(camera_file, "static/img"))
    gphoto.check_result(gphoto.gp_camera_exit(camera))
  
    data = {
        "response":"OK"
    }
    
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp
