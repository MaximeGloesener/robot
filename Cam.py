# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 15:16:30 2023

@author: alex0
"""

import numpy as np 
import cv2 
from math import *

cropped = 0
thecase = 0
# angle pour les différents cas :  1x101 1x104  1x203 1x807 1x809 1x818
# 1 : point pour aucune des 2 équipes
# 2 : point pour les bleus
# 3 : point pour les 2 équipes
# 4 : point pour les jaunes
case1_ul = 35
case2_ul = 125
case3_ul = -145
case4_ul = -35

def findArucoMarkers(img, scale_percent, markerSize = 4, totalMarkers = 250, draw = True):
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(img)
    #print(markerIds)
    #print(markerCorners)
    
    if draw: 
        cv2.aruco.drawDetectedMarkers(img, markerCorners, markerIds)
        cv2.imwrite("D:/Eurobot/Camera/ArucoDetected.jpg",img)
        Aruco_draw = cv2.aruco.drawDetectedMarkers(img.copy(), markerCorners, markerIds) 
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        Aruco_draw = cv2.resize(Aruco_draw, dim, interpolation = cv2.INTER_AREA)
        #cv2.imshow('Aruco draw',cv2.aruco.drawDetectedMarkers(img.copy(), markerCorners, markerIds))
        cv2.imshow('Aruco draw',Aruco_draw)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return[markerCorners, markerIds]

image = cv2.imread("D:/Eurobot/Camera/Aruco7.jpg")
#print(image.shape[0]) #y : 1536
#print(image.shape[1]) #x : 2048

if cropped == 0 :
    arucoBoxes, ids = findArucoMarkers(image,scale_percent = 30) #sur toute l'image
else :
    image_cropped1 = image[500:1500,0:850]                 
    image_cropped2 = image[500:1500,800:1500]
    cv2.imshow('image_cropped1',image_cropped1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('image_cropped2',image_cropped2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    arucoBoxes, ids = findArucoMarkers(image_cropped2,scale_percent = 40)
    
if ids is not None :
    
    nbr_detected = len(ids)
    Q = 0
    for i in range(nbr_detected) :
        if ids[i] == 47 :
            Q = Q+1
            print("QR code "+str(Q)+" : ")
            V_y = (((arucoBoxes[i])[0])[3])[1]-(((arucoBoxes[i])[0])[0])[1]
            V_x = (((arucoBoxes[i])[0])[3])[0]-(((arucoBoxes[i])[0])[0])[0]
            #print(V_x)
            #print(V_y)
            Norm_V = sqrt(pow(V_x,2)+pow(V_y,2))
            #print (Norm_V)
            theta = acos(-V_y/Norm_V)
            if (((arucoBoxes[i])[0])[0])[0] > (((arucoBoxes[i])[0])[3])[0] :
                theta = -theta
            theta = np.rad2deg(theta)
            print("angle : "+ str(theta))
            if theta <= case1_ul and theta >= case4_ul :
                thecase = 1
                print("cas 1 (point pour aucune équipe)")
            elif theta > case1_ul and theta <= case2_ul :
                thecase = 2
                print("cas 2 (point pour les bleus)")
            elif theta >case2_ul or theta <= case3_ul :
                thecase = 3
                print("cas = 3 (point pour les 2 équipes)")
            else  :
                thecase = 4
                
                print("cas = 4 (point pour les jaunes)")
            
            






