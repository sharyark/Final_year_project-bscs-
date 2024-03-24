import cv2
import face_recognition as FR
import os 
import pickle as pk
from datetime import datetime
import time
from db import DBhelper
import threading

with open('train.pkl','rb') as f:
    names = pk.load(f)
    knownEncodings = pk.load(f)


db_ = DBhelper()
def attendance(name):
    db_.entrance(name)
    print('attendance is called..')
    print(name)

font=cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0) # making camera object
print("cam object is ",cam)
while True:
    ignore , frame = cam.read()
    faceLocations=FR.face_locations(frame)
    unknownEncodings=FR.face_encodings(frame,faceLocations)
    for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
        top,right,bottom,left=faceLocation
        cv2.rectangle(frame,(left+10,top-10),(right,bottom),(255,0,0),3)
        name='Unknown Person'
        matches=FR.compare_faces(knownEncodings,unknownEncoding)
        if True in matches:
            matchIndex=matches.index(True)
            name=names[matchIndex]
        elif name=='Unknown Person':
            print(name)
            now = datetime.now()
           
    

        cv2.putText(frame,name,(left,top),font,.75,(0,0,255),2)
    
    cv2.imshow('My Faces',frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()




































