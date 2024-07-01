import time

import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np

cap = cv2.VideoCapture(0)

detector = PoseDetector()
ptime = 0
ctime = 0
color = (0,0,255)
dir = 0
push_ups = 0
while True:
    _, img = cap.read()
    img = detector.findPose(img)
    lmlst, bbox = detector.findPosition(img,draw=False)
    if lmlst:
        #print(lmlst)
        a1 = detector.findAngle(img, 12, 14, 16)
        a2 = detector.findAngle(img, 15, 13, 11)
        per_val1 = int(np.interp(a1, (85, 175), (100, 0)))
        per_val2 = int(np.interp(a2, (85, 175), (100, 0)))
        bar_val1 = int(np.interp(per_val1, (0, 100), (40+350, 40)))
        bar_val2 = int(np.interp(per_val2, (75, 175), (100, 0)))
        #print(per_val1)
        #1st bar
        cv2.rectangle(img, (570, bar_val1), (570 + 35, 40 + 350),color, cv2.FILLED)
        cv2.rectangle(img,(570,40),(570+35,40+350),(),3)
        #2nd bar
        cv2.rectangle(img, (35, bar_val2), (35 + 35, 40 + 350),color, cv2.FILLED)
        cv2.rectangle(img, (35, 40), (35 + 35, 40 + 350), (), 3)
        #bar 2%
        cvzone.putTextRect(img,f'{per_val2} %',(35,25),1.1,2,colorT=(255,255,255),colorR=color,border=3,colorB=())
        #bar 1%
        cvzone.putTextRect(img,f'{per_val1} %',(570,25),1.1,2,colorT=(255,255,255),colorR=color,border=3,colorB=())
        if per_val1 == 100 and per_val2 == 100:
            if dir == 0:
                push_ups +=0.5
                dir = 1
                color = (0,255,0)
        elif per_val1 == 0 and per_val2 == 0:
            if dir == 1:
                push_ups += 0.5
                dir = 0
                color = (0, 255, 0)
        else:
            color = (0,0,255)
        cvzone.putTextRect(img,f'Push_Ups : {int(push_ups)}',(209,35),2,2,colorT=(255,255,255),colorR=(255,0,0),border=3,colorB=())
        cvzone.putTextRect(img,'Left Hand', (15,350+80),1.4,2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())
        cvzone.putTextRect(img,'Right Hand',(495,350+80),1.4,2, colorT=(255, 255, 255), colorR=(255, 0, 0),border=3, colorB=())
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cvzone.putTextRect(img,f'FPS : {int(fps)}',(288,440),1.6,2,colorT=(255,255,255),colorR=(0,135,0),border=3,colorB=())
    cv2.imshow('Push-up Counter',img)
    if cv2.waitKey(1) == ord('q'):
        break
