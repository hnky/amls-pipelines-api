#!/usr/bin/env python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import keras
import tensorflow as tf
from keras.models import model_from_json
import cv2
import json
import numpy as np
import os
import base64
import urllib

loaded = False
app = Flask(__name__)
api = Api(app)

class SimpsonsApi(Resource):
    
    def __init__(self):
        global loaded
        global loaded_model
        print("run init")
        if loaded == False:
            print("--> Start - Loading Model")
            model_root = 'model' 
            model_file_json = os.path.join(model_root, 'simple_model.json')
            model_file_h5 = os.path.join(model_root, 'simple_model.h5')

            json_file = open(model_file_json, 'r') 
            loaded_model_json = json_file.read()
            json_file.close()

            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights(model_file_h5)  
            loaded = True
            print("--> End - Loading Model")     
    
    def post(self):
        global loaded_model
        try:
            url = request.get_json()['url']
            urllib.request.urlretrieve(url, filename="tmp.jpg")

            pic_size = 64
            image = cv2.imread("tmp.jpg")
            pic = cv2.resize(image, (pic_size,pic_size))
            data = pic.reshape(1, pic_size, pic_size,3)
            a = loaded_model.predict(data)[0]

            map_characters = {0:"marge_simpson", 1: "homer_simpson" }
            text = sorted(["{:s} : {:.1f}%".format(map_characters[k].split("_")[0].title(), 100*v) for k,v in enumerate(a)], key=lambda x:float(x.split(":")[1].split("%")[0]), reverse=True)[:3]        
            os.remove("tmp.jpg")

            return json.dumps(text)
        except AssertionError as error:
            print(error)  

api.add_resource(SimpsonsApi, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
