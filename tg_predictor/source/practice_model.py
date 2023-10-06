# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 02:05:38 2022

@author: arsko
"""

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Load the model
itogi = ['бабочка','курица','корова','собака','слон','лошадь','кошачий','овца','паук','белка']
model = load_model('keras_model.h5')

def predict_it(karta):
    #model = load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open(karta)
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    
    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    
    # run the inference
    prediction = model.predict(data)
    if max(prediction[0])> 0.95:
        return 'Я думаю, что это '+ itogi[np.argmax(prediction)]
    else:
        return 'Такое я не могу распознать('
