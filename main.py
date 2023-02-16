'''
2022.12.29
press 'I' -> camselect -> QR code detection -> iv level detection

'''


import socket
from socket import *

import os
import numpy as np
import cv2 as cv
import numpy as np  
import argparse

import AdapterBoard
import inference
import object_detection


parser = argparse.ArgumentParser(description='Argparse Tutorial')
parser.add_argument('--p_id', type=str)
parser.add_argument('--d_id', type=str)
parser.add_argument('--threshold', type=int)

args = parser.parse_args()

patient_ID = args.p_id
drug_ID = args.d_id
threshold = args.threshold


CAM_0_image = "CAM_00.jpg"
CAM_1_image = "CAM_01.jpg"
CAM_2_image = "CAM_02.jpg"


Arducam_adapter_board = AdapterBoard.MultiAdapter()

# CAM selection

while True:
    print("start")    
    
    Arducam_adapter_board.init(448,448,0)
    pred_CAM_0 = inference.inference(CAM_0_image)
    print(pred_CAM_0)
    
    Arducam_adapter_board.init(448,448,1)
    pred_CAM_1 = inference.inference(CAM_1_image)
    print(pred_CAM_1)
    
    Arducam_adapter_board.init(448,448,2)
    pred_CAM_2 = inference.inference(CAM_2_image)
    print(pred_CAM_2)
    
    
    print("Please press 'I' key!")
    keycode = cv.waitKey(5000)
    
    if keycode == ord('i') or keycode == ord('I'):
        if pred_CAM_0 == 1:
            selected_CAM = 0
        elif pred_CAM_1 == 1:
            selected_CAM = 1
        elif pred_CAM_2 == 1:
            selected_CAM = 2
        #dele .jpg!!!!!!!
        cv.destroyAllWindows()
        os.remove(CAM_0_image)
        os.remove(CAM_1_image)
        os.remove(CAM_2_image)
        
        break
    
    elif keycode == 27:
        print("System shutdown!")
        exit()
    
   
print("'I' key is pressed.")
print("selected CAM number is ", selected_CAM)    


# QR-code detection(Patient_ID, Drug_ID)

count = 0

while True:
    if selected_CAM == 0:
        Arducam_adapter_board.init(448,448,0)
        qr_data = Arducam_adapter_board.QRcode_Reader(448,448,0)
        
        if qr_data == 1:
            print('QR code is not detected')
            continue
        else:
            p_id = qr_data[6:12]
            drug_id = qr_data[-6:]
            
            if p_id == patient_ID and drug_id == drug_ID:
                print('"match!"')
                break
            else:
                print('"mismatch!"\n please check!')
                count += 1
                
                if count == 5:
                    print('system shutdown')
                    exit()
                
                continue
    
    elif selected_CAM == 1:
        Arducam_adapter_board.init(448,448,1)
        qr_data = Arducam_adapter_board.QRcode_Reader(448,448,1)
        
        if qr_data == 1:
            print('QR code is not detected')
            continue
        else:
            p_id = qr_data[6:12]
            drug_id = qr_data[-6:]
            
            if p_id == patient_ID and drug_id == drug_ID:
                print('"match!"')
                break
            else:
                print('"mismatch!"\n please check!')
                count += 1
                
                if count == 5:
                    print('system shutdown')
                    exit()
                
                continue            
            
    
    elif selected_CAM == 2:
        Arducam_adapter_board.init(448,448,2)
        qr_data = Arducam_adapter_board.QRcode_Reader(448,448,2)
        
        if qr_data == 1:
            print('QR code is not detected')
            continue
        else:
            p_id = qr_data[6:12]
            drug_id = qr_data[-6:]
            
            if p_id == patient_ID and drug_id == drug_ID:
                print('"match!"')
                break
            else:
                print('"mismatch!"\n please check!')
                count += 1
                
                if count == 5:
                    print('system shutdown')
                    exit()
                
                continue
        
print('succeed!')

# IV level detection

while True:
    if selected_CAM == 0:
        Arducam_adapter_board.init(448,448,0)
        object_detection.ObjectDetector(CAM_0_image,0,threshold)
        keycode = cv.waitKey(100)
        
        if keycode == 27:
            break        
        
    elif selected_CAM == 1:
        Arducam_adapter_board.init(448,448,1)
        object_detection.ObjectDetector(CAM_1_image,1,threshold)
        keycode = cv.waitKey(100)
        
        if keycode == 27:
            break
        
    elif selected_CAM == 2:
        Arducam_adapter_board.init(448,448,2)
        object_detection.ObjectDetector(CAM_2_image,2,threshold)
        keycode = cv.waitKey(100)
        
        if keycode == 27:
            break
        
print('complete!')