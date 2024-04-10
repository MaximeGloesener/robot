import time
import picamera
import torch
#from ultralytics import YOLO
with picamera.PiCamera() as camera:
    camera.start_preview()
    camera.capture('image8.jpg')
    camera.stop_preview()