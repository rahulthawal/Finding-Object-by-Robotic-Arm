# Members:	Tyler Culp; Robert Finley; Rahul Thawal; Tamin Holm
# Class:	AI and Robotics
# Semester:	Spring 2015
# Team 4
# Project 1

# Use Python 2.7
# To use a raw command, put the command used for the web 
# interface in quotes and use it as a parameter for rawCommand
# In this program, all large spaces are tab characters

# Each part of the project is contained in its own method
#
# TMOVETO Top:		1A
# TMOVETO Front:	1B
# AJMA Top:			2A
# AJMA Front:		`

import math
import httplib
from time import sleep
from datetime import datetime
import numpy as np
import cv2
import math
import urllib
import os
import imghdr
#import image

# Passwords
culp = ["TClyv6urx4wu7", "Tyler Culp"]
finley = ["RFkuh4lyaioym", "Robert Finley"]
thawal = ["RTbv6vl7ty5co", "Rahul Thawal"]
holm = ["THkgbku6tc4hxwy", "Tamin Holm"]

# Default's the user to a blank string because nobody has access except for the following times
user = ""
username = ""

hour = datetime.now().strftime('%H')
minute = datetime.now().strftime('%M')
if (hour == "12"):
	user = finley[0]
	username = finley[1]
elif (hour == "15"):
	user = thawal[0]
	username = thawal[1]
elif (hour == "17"):
	user = culp[0]
	username = culp[1]
elif (hour == "22"):
	user = holm[0]
	username = holm[1]

space = '%20';

# CAPTURE parameter
url = 'http://debatedecide.fit.edu/robot/' # the url
filenumber = 1001 # Just the number, no extension
filename = ""
extension = '.bmp' # the extension for the file
data = ""

sleepTime = 1


# AJMA Parameters
aHand = 0
aWrist = 0
aElbow = 0
aShoulder = 0
aWaist = 0

(xarm, yarm, zarm) = (0, 0, 0)
	
# Read the HTML response from the server
def readResponse():
	global data
	global lastResponse
	print(data.replace('%20', " "))
	sleep (sleepTime)
	try:
		res = conn.getresponse();
		lastResponse = res.read()
	except:
		print "bad status"
		lastResponse = "X=0 Y=0 Z=0 (C=0)"
		
	sleep (sleepTime)
	return lastResponse

def getCoords(output):
	xindex = output.find("X=")
	yindex = output.find(" Y=")
	zindex = output.find(" Z=")
	endIndex = output.find(" (C=")
	xcoord = output[xindex+2 : yindex]
	ycoord = output[yindex+3 : zindex]
	zcoord = output[zindex+3 : endIndex]
	
	print ("%s %s %s" % (xcoord, ycoord, zcoord))
	return (int(xcoord), int(ycoord), int(zcoord))
	
def sendAJMA():
	global xarm
	global yarm
	global zarm
	data = "%i%s%i%s%i%s%i%s%i%s%s" % (aHand, space, aWrist, space, aElbow, space, aShoulder, space, aWaist, space, 'AJMA')
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	(xarm, yarm, zarm) = getCoords(readResponse())

def sendCapture():
	data = "%i%sCAPTURE" % (filenumber, space)
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()	

def find_marker(image):
	# loop over the boundaries
	bil = cv2.bilateralFilter(image,9,75,75)

	# create NumPy arrays from the boundaries
	lower = np.array([10, 30, 10])   #for BGR
	upper = np.array([250, 200, 55]) #for BGR       
	       
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(bil, lower, upper)
	output = cv2.bitwise_and(bil, bil, mask = mask)
	#cv2.imshow("mask", mask)
	#cv2.waitKey(0)		
	
	edged = cv2.Canny(mask, 5, 300)
	#cv2.imshow("edged", edged)
	#cv2.waitKey(0)
	
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	list = []
	for i in cnts:
		list.append(cv2.approxPolyDP(i, 20, True))
	
	if (list):
		c = max(list, key = cv2.contourArea)
		#c = max(cnts, .1, True, key = cv2.approxPolyDP)
	else:
		return 0

	
	# compute the bounding  of the of the paper region and return it
	return cv2.minAreaRect(c)
	
def download_image(url, filename):
    image = urllib.URLopener()
    image.retrieve(url, filename)
	
def rawCommand(givenData):
	global data
	data = givenData.replace(' ', space)
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def printData():
	global data
	data = data.replace('%20', " ")
	print (data)

def downloadCheckImage():
	global filenumber
	global filename
	global finalFilename
	
	sleep(1)
	#Download the image
	try:
	    filename = str(str(filenumber) + extension)
	    full_url = str(url + filename)
	    sleep(1)
	    download_image(full_url, filename)
	except IOError: # error handling
	    errors += 1
	    print str("FileIO Error: " + ' ' + filename + ' ' + "could not be found")
			
	filenumber += 1
	print("Downloaded %s" % filename)

	stats = os.stat(filename)
	imgSize = stats.st_size
	print "Image size: %s" % imgSize
	if (imgSize < 921650):
		print "failed"
		return (0, 0)
	

	if (imghdr.what(filename) != "bmp"):
		return (0, 0)
	
	# Check the image

	# initialize the list of images that we'll be using
	imagePath = filename

	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	image = cv2.imread(imagePath)
	
	marker = find_marker(image)

	if not marker:
		marker = ((0, 0), (0, 0), 0)

	# draw a bounding box around the image and display it
	#print marker
	foo = cv2.cv.BoxPoints(marker)
	box = np.int0(foo)
	cv2.drawContours(image, [box], -1, (0, 0, 255), 2)
	#print "box",box
	length = math.sqrt((box[0][0]-box[1][0]) ** 2 +(box[0][1]-box[1][1]) ** 2)
	width = math.sqrt((box[1][0]-box[2][0]) ** 2 +(box[1][1]-box[2][1]) ** 2)
	area = length * width

	center = ((box[0][0]+box[2][0])/2,(box[0][1]+box[2][1])/2)

	print "center",center
	print "area",area

	#cv2.imshow("image", image)
	#cv2.waitKey(0)
	sleep(.05)
	
	if (area > 30000):
	    print ("Area seems large enough")
	    finalFilename = filename
	return (area, center)
		
	
	
def testCom():
	global filenumber
	global filename
	global aHand
	global aWrist
	global aElbow
	global aShoulder
	global aWaist
	
	finalFilename = ""
	#First [-8000, 10000, 7500, 0, 0], [-8000, 10000, 6500, 0, 0], [-8000, 10000, 5500, 0, 0], [-8000, 10000, 4800, 0, 0], 
	#Last , [10000, -10000, -7500, 0, -7500], [10000, -10000, -6500, 0, -7500], [10000, -10000, -5500, 0, -7500], [10000, -10000, -4500, 0, -7500]
	
	comds = [[-8000, 9000, 8700, 0, 0], [-8000, 9000, 7500, 0, 0], [-8000, 9000, 6500, 0, 0], [-8000, 9000, 5800, 0, 0],
		[-8000, 9000, 8700, 0, -2500],
		 [-8000, 9000, 7500, 0, -2500], [-8000, 9000, 6500, 0, -2500],
		 [-8000, 9000, 5500, 0, -2500], [-8000, 9000, 8700, 0, -5000],
		 [-8000, 9000, 7500, 0, -5000], [-8000, 9000, 6500, 0, -5000],
		 [-8000, 9000, 5500, 0, -5000], [-8000, 9000, 8700, 0, -7550],
		 [-8000, 9000, 7500, 0, -7550], [-8000, 9000, 6500, 0, -7550],
		 [-8000, 9000, 5500, 0, -7550], [-8000, 9000, 8700, 0, -10450],
		 [-8000, 9000, 7500, 0, -10450], [-8000, 9000, 6500, 0, -10450],
		 [-8000, 9000, 5500, 0, -10450], [-8000, 9000, 8700, 0, -12500],
		 [-8000, 9000, 7500, 0, -12500], [-8000, 9000, 6500, 0, -12500],
		 [-8000, 9000, 5500, 0, -12500], [-8000, 9000, 8700, 0, -15000],
		 [-8000, 9000, 7500, 0, -15000], [-8000, 9000, 6500, 0, -15000],
		 [-8000, 9000, 5500, 0, -15000], [-8000, 9000, 8700, 0, -17250],
		 [-8000, 9000, 7500, 0, -17250], [-8000, 9000, 6500, 0, -17250],
		 [-8000, 9000, 5500, 0, -17250], [10000, -9000, -8700, 0, 0],
		 [10000, -9000, -7500, 0, 0], [10000, -9000, -6500, 0, 0],
		 [10000, -9000, -5500, 0, 0], [10000, -9000, -8700, 0, -2500],
		 [10000, -9000, -7500, 0, -2500], [10000, -9000, -6500, 0, -2500],
		 [10000, -9000, -5500, 0, -2500], [10000, -9000, -8700, 0, -5000],
		 [10000, -9000, -7500, 0, -5000], [10000, -9000, -6500, 0, -5000],
		 [10000, -9000, -5500, 0, -5000]]

	xc = 0
	yc = 0
	a = 0
	
	# Phase 1: Locate the box
	for com in comds:
		aHand = com[0]
		aWrist = com[1]
		aElbow = com[2]
		aShoulder = com[3]
		aWaist = com[4]
		sendAJMA()
		
		sendCapture()

		(a, (xc, xy)) = downloadCheckImage() 
		
		if (a >= 40000):
			break
	
	
	# Phase 2: Center the image (horizontally)
	while (xc < 300 or xc > 350):
		if (xc < 200):
			aWaist -= 1000
		elif (xc > 400):
			aWaist += 1000
		elif (xc < 300):
			aWaist -= 200
		else:
			aWaist += 200
			
		sendAJMA()
		sendCapture()
		
		(a, (xc, yc)) = downloadCheckImage()
		
	print ("Picture is centered horizontally")

	# Phase 2.5: Center the image (vertically)
	while (yc < 210 or yc > 260):
		#print yc
		if (yc < 140):
			if (aElbow >= 0):
				aElbow -= 400
			else:
				aElbow += 400   
		elif (yc > 300):
			if (aElbow >= 0):
				aElbow += 400
			else:
				aElbow -= 400
		elif (yc < 210):
			if (aElbow >= 0):
				aElbow -= 100
			else:
				aElbow += 100
		else:
			if (aElbow >= 0):
				aElbow += 100
			else:
				aElbow -= 100
			
		sendAJMA()
		sendCapture()
		
		(a, (xc, yc)) = downloadCheckImage()
		
	print ("Picture is centered vertically")

	# Phase 2: Center the image (horizontally)
	while (xc < 300 or xc > 350):
		if (xc < 200):
			aWaist -= 1000
		elif (xc > 400):
			aWaist += 1000
		elif (xc < 300):
			aWaist -= 200
		else:
			aWaist += 200
			
		sendAJMA()
		sendCapture()
		
		(a, (xc, yc)) = downloadCheckImage()
		
	print ("Picture is centered horizontally")

	# Phase 2.5: Center the image (vertically)
	while (yc < 210 or yc > 260):
		#print yc
		if (yc < 140):
			aElbow -= 400
		elif (yc > 300):
			aElbow += 400
		elif (yc < 210):
			aElbow -= 100
		else:
			aElbow += 100
			
		sendAJMA()
		sendCapture()
		
		(a, (xc, yc)) = downloadCheckImage()
		
	print ("Picture is centered vertically\r\n\r\n")

	# Phase 4: Calculate the box's locations

	aElbow = (aElbow/100*math.pi/180)

	
	Dbox = ((558+(250*math.cos(aElbow)))/math.tan(aElbow))+(250*math.sin(aElbow))	
	Xbox = xarm * Dbox/(250*math.sin(aElbow))
	Ybox = yarm * Dbox/(250*math.sin(aElbow))

	print ("Dbox: %s" % Dbox)
	print ("Xbox: %s" % Xbox)
	print ("Ybox: %s" % Ybox)
	print ("Zbox: -1200")

	rawCommand("-6500 -9000 %s %s -1100 TMOVETO" % (Xbox, Ybox))




# Main
if (username != ""):
	#Sending commands, using the valid user's password password
	print ("Using %s's password...\r\n" % username)
	conn = httplib.HTTPConnection("debatedecide.org");
	testCom()
	print ("\r\nDone!")
else:
	print ("It's nobody's hour! The time is %s:%s" %(hour, minute))

