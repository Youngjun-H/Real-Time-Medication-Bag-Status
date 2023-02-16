'''
2022.12.13
connect one cam -> data 
'''

import numpy as np

import cv2 as cv
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

model = './model/model_intergrated_efficientdet0.tflite'

enable_edgetpu = False
num_threads = 4

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

def ObjectDetector(image_dir, cam, threshold):
    #Image Load
    frame = cv.imread(image_dir)       
 
    # Initialize the object detection model
    base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)
    
    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    # Draw keypoints and edges on input image
    image = utils.visualize(frame, detection_result)

    print(detection_result)
    # Stop the program if the ESC key is pressed.        
    
    if len(detection_result.detections)==0:
        print('liquid is not detected!')
        cv.imshow('object_detector', image)
        
        
    else:
                    
        x = detection_result.detections[0].bounding_box.origin_y
        
        #select liquid level estimation formular
        if cam == 0:
            level = -2.37438e-5*pow(x,3) + 0.00437*pow(x,2) - 0.63342*x + 70
        elif cam == 1:            
            level = 2.863e-5*pow(x,3) - 0.00576*pow(x,2) - 0.72575*x + 146
        elif cam == 2:
            level = -1.01053e-5*pow(x,3) + 0.00443*pow(x,2) - 1.65056*x + 245       
        
        print('liquid_level : ', level)
        
        if level < threshold:
            print('alarm!   alarm!   alarm!   alarm!   alarm!   alarm!   alarm!   alarm!')
        
        cv.imshow('object_detector', image)