import cv2
import mediapipe as mp
import time
import math
import numpy as np
import os


class handDetection():
  def __init__(self, mode=False, maxHands = 2, modelComplexity=1, detectionCon=0.8, trackCon=0.5):
    self.mode = mode
    self.maxHands = maxHands
    self.modelComplex = modelComplexity
    self.detectionCon = detectionCon
    self.trackCon = trackCon

    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)         
    self.mpDraw = mp.solutions.drawing_utils
    self.fingerTips = [(4, "Thumb"), (8, "Index"), (12, "Middle"), (16, "Ring"), (20, "Pinky")]



  def drawHands(self, camera_img, handNo=0, draw=True):
    self.myHands = []
    camera_imgRGB = cv2.cvtColor(camera_img, cv2.COLOR_BGR2RGB)
    self.cam_video = self.hands.process(camera_imgRGB)

    if self.cam_video.multi_hand_landmarks:

      for hand, i in zip(self.cam_video.multi_handedness, range(len(self.cam_video.multi_hand_landmarks))):

        myHand = self.cam_video.multi_hand_landmarks[i]
        self.myHands.append(1)
        handType = hand.classification[0].index
        self.myHands[i] = self.HandProperties(camera_img, myHand, i, handType, draw=True)

    return camera_img, self.myHands


  def findDistance(self,p1, p2, hn, camera_img, r=5,t=3,drawCentre=False, draw=True):
    #if hn == True:
    #  x1, y1 = self.myHands[0].landmarksList[]
    try:
      x1, y1 = self.myHands[hn].landmarksList[p1][1:]
      x2, y2 = self.myHands[hn].landmarksList[p2][1:]
    except:
      pass
      #x1, y1 = self.myHands[]
    #print(x1, y1)
    #print(x2, y2)
    cx, cy = (x1 + x2) // 2, (y1 + y2)//2
    if draw:
      cv2.line(camera_img, (x1,y1), (x2, y2), (255, 0, 255), t)
      cv2.circle(camera_img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
      cv2.circle(camera_img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
      #cv2.circle(camera_img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
    if drawCentre:
      cv2.circle(camera_img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    length = math.hypot(x2 - x1, y2 - y1)
    scale = length/self.myHands[hn].rectangleScale
    #print(scale)
    scaledLength = np.interp(scale, [0.1,0.6], [0,100])

    dist = self.distancebetween2points(camera_img, [x1, y1, x2, y2, cx, cy], length, scale, scaledLength)

    return dist


  def isFingersUp(self, camera_img, rScale, hn):
    fingers = []

    if self.myHands:
      if self.myHands[hn].LorR == "Left":
        if self.myHands[hn].landmarksList[2][1] -10 > self.myHands[hn].landmarksList[4][1]:
          cbx1 = self.myHands[hn].landmarksList[4][1]
        else:
          cbx1 = self.myHands[hn].landmarksList[2][1] - 20
        
        if self.myHands[hn].landmarksList[17][1] +10 < self.myHands[hn].landmarksList[20][1]:
          cbx2 = self.myHands[hn].landmarksList[20][1] 
        else:
          cbx2 = self.myHands[hn].landmarksList[17][1] + 10

        cby1 = self.myHands[hn].landmarksList[9][2] - 30
        cby2 = self.myHands[hn].landmarksList[0][2] + 10

        cv2.rectangle(camera_img, (cbx1,cby1),(cbx2, cby2), (0,0,255), 2)
        for id in self.fingerTips:
          if ((self.myHands[hn].landmarksList[id[0]] [1]) > cbx1 
              and (self.myHands[hn].landmarksList[id[0]] [1]) < cbx2 
              and (self.myHands[hn].landmarksList[id[0]] [2]) > cby1 
              and (self.myHands[hn].landmarksList[id[0]] [2]) < cby2):
            fingers.append(0)
          else:
            fingers.append(1)

        return fingers

      elif self.myHands[hn].LorR == "Right":
        if self.myHands[hn].landmarksList[2][1] + 10> self.myHands[hn].landmarksList[4][1]:
          cbx1 = self.myHands[hn].landmarksList[2][1] + 20
        else:
          cbx1 = self.myHands[hn].landmarksList[4][1]# + 20

        
        if self.myHands[hn].landmarksList[17][1] - 10< self.myHands[hn].landmarksList[20][1]:
          cbx2 = self.myHands[hn].landmarksList[17][1] - 10
        else:
          cbx2 = self.myHands[hn].landmarksList[20][1]
        #if self.myHands[hn].landmarksList[9][2] <  
      

        cby1 = self.myHands[hn].landmarksList[9][2] - 30
        cby2 = self.myHands[hn].landmarksList[0][2] + 10


        cv2.rectangle(camera_img, (cbx1,cby1),(cbx2, cby2), (0,0,255), 2)
        cv2.circle(camera_img, (cbx2,cby2),5, (0,0,255), cv2.FILLED)
        for id in self.fingerTips:
          if ((self.myHands[hn].landmarksList[id[0]] [1]) < cbx1 
              and (self.myHands[hn].landmarksList[id[0]] [1]) > cbx2 
              and (self.myHands[hn].landmarksList[id[0]] [2]) > cby1 
              and (self.myHands[hn].landmarksList[id[0]] [2]) < cby2):
            fingers.append(0)
          else:
            fingers.append(1)

      return fingers

  class HandProperties():

    def __init__(self, camera_img, myHand, handId, LorR, draw):
      self.id = handId
      self.landmarksList = []
      self.mpDraw = mp.solutions.drawing_utils
      self.mpHands = mp.solutions.hands
      self.handId = "Hand"+str(handId)
      if LorR == 0:
        self.LorR = "Right"
      else:
        self.LorR = "Left"

      listX = []
      listY = []

      for id, lm in enumerate(myHand.landmark):
        height, width, channel = camera_img.shape
        centre_x, centre_y = int(lm.x* width), int(lm.y*height)
        listX.append(centre_x)
        listY.append(centre_y)
        self.landmarksList.append([id, centre_x, centre_y])
        if draw:
          cv2.circle(camera_img, (centre_x, centre_y), 5, (100, 50, 200), cv2.FILLED)
      if draw:
        self.mpDraw.draw_landmarks(camera_img, myHand, self.mpHands.HAND_CONNECTIONS)
        
      minX, maxX, minY, maxY = min(listX), max(listX), min(listY), max(listY)
      self.bbox = minX, minY, maxX, maxY
      self.hbox = maxY - minY
      self.lbox = maxX - minX
      self.rectangleScale = math.hypot(self.lbox, self.hbox)
      self.centre = ((self.bbox[0] + self.bbox[2])/2, (self.bbox[1] + self.bbox[3])/2)
      if draw:
        cv2.rectangle(camera_img, (self.bbox[0],self.bbox[1]),(self.bbox[2], self.bbox[3]), (0,255,0), 2)
        cv2.putText(camera_img, str(self.LorR), (self.bbox[0], (self.bbox[1] - 10)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

  class distancebetween2points():
    
    def __init__(self, camera_img, lineInfo, length, scale, scaledLength):
      self.x1 = lineInfo[0]
      self.y1 = lineInfo[1]
      self.x2 = lineInfo[2]
      self.y2 = lineInfo[3]
      self.cx = lineInfo[4]
      self.cy = lineInfo[5]
      self.length = length
      self.scale = scale
      self.scaledLength = scaledLength
      


