"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import cv2
import numpy as np
import base64
import sys
import os.path
from datetime import datetime
from matplotlib import pyplot as plt
from face_recognition import *
from template_match import *
from fingerprint import *
from flask import Flask,request,send_file,render_template,jsonify
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
currss=''
dir_path='C:/temp_data/'
face_result=''

def server_init():
    global currss
    ssid = open(dir_path+'session.id', 'r')
    currss = ssid.readline().rstrip('\n')
    return currss

@app.route('/')
def hello():
    global currss
    currss=server_init()
    return 'This session: ' + currss

@app.route('/app_upload_face', methods=['POST'])
def app_upload_face():
    global face_result
    server_init()
    #return send_file(dir_path+currss+'face.jpg',mimetype='image/gif')
    try:
        filestr = request.files['image'].read()
        npimg = np.fromstring(filestr, np.uint8)
        # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
        img1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR) 
        img2 = cv2.imread(dir_path+currss+'faceimg.jpg')
        cv2.imwrite(dir_path+currss+'face.jpg',img1)
        #img1 = cv2.imread('./image/dai_sf.jpg')
        #img2 = cv2.imread('./image/dai_cmnd.jpg')
        face_result=face_recognition(img1,img2)    
        return jsonify(
        stt=str(face_result))
    except Exception as e:
        return jsonify(
        error=str(e))
@app.route('/app_face_result', methods=['GET'])
def app_face_result():
    try:
        return send_file(dir_path+currss+'faceimg.jpg',mimetype='image/gif')   
    except Exception as e:
        return jsonify(
        error=str(e))
@app.route('/app_upload_template',methods=['POST'])
def app_upload_template():
    global currss
    server_init()
    try:
        filestr = request.files['image'].read()
        npimg = np.fromstring(filestr, np.uint8)
        # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        result=template_matching(img)
        cv2.imwrite(dir_path+currss+'temp_result.jpg', result)
        #process_img(img)
        return jsonify(
        stt=str(return_percent()))
    except Exception as e:
        return jsonify(
        error=str(e))

@app.route('/app_template_result', methods=['GET'])
def app_template_result():
    server_init()
    try:
        return send_file(dir_path+currss+'temp_result.jpg',mimetype='image/gif')
    except Exception as e:
        return jsonify(
        error=str(e))

@app.route('/app_get_finger', methods=['GET'])
def app_get_finger():
    return send_file(dir_path+currss+'finger.jpg',mimetype='image/gif')
@app.route('/app_upload_finger',methods=['POST'])
def app_upload_finger():
    global finger_result  
    filestr = request.files['image1'].read()
    npimg = np.fromstring(filestr, np.uint8)
    # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
    img1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    filestr = request.files['image2'].read()
    npimg = np.fromstring(filestr, np.uint8)
    # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
    img2 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    finger_result=fingerprint_matching(img1, img2)
    return jsonify(
        stt='Done')
@app.route('/app_finger_result',methods=['GET'])
def app_finger_result():
    global finger_result    
    return jsonify(
        stt=str(finger_result))

if __name__ == '__main__':
    import os
    HOST = '0.0.0.0'
    try:
        PORT = int(os.environ.get('SERVER_PORT', '56788'))
        lastss=server_init()
    except ValueError:
        PORT = 56788
        currss=server_init()
    app.run(HOST, PORT)
