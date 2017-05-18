from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


car_hc = cv2.CascadeClassifier('cars.xml')
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=camera.resolution)
bgs = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
opMorph = np.ones((4,4),np.uint8)
clMorph = np.ones((4,4),np.uint8)

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

	fgmask = bgs.apply(image)
	
	_, imBin=cv2.threshold(fgmask, 200, 255, cv2.TRESH_BINARY)
	
	fgmask = cv.morphologyEx(imBin, cv2.MORPH_OPEN, opMorph)
	fgmask = cv2.morphologyEx(imBin, cv2.MORPH_CLOSE, clMorph)
	
    cars = car_hc.detectMultiScale(image, 1.1, 2)

    ncars = 0
    for (x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        ncars = ncars + 1
        print ncars    
    
    cv2.imshow("Frame", image)
	cv2.imshow("Background Subtraction", fgmask)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
