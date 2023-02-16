import RPi.GPIO as gp
import os
import cv2 as cv 
import numpy as np
import pyzbar.pyzbar as pyzbar


class MultiAdapter:
    camNum = 3
    adapter_info = {   "A":{   "i2c_cmd":"i2cset -y 0 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
                        "B":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
                        "C":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                     }
    camera = cv.VideoCapture(0)
    #cmd="raspistill -o /home/pi/image_Sp0%d.jpg"%cam
    width = 448
    height = 448
   
    def __init__(self):
       gp.setwarnings(False)
       gp.setmode(gp.BOARD)
       gp.setup(7, gp.OUT)
       gp.setup(11,gp.OUT)
       gp.setup(12,gp.OUT)

    def choose_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        os.system(channel_info["i2c_cmd"]) # i2c write
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])
    def select_channel(self,index):
        channel_info = self.adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])

    def init(self,width,height, cam):
                   
           self.height = height
           self.width = width
           self.i = cam
           
           self.choose_channel(chr(65+self.i)) 
           self.camera.set(3, self.width)
           self.camera.set(4, self.height)
           
           ret, frame = self.camera.read()          
           if ret == True:                   
               print("camera %s init OK" %self.i)
               
               array = np.full(frame.shape, (0, 15, 0), dtype=np.uint8)
               frame = cv.add(frame, array)
                   
               pname = "/home/pi/Desktop/model_final/CAM_0%s.jpg" %self.i
               wname = "CAM_0%s" %self.i
               
               #cv.line(frame, (0, 76), (224, 76), (0, 0, 255))
               
               cv.imshow(wname, frame)
               #cv.waitKey(0)
               cv.imwrite(pname, frame)
               #img = cv.imread(pname)
               cv.waitKey(100)                   
    
                
    def QRcode_Reader(self, width, height, cam):
        
            self.height = height
            self.width = width
            self.i = cam
           
            self.choose_channel(chr(65+self.i)) 
            self.camera.set(3, self.width)
            self.camera.set(4, self.height)               
            
            #check = 0
            
            ret, frame = self.camera.read()
            
            if ret == True:              
                array = np.full(frame.shape, (0, 15, 0), dtype=np.uint8)
                frame = cv.add(frame, array)
                   
                pname = "/home/pi/Desktop/model_final/CAM_0%s.jpg" %self.i
                wname = "CAM_0%s" %self.i
                
                # capture -> save -> load -> QR code detection
                cv.imwrite(pname, frame)
                img = cv.imread(pname)
                #cv.waitKey(50)
                    
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                decoded = pyzbar.decode(gray)    
                
                print(type(decoded))
                
                for d in decoded:
                    x, y, w, h = d.rect
                                        
                    barcode_data = d.data.decode("utf-8")
                    barcode_type = d.type
                    
                    print('barcode data:  ', barcode_data)

                    cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    #text = '%s (%s)' % (barcode_data, barcode_type)
                    text = 'IV bag_ID: %s' % barcode_data
                    cv.putText(img, text, (x-10, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                
                    wname = "CAM_0%s" %self.i                        
                    print(text)       
                    
                    cv.imshow(wname, img)
                    cv.waitKey(1000)
                    cv.destroyAllWindows()                                       
                    
                    return barcode_data
                
                return 1
                 
