#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCamPanTilt.py
#  	Streaming video with Flask based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with PanTilt position Control
#
#   MJRoBot.org 30Jan18

import os
from time import sleep
from flask import Flask, render_template, request, Response, jsonify

# Raspberry Pi camera module (requires picamera package from Miguel Grinberg)
from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

panPin = 16
tiltPin = 21

@app.route('/')
def index():
    """Video streaming home page."""
 
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
    return render_template('index.html', **templateData)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 30
		else:
			panServoAngle = panServoAngle - 30
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 30
		else:
			tiltServoAngle = tiltServoAngle - 30
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	return jsonify(success=True)

@app.route("/leftmost")
def leftmost():
    global panServoAngle
    panServoAngle=150
    os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
    return jsonify(success=True)


@app.route("/rightmost")
def rightmost():
    global panServoAngle
    panServoAngle=30
    os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
    return jsonify(success=True)


@app.route("/tocentre")
def tocentre():
    global panServoAngle
    global tiltServoAngle
    panServoAngle=90
    tiltServoAngle=100
    os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
    os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))	
    return jsonify(success=True)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port =4321, debug=True, threaded=True)
