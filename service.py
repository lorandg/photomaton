from datetime import datetime 
from flask import Flask
import os, glob
from flask import jsonify
from flask import redirect, url_for, Response, request
import json
from subprocess import call
import gphoto2 as gp
import logging
import time


app= Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route("/pictures", methods = ['GET'])
def pictures():
    files = list(filter(os.path.isfile, glob.glob("static/img/*.jpg")))
    files.sort(key=lambda picture: os.path.getmtime(picture))
    filesInfo = [{"name":filename[7:],"date":datetime.fromtimestamp(os.path.getmtime(filename)).isoformat()} for filename in files]
    
    return jsonify(filesInfo[::-1])


@app.route("/pictures/take", methods=['PUT'])
def takeApicture():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    curFilePath = os.path.dirname(os.path.realpath(__file__))
    imgName="Photomat_"+datetime.now().isoformat()+".jpg"
    target = os.path.join(curFilePath, 'static/img', imgName)
    print('Copying image to', target)
    camera_file = gp.check_result(gp.gp_camera_file_get(
        camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera))

    data = {
        "response":"OK"
    }
    
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/pictures', methods = ['POST'])
def receiveImg():
    image = request.files['image']  # get the image
    file = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    image.save('%s/%s' % ("static/img/", file))
    
    return Response("%s saved" % file)