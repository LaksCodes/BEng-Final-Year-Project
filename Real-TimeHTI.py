########################
##Imports

import TrackHand

import sys
import os
import numpy as np
import cv2
import math
import time
import mouse
import keyboard
import win32api
import win32con
import screeninfo
import collections
import pycaw
import speech_recognition
import threading
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading
import concurrent.futures


##########################

##Global Variables

global wScreen, hScreen
global overlayList
global mouseTrackFrame, menuFrame
global gap
global devices, interface, volume, volumeRange
global recog

##########################

##Initialisers/constants

wScreen, hScreen  = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

menuFrame = 60

gap = 145

smoothening = 5
plocx, plocy = 0,0
clocx, clocy = 0,0
last_action = ["None"]
last_gesture = []

#########################
##Initialise audio device variables

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
#minVolume, maxVolume = volumeRange[0], volumeRange[1]

recog =  speech_recognition.Recognizer()


##Initialise Overlay Images

class readOverlay():
  def __init__(self, path, position):
    self.path = path
    self.camera_img = cv2.imread(self.path)
    self.position= position

    self.imgHeight = self.camera_img.shape[0]
    self.imgWidth = self.camera_img.shape[1]




overlayPath = "OverlayImages"
readingFilesList = os.listdir(overlayPath)

overlayList = []

for x, path in enumerate(readingFilesList):
  overlayList.append(readOverlay(f'{overlayPath}/{path}', [x*gap,0]))

##Function to read through Settings.txt file (To open Settings must open openSettings.py)


def readSettings():
  global wVideo, hVideo, twoHandMode, allScreenMode, mainMouseFinger, secondaryMouseFinger, rightClickFinger, scrollFinger, volumeIncrements,mouseTrackFrame, showLandmarks,showFPS, showBoundaryBox, showClosedBox, Shortcut1, Shortcut2, Shortcut3, Shortcut4, Shortcut5, showVolumeBar
  with open('settings.txt', 'r') as s:
    lines = s.readlines()
    for line in lines:
      if "ResolutionWidth" in line:
        wVideo = int(line.split("-", 1)[1])
      if "ResolutionHeight" in line:
        hVideo = int(line.split("-", 1)[1])
      if "TwoHandMode" in line:
        twoHandMode = str(line.split("-",1)[1])
      if "AllScreenMode" in line:
        allScreenMode = str(line.split("-",1)[1])
      if "MainMouseFinger" in line:
        mainMouseFinger = int(line.split("-",1)[1])
      if "SecondaryMouseFinger" in line:
        secondaryMouseFinger = int(line.split("-",1)[1])
      if "RightClickFinger" in line:
        rightClickFinger = int(line.split("-",1)[1])
      if "ScrollFinger" in line:
        scrollFinger = int(line.split("-",1)[1])
      if "MouseTrackFrame" in line:
      	mouseTrackFrame = int(line.split("-",1)[1])
      if "VolumeIncrements" in line:
        volumeIncrements = int(line.split("-", 1)[1])
      if "ShowLandmarks" in line:
      	showLandmarks = str(line.split("-",1)[1])
      if "ShowFPS" in line:
      	showFPS = str(line.split("-")[1])
      if "ShowBoundaryBox" in line:
      	showBoundaryBox = str(line.split("-")[1])
      if "ShowClosedBox" in line:
      	showClosedBox = str(line.split("-")[1])
      if "Shortcut1" in line:
      	Shortcut1 = str(line.split("-")[1])
      if "Shortcut2" in line:
      	Shortcut2 = str(line.split("-")[1])
      if "Shortcut3" in line:
      	Shortcut3 = str(line.split("-")[1])
      if "Shortcut4" in line:
      	Shortcut4 = str(line.split("-")[1])
      if "Shortcut5" in line:
      	Shortcut5 = str(line.split("-")[1])
      if "ShowVolumeBar" in line:
      	showVolumeBar = str(line.split("-")[1])

##Function for mouse mode

def Mouse(camera_img, detect, hands, hn):
  global smoothening
  global plocx, plocy
  global clocx, clocy
  global last_action

  if hands:
    if twoHandMode == True:
      if len(hands == 2):
        if hands[0].LorR == "Right":
          leftHand = hands[1]
          rightHand = hands[0]
        elif hands[0] == "Left":
          leftHand = hands[0]
          rightHand = hands[1]

        leftFingers = detect.isFingersUp(camera_img, leftHand.rectangleScale, leftHand.id)
        rightFingers = detect.isFingersUp(camera_img, rightHand.rectangleScale, rightHand.id)
        cv2.circle(camera_img, (int(leftHand.centre[0]), int(leftHand.centre[1])), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(camera_img, (int(rightHand.centre[0]), int(rightHand.centre[1])), 10, (255, 0, 0), cv2.FILLED)
        
        ccox, ccoy = np.interp(rightHand.centre[0], (mouseTrackFrame, wVideo - mouseTrackFrame), (0,wScreen)), np.interp(rightHand.centre[1], (mouseTrackFrame, hVideo -mouseTrackFrame), (0, hScreen))
        clocx = plocx + (ccox-plocx)/ smoothening
        clocy = plocy + (ccoy - plocy)/ smoothening
        mouse.move(wScreen - clocx, clocy)
        plocx, plocy = clocx, clocy
        if len(last_action)<10:
          
          if rightFingers == [0,0,0,0,0]:
            mouse.click()
            last_action.append("left_click")
          
          elif leftFingers == [0,1,0,0,0]:
            mouse.click(button="right")
            last_action.append("right_click")

          elif leftFingers == [0,1,0,0,1]:
            mouse.wheel(-1)
            last_action.append("scroll_up")

          elif leftFingers == [0,1,1,0,1]:
            mouse.wheel()
            last_action.append("scroll_down")
        else:
          last_action=last_action[1:]
      
    else:
      fingers = detect.isFingersUp(camera_img, hands[0].rectangleScale, 0)
      cv2.rectangle(camera_img, (mouseTrackFrame,mouseTrackFrame),(wVideo - mouseTrackFrame, hVideo -mouseTrackFrame),(0,255,255))

      leftClick= detect.findDistance(mainMouseFinger, secondaryMouseFinger , hn, camera_img, drawCentre=True,draw=False)
      rightClick = detect.findDistance(secondaryMouseFinger, rightClickFinger, hn, camera_img,drawCentre=False,draw=False)
      fingerToPalmLength = detect.findDistance(secondaryMouseFinger, 5, hn, camera_img, drawCentre=False, draw = False)
      scrollFingerToPalm = detect.findDistance(scrollFinger, 13, hn, camera_img, drawCentre=False, draw = False)
      scrollFingerLength = detect.findDistance(scrollFinger, 12, hn, camera_img, drawCentre=False,draw=False)
      ccox, ccoy = np.interp(leftClick.cx, (mouseTrackFrame,wVideo - mouseTrackFrame), (0,wScreen)), np.interp(leftClick.cy, (mouseTrackFrame,hVideo - mouseTrackFrame), (0,hScreen))
      
      clocx = plocx + (ccox-plocx)/ smoothening
      clocy = plocy + (ccoy-plocy)/ smoothening
      mouse.move(wScreen-clocx, clocy)
      plocx, plocy = clocx, clocy

      if len(last_action)<10:

        if (leftClick.scaledLength < 1) and (tuple(fingers[2:]) == (1,1,1)):
          mouse.press(button="left")
          last_action.append("left_click_drag")


        elif leftClick.scaledLength < 1:
          cv2.circle(camera_img, (leftClick.x1,leftClick.y1), 5, (255, 255, 0), cv2.FILLED)
          cv2.circle(camera_img, (leftClick.x2,leftClick.y2), 5, (255, 255, 0), cv2.FILLED)
          mouse.click()
          last_action.append("left_click")


        elif (rightClick.scaledLength < 1) and (scrollFingerToPalm.scaledLength > 40):
          cv2.circle(camera_img, (rightClick.x1, rightClick.y1), 5, (255, 213, 0))
          cv2.circle(camera_img, (rightClick.x2, rightClick.y2), 5, (255, 213, 0))
          mouse.wheel()
          last_action.append("scroll_up")

        elif(rightClick.scaledLength < 1) and (fingers[3] == 0):
          cv2.circle(camera_img, (rightClick.x1, rightClick.y1), 5, (145, 50, 200))
          cv2.circle(camera_img, (rightClick.x2, rightClick.y2), 5, (145, 50, 200))
          mouse.wheel(-1)
          last_action.append("scroll_down")

        elif rightClick.scaledLength < 1:
          cv2.circle(camera_img, (rightClick.x2,rightClick.y2), 5, (153,0,0))
          mouse.click(button="right")
          last_action.append("right_click")
            #timestamps.append(time.time())

        elif last_action[-1] == "None":
          mouse.release()
        else:
          last_action.append("None")

      else:
        last_action=last_action[1:]


#Function for Media Mode


def Media(camera_img, detect, hands):
	global last_gesture
	minVolume, maxVolume = volumeRange[0], volumeRange[1]
	if hands:
		fingers = detect.isFingersUp(camera_img, hands[0].rectangleScale, 0)
		if fingers == [0,0,0,0,0] and last_gesture != [0,0,0,0,0]:
			win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
			last_gesture = fingers

		elif fingers == [0,1,1,0,0] and last_gesture != [0,1,1,0,0]:
			win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0 , win32con.KEYEVENTF_EXTENDEDKEY, 0)     
			last_gesture = fingers
    
		elif fingers == [0,1,0,0,0] and last_gesture != [0,1,0,0,0]:
			win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0 , win32con.KEYEVENTF_EXTENDEDKEY, 0)
			last_gesture = fingers
    
		elif fingers == [1,1,0,0,0]:
			volumeLine  = detect.findDistance(4,8,0, camera_img, drawCentre=False,draw=True)
			vol = volumeIncrements * round (volumeLine.scaledLength/volumeIncrements)
			col = np.interp(vol, [0, 100], [0, 255])
			cv2.line(camera_img, (volumeLine.x1, volumeLine.y1), (volumeLine.x2,volumeLine.y2), (0, col, col), 3)

			volume.SetMasterVolumeLevelScalar(vol/100, None)
			if volumeLine.scaledLength<1:
				cv2.circle(camera_img, (volumeLine.x1, volumeLine.y1), 10, (0, 0, 255), cv2.FILLED)
				cv2.circle(camera_img, (volumeLine.x2, volumeLine.y2), 10, (0, 0, 255), cv2.FILLED)
		if fingers[4] == 1:
			last_gesture = fingers
		else:
			last_gesture = fingers

#Function for Speech Recognition

def SpeechRecognition():
	global text
	with speech_recognition.Microphone() as mic:
		recog.adjust_for_ambient_noise(mic, duration=0.1)

		text = recog.listen(mic)
		try:
			text = recog.recognize_google(text)
		except:
			print("Nothing heard")

#Function for Shortcuts (Error when passing Shortcut variables)

def Shortcuts(camera_img, detect, hands):
	global last_gesture
	if hands:
		fingers = detect.isFingersUp(camera_img, hands[0].rectangleScale, 0)
		if fingers == [1,0,0,0,0] and last_gesture != [1,0,0,0,0]:
			keyboard.send("alt+tab")
		if fingers == [0,1,0,0,0] and last_gesture != [0,1,0,0,0]:
			keyboard.send("ctrl+shift")
		if fingers == [0,0,1,0,0] and last_gesture != [0,0,1,0,0]:
			keyboard.send("F11")
		if fingers == [0,0,0,1,0] and last_gesture != [0,0,0,1,0]:
			keyboard.send("F2")

##Main function

def main():
	global currentMode
	readSettings()
	presentTime = 0
	currentTime = 0
	video_object = cv2.VideoCapture(0)
	video_object.set(3,wVideo)
	video_object.set(4,hVideo)
	detect = TrackHand.handDetection()

	currentMode = "NO MODE ACTIVATED"

	heardText = False

	while True:
		success, camera_img = video_object.read()
		camera_img, hands = detect.drawHands(camera_img)

		for icon in overlayList:
			iconHeight = icon.imgHeight
			iconWidth =  icon.imgWidth
			posx, posy = icon.position
			camera_img[posy: posy + iconHeight, posx: posx + iconWidth] = icon.camera_img

		if hands:
			menuNav = detect.findDistance(8,12,0, camera_img,drawCentre=False, draw=False)
			menuX, menuY = hands[0].landmarksList[12][1], hands[0].landmarksList[12][2]
			if menuFrame < menuX < wVideo- menuFrame and menuFrame < menuY < hVideo - menuFrame:

				if currentMode == "MOUSE":
					Mouse(camera_img, detect, hands, hn=0)

				elif currentMode == "MEDIA":
					Media(camera_img, detect, hands)

				elif currentMode == "SHORTCUTS":
					Shortcuts(camera_img, detect, hands)
			else:

				if (0 < menuX < menuFrame and 0 < menuY <menuFrame) and (menuNav.scaledLength < 2):
					os.system('wmic process where name="TabTip.exe" delete')
					os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")

  
				elif gap < menuX < gap + menuFrame and 0 < menuY < menuFrame and (menuNav.scaledLength < 2):
					#print("mouse button")
					currentMode = "MEDIA"
  
				elif 2*gap < menuX < 2*gap + menuFrame and 0 < menuY < menuFrame and (menuNav.scaledLength < 2):
					currentMode = "MOUSE"
  
				elif 3*gap < menuX < 3*gap + menuFrame and 0 < menuY < menuFrame and (menuNav.scaledLength < 2):
					#print("shortcuts")
					currentMode = "SHORTCUTS"

				elif 4*gap< menuX < 4*gap + menuFrame and 0 < menuY < menuFrame and (menuNav.scaledLength < 2):
					try:
						thread2 = threading.Thread(target=SpeechRecognition)
						thread2.start()
						thread2.join()
						keyboard.write(str(text), delay=0.01)
					except:
						currentMode = "Speech not recognised"
		else:
			currentMode= "NO MODE ACTIVATED"

		cv2.putText(camera_img, currentMode, (60, (int(hVideo - 35))), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
		cv2.rectangle(camera_img, (menuFrame, menuFrame), (wVideo - menuFrame, hVideo - menuFrame), (124,12,89))
		cv2.imshow("Image", camera_img)
		cv2.waitKey(1)

if __name__ == "__main__":
	thread1 = threading.Thread(target=main)
	thread1.start()
