'''
2022.12.13
connect one cam -> data 
'''

import numpy as np
import argparse
import sys
from datetime import datetime
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 448) # 가로
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 448) # 세로

model = 'model/model_intergrated_efficientdet0.tflite'
enable_edgetpu = False
num_threads = 4

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

i = 0
level = []
alarm = [0 for i in range(10)]

while True:
    ret, frame = cam.read()
    
    if ret:        
        
        array = np.full(frame.shape, (0, 15, 0), dtype=np.uint8)
        frame = cv2.add(frame, array)        
        
        
        pname = "/home/pi/Desktop/data/test.jpg"
        
        #cv2.imwrite(pname, frame)
        #image = cv2.imread(pname)
        
        # Initialize the object detection model
        base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
        detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
        detector = vision.ObjectDetector.create_from_options(options)
        
        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)

        # Draw keypoints and edges on input image
        image = utils.visualize(frame, detection_result)
        
        cv2.imshow('object_detector', image)

        #print(detection_result)
        
        if len(detection_result.detections)==0:
            print('liquid is not detected!')
            #cv2.imshow('object_detector', image)
            key = cv2.waitKey(100)
            if key == 27:
                cv2.destroyAllWindows()
                break
            continue
        else:
            
            i+=1    #capture counting
            
            x = detection_result.detections[0].bounding_box.origin_y
            
            
            #a_500= 2.863e-5*pow(x,3) - 0.00576*pow(x,2) - 0.72575*x + 151.61965 #original
            a_500= 2.863e-5*pow(x,3) - 0.00576*pow(x,2) - 0.72575*x + 148
            #a_500= -0.00172*pow(x,3) + 0.60867*pow(x,2) - 72.25879*x + 2916.2926
            #a_1000 = -1.01053e-5*pow(x,3) + 0.00443*pow(x,2) - 1.65056*x + 249.08953 #original
            #a_1000 = -1.01053e-5*pow(x,3) + 0.00443*pow(x,2) - 1.65056*x + 245
            #a_100 = 1.74762e-5*pow(x,3) - 0.00397*pow(x,2) -0.20492*x + 73
            #a_100_1 = -2.37438e-5*pow(x,3) + 0.00437*pow(x,2) - 0.63342*x + 70
            
            
            print('Level_y : ', x)
            print('Residue : ', a_500, 'ml')
            
            level.append(a_500)
            
            threshold = 30
            
            if a_500 < threshold:
                #print('alarm      alarm      alarm      alarm      alarm      alarm      alarm      alarm      alarm      ')
                del alarm[0]
                alarm.append(1)
            else:
                del alarm[0]
                alarm.append(0)
            
            print(alarm)
            
            
            alarm_mean = np.mean(alarm)
            
            if alarm_mean == 1:
                print('alarm      alarm      alarm      alarm      alarm      alarm      alarm      alarm      alarm      ')
            
            #cv2.imwrite('result.jpg', image)
                            
            key = cv2.waitKey(100)
            if key == 27:
                cv2.destroyAllWindows()
                break
            #if i == 10:
             #   cv2.destroyAllWindows()
              #  break

#listSize = len(level)
#listSum = sum(level)
#listMean = listSum / len(level)

print('finish!')
#print(level)
#print('length : ', listSize)
#print('level mean : ', listMean)