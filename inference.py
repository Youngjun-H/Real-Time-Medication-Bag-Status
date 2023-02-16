import cv2 as cv 
import numpy as np

from PIL import Image

import tflite_runtime.interpreter as tflite

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


model_path = "./model/model_camselect_lite0.tflite"

interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get indexes of input and output layer

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

def inference(image_dir):
    data_dir = image_dir
    image = Image.open(data_dir)
    image = image.resize((224,224))
    image = np.array(image)
    image = image.astype(np.uint8)
    image = np.expand_dims(image, axis=0)
    
    # Step 2. Transform input data
    interpreter.set_tensor(input_index, image)
    # Step 3. Run inference
    interpreter.invoke()
    # Step 4. Interpret output
    pred = interpreter.get_tensor(output_index)

    #sum_time += time.time() - s_time
    pred = np.argmax(pred)

    return pred