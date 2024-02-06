from SettingsUI import *
import sys
# import os

# CURRENT_PATH = os.path.join(os.getcwd())

# print(CURRENT_PATH)

class Settings(Ui_Settings):
	def __init__(self, window):
		self.setupUi(window)
		self.saveButton.clicked.connect(self.saveSettings)
		self.readSettings()
		self.mouseSpaceScaleSlider.valueChanged.connect(self.updateMouseSliderLabel)
		self.VolIncrementsSlider.valueChanged.connect(self.updateVolumeSliderLabel)


	def updateMouseSliderLabel(self,value):
		self.mouseSpaceScaleValuelabel.setText(str(value))


	def updateVolumeSliderLabel(self,value):
		self.volumeIncrementLabel.setText(str(value))



	def readSettings(self):
		with open('settings.txt', 'r') as s:
			lines = s.read().splitlines()
			for line in lines:
				if "ResolutionWidth" in line:
					wVideo = int(line.split("-", 1)[1])
				
				if "ResolutionHeight" in line:
					hVideo = int(line.split("-", 1)[1])

				if "TwoHandMode" in line:
					twoHandMode = str(line.split("-",1)[1])
					if twoHandMode == "False":
						self.dualHandModeCB.setChecked(False)
					elif twoHandMode == "True":
						self.dualHandModeCB.setChecked(True)
				
				if "AllScreenMode" in line:
					allScreenMode = str(line.split("-",1)[1])
					if allScreenMode == "False":
						self.mulipleMonitorCheckBox.setChecked(False)
					elif allScreenMode == "True":
						self.mulipleMonitorCheckBox.setChecked(True)
				
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
					self.mouseSpaceScaleValuelabel.setText(str(mouseTrackFrame))
					self.mouseSpaceScaleSlider.setValue(mouseTrackFrame)

				if "VolumeIncrements" in line:
					volumeIncrements = int(line.split("-", 1)[1])
					self.volumeIncrementLabel.setText(str(volumeIncrements))
					self.VolIncrementsSlider.setValue(volumeIncrements)

				
				if "ShowLandmarks" in line:
					showLandmarks = str(line.split("-",1)[1])
					if showLandmarks == "False":
						self.showLandmarksCB.setChecked(False)
					elif showLandmarks == "True":
						self.showLandmarksCB.setChecked(True)
				
				if "ShowFPS" in line:
					showFPS = str(line.split("-")[1])
					if showLandmarks == "False":
						self.FPSCB.setChecked(False)
					elif showLandmarks == "True":
						self.FPSCB.setChecked(True)
				
				if "ShowBoundaryBox" in line:
					showBoundaryBox = str(line.split("-")[1])
					if showBoundaryBox == "False":
						self.showBoundaryBoxCB.setChecked(False)
					elif showLandmarks == "True":
						self.showBoundaryBoxCB.setChecked(True)
					
				if "ShowClosedBox" in line:
					showClosedBox = str(line.split("-")[1])
					if showClosedBox == "False":
						self.showClosedHandBoxCB.setChecked(False)
					elif showClosedBox == "True":
						self.showClosedHandBoxCB.setChecked(True)
				
				if "Shortcut1" in line:
					Shortcut1 = str(line.split("-")[1])
					self.shortcutLineEdit1.setText(Shortcut1)
				
				if "Shortcut2" in line:
					Shortcut2 = str(line.split("-")[1])
					self.shortcutLineEdit2.setText(Shortcut2)
				
				if "Shortcut3" in line:
					Shortcut3 = str(line.split("-")[1])
					self.shortcutLineEdit3.setText(Shortcut3)

				if "Shortcut4" in line:
					Shortcut4 = str(line.split("-")[1])
					self.shortcutLineEdit4.setText(Shortcut4)

				if "Shortcut5" in line:
					Shortcut5 = str(line.split("-")[1])
					self.shortcutLineEdit5.setText(Shortcut5)

				if "ShowVolumeBar" in line:
					showVolumeBar = str(line.split("-")[1])
					if showVolumeBar == "False":
						self.volumeBarCB.setChecked(False)
					elif showVolumeBar == "True":
						self.volumeBarCB.setChecked(True)




	def saveSettings(self):
		with open('settings.txt', 'r') as s:
			lines = s.read().splitlines()
	
		with open('settings.txt', 'w') as s:
			# lines = s.read().splitlines()
			for line in lines:
				newline = line
				if "ResolutionWidth" in line:
					wVideo = int(line.split("-", 1)[1])
				
				if "ResolutionHeight" in line:
					hVideo = int(line.split("-", 1)[1])

				if "TwoHandMode" in line:
					twoHandMode = str(line.split("-",1)[0])
					##########self.HandModeCB is the "Dual Hand mode" checkbox, I want to be able to change the text after the "-" to False or True depending
					##########on whether the checkbox is True or False, To test, all you have to do is check the Dual Hand Mode box and then press save.
					if self.dualHandModeCB.isChecked() == True:
						newline = line.replace(line,str(twoHandMode + "-True"))
					else:
						newline = line.replace(line,str(twoHandMode + "-False"))
						
				if "AllScreenMode" in line:
					allScreenMode = str(line.split("-",1)[0])
					if self.mulipleMonitorCheckBox.isChecked() == True:
						newline = line.replace(line,str(allScreenMode + "-True"))
					else:
						newline = line.replace(line,str(allScreenMode + "-False"))
				
				# if "MainMouseFinger" in line:
				# 	mainMouseFinger = int(line.split("-",1)[1])
				
				# if "SecondaryMouseFinger" in line:
				# 	secondaryMouseFinger = int(line.split("-",1)[1])
				
				# if "RightClickFinger" in line:
				# 	rightClickFinger = int(line.split("-",1)[1])
				
				# if "ScrollFinger" in line:
				# 	scrollFinger = int(line.split("-",1)[1])
				
				# if "MouseTrackFrame" in line:
				# 	mouseTrackFrame = int(line.split("-",1)[1])
				# 	self.mouseSpaceScaleValuelabel.setText(str(mouseTrackFrame))
				# 	self.mouseSpaceScaleSlider.setValue(mouseTrackFrame)

				# if "VolumeIncrements" in line:
				# 	volumeIncrements = int(line.split("-", 1)[1])
				# 	self.volumeIncrementLabel.setText(str(volumeIncrements))
				# 	self.VolIncrementsSlider.setValue(volumeIncrements)

				
				if "ShowLandmarks" in line:
					showLandmarks = str(line.split("-",1)[0])
					if self.showLandmarksCB.isChecked() == True:
						newline = line.replace(line,str(showLandmarks + "-True"))
					else:
						newline = line.replace(line,str(showLandmarks + "-False"))
				
				if "ShowFPS" in line:  #UPDATES THE TEXT FILE BUT NOT THE GUI. NOT SURE WHY.
					showFPS = str(line.split("-")[0])
					if self.FPSCB.isChecked() == True:
						newline = line.replace(line,str(showFPS + "-True"))
					else:
						newline = line.replace(line,str(showFPS + "-False"))
				
				if "ShowBoundaryBox" in line:
					showBoundaryBox = str(line.split("-")[1])
					if self.showBoundaryBoxCB.isChecked() == True:
						newline = line.replace(line,str(showBoundaryBox + "-True"))
					else:
						newline = line.replace(line,str(showBoundaryBox + "-False"))
					
				if "ShowClosedBox" in line:  #UPDATES THE TEXT FILE BUT NOT THE GUI. NOT SURE WHY.
					showClosedBox = str(line.split("-")[1])
					if self.showClosedHandBoxCB.isChecked() == True:
						newline = line.replace(line,str(showClosedBox + "-True"))
					else:
						newline = line.replace(line,str(showClosedBox + "-False"))
				
				# if "Shortcut1" in line:
				# 	Shortcut1 = str(line.split("-")[1])
				# 	self.shortcutLineEdit1.setText(Shortcut1)
				
				# if "Shortcut2" in line:
				# 	Shortcut2 = str(line.split("-")[1])
				# 	self.shortcutLineEdit2.setText(Shortcut2)
				
				# if "Shortcut3" in line:
				# 	Shortcut3 = str(line.split("-")[1])
				# 	self.shortcutLineEdit3.setText(Shortcut3)

				# if "Shortcut4" in line:
				# 	Shortcut4 = str(line.split("-")[1])
				# 	self.shortcutLineEdit4.setText(Shortcut4)

				# if "Shortcut5" in line:
				# 	Shortcut5 = str(line.split("-")[1])
				# 	self.shortcutLineEdit5.setText(Shortcut5)

				if "ShowVolumeBar" in line:
					showVolumeBar = str(line.split("-")[1])
					if self.volumeBarCB.isChecked() == True:
						newline = line.replace(line,str(showVolumeBar + "-True"))
					else:
						newline = line.replace(line,str(showVolumeBar + "-False"))


				s.write(newline + "\n")





if __name__ == "__main__":

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()

	settingsUi = Settings(MainWindow)

	MainWindow.show()
	app.exec_()
