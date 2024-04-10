import time
import cv2
import numpy as np
from picamera2 import Picamera2, Preview
from math import *

thecase = 0

case1_ul = 35
case2_ul = 125
case3_ul = -145
case4_ul = -35

def findArucoMarkers(img, scale_percent, markerSize = 4, totalMarkers = 250, draw = True):
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary,parameters)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(img)
    return[markerCorners, markerIds]


picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (3280, 2464)
}, lores={"size": (640, 480)}, display="main")
picam.configure(config)
picam.start()
picam.capture_file("./test1.png")
picam.stop()

image = cv2.imread("./ARUCO7.png")

arucoBoxes, ids = findArucoMarkers(image,scale_percent = 40)

arucoboxes47 = []

for i in range (len(ids)):
    if ids[i] == 47:
        arucoboxes47.append(arucoBoxes[i]) 

arucoBoxes = sorted(arucoboxes47, key=lambda x:x[0][0][0])

if ids is not None :
    nbr_detected = len(arucoBoxes)
    Q = 0
    for i in range(nbr_detected):
        Q = Q+1
        print("QR code "+str(Q)+" : ")
        V_y = (((arucoBoxes[i])[0])[3])[1]-(((arucoBoxes[i])[0])[0])[1]
        V_x = (((arucoBoxes[i])[0])[3])[0]-(((arucoBoxes[i])[0])[0])[0]

        Norm_V = sqrt(pow(V_x,2)+pow(V_y,2))

        theta = acos(-V_y/Norm_V)

        if (((arucoBoxes[i])[0])[0])[0] > (((arucoBoxes[i])[0])[3])[0]:
            theta=-theta
        theta = np.rad2deg(theta)
        print("angle:"+ str(theta))

        if theta <= case1_ul and theta >= case4_ul:
            thecase=1
            print('cas 1 point pour aucune équipe')
        elif theta > case1_ul and theta <= case2_ul:
            thecase=2
            print('cas 2 point pour les bleus')
        elif theta > case2_ul or theta <= case3_ul:
            thecase=3
            print('cas = 3 point pour les 2 équipes')
        else:
            thecase=4
            print('cas 4 point pour les jaunes')
else :
    print("no aruco found")

# with picamera2.Picamera2() as camera:
#     camera.start_preview()
#     camera.capture("./test.png")
#     camera.stop_preview()