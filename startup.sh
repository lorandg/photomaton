#!/bin/bash

pkill gphoto2
gphoto2 --auto-detect

export FLASK_APP=service.py 
export FLASK_ENV=development 
export FLASK_RUN_PORT=80 
flask run
