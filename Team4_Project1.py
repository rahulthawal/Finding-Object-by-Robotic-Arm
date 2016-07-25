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
# AJMA Front:		2B

import math
import httplib
from time import sleep
from datetime import datetime

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
picNum = 1001

# TMOVETO Parameters
tHand = 0
tWrist = 0
tX = -4000
tY = 0
tZ = 1000

# AJMA Parameters
aHand = 0
aWrist = 0
aElbow = 0
aShoulder = 0
aWaist = 0

data = ""

sleepTime = 1

responseWanted = True

def calibrate():
	global picNum
	clearCaptures()
	# Moves the arm to the 4 corners originally recorded
	rawCommand("-6500 -300 -1800 -550 350 TMOVETO")
	
	rawCommand("-5700 -8500 -4250 -1700 550 TMOVETO")
	sendCAPTURE()
	picNum+=1
	rawCommand("-6900 -8500 -4550 -650 550 TMOVETO")
	sendCAPTURE()
	picNum+=1
	rawCommand("-6900 -8500 -4000 -450 550 TMOVETO")
	sendCAPTURE()
	picNum+=1
	rawCommand("-5700 -8500 -3700 -1550 550 TMOVETO")
	sendCAPTURE()
	picNum+=1
	
	rawCommand("-6500 -300 -1800 -550 350 TMOVETO")
		
	rawCommand("-6500 400 -2250 -950 -1150 TMOVETO")
	sendCAPTURE()
	picNum += 1
	rawCommand("-6500 400 -2450 -255 -1150 TMOVETO")
	sendCAPTURE()
	picNum += 1
	rawCommand("-6500 -425 -2250 -940 -1800 TMOVETO")
	sendCAPTURE()
	picNum += 1
	rawCommand("-6500 -425 -2450 -245 -1800 TMOVETO")
	sendCAPTURE()
	picNum += 1
	
	rawCommand("-6500 -300 -1800 -550 350 TMOVETO")
	
	sendHOME()
	clearCaptures()
	
	

# Read the HTML response from the server
def readResponse():
	global data
	print(data.replace('%20', " "))
	sleep (sleepTime)
	res = conn.getresponse();
	if (responseWanted == True):
		print res.read()
	else:
		res.read()
	sleep (sleepTime)
	
def sendTMOVETO():
	global data
	data = "%i%s%i%s%i%s%i%s%i%s%s" % (tHand, space, tWrist, space, tX, space, tY, space, tZ, space, 'TMOVETO')
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def sendHOME():
	global data
	data = "HOME"
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def sendCAPTURE():
	global data
	data = "%i%sCAPTURE" % (picNum, space)
	print ("Picture %i" % picNum)
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def clearCaptures():
	global data
	data = "-1%sCAPTURE" % space
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def sendAJMA():
	global data
	data = "%i%s%i%s%i%s%i%s%i%s%s" % (aHand, space, aWrist, space, aElbow, space, aShoulder, space, aWaist, space, 'AJMA')
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def rawCommand(givenData):
	global data
	data = givenData.replace(' ', space)
	conn.request("GET", "/robot.php?o=369&m=Y&p="+user+"&c="+data)
	readResponse()
	
def printData():
	global data
	data = data.replace('%20', " ")
	print (data)
	
def endProgram():
	exit()

# Set of commands for Part 1A
def sendTMOVETO_Top():
	global picNum
	global tHand
	global tWrist
	global tX
	global tY
	global tZ
	
	# Starting position
	
	c1 = [-5700, -8500, -4250, -1700, 550]
	c2 = [-6900, -8500, -4550, -650, 550]
	c3 = [-6900, -8500, -4000, -450, 550]
	c4 = [-5700, -8500, -3700, -1550, 550]
	
	tHand = c1[0]
	tWrist = c1[1]
	tX = c1[2]
	tY = c1[3]
	tZ = c1[4]
	
	rList = [[-4250, -4550, -1700, -650],
			[-4159, -4459, -1675, -617],
			[-4068, -4368, -1650, -584],
			[-3977, -4277, -1625, -551],
			[-3880, -4186, -1600, -518],
			[-3795, -4095, -1575, -485],
			[-3700, -4000, -1550, -450]]
	
	picNum = 1001
	
	rowCount = -1
	# Move across the rows
	
	for i in range(7):
		rowCount += 1
		tX = rList[rowCount][0]
		tY = rList[rowCount][2]
		tHand = c1[0]
		for j in range(11):
			sendTMOVETO()
			#sendCAPTURE()
			picNum += 1
			tY += (-1*(rList[rowCount][2]-rList[rowCount][3]))/10
			tX -= (rList[rowCount][0]-rList[rowCount][1])/10
			tHand -= (c1[0]-c2[0])/11
	

# Set of commands for Part 1B	
def sendTMOVETO_Front():
	global picNum
	global tHand
	global tWrist
	global tX
	global tY
	global tZ
	
	tmovetoCoords = [[-6500,400,-2250,-950,-1150], [-6500,400,-2260,-895,-1150], [-6500,400,-2270,-840,-1150], [-6500,400,-2280,-785,-1150], [-6500,400,-2290,-730,-1150], [-6500,400,-2300,-675,-1150], [-6500,400,-2330,-591,-1150], [-6500,400,-2360,-507,-1150], [-6500,400,-2390,-423,-1150], [-6500,400,-2420,-339,-1150], [-6500,400,-2450,-255,-1150],
					[-6500,308,-2250,-949,-1222], [-6500,308,-2261,-896,-1222], [-6500,308,-2272,-838,-1222], [-6500,308,-2283,-783,-1222], [-6500,308,-2294,-728,-1222], [-6500,308,-2305,-672,-1222], [-6500,308,-2335,-589,-1222], [-6500,308,-2363,-506,-1222], [-6500,308,-2392,-423,-1222], [-6500,308,-2421,-339,-1222], [-6500,308,-2450,-253,-1222],
					[-6500,216,-2250,-948,-1294], [-6500,216,-2262,-898,-1294], [-6500,216,-2274,-836,-1294], [-6500,216,-2286,-781,-1294], [-6500,216,-2298,-725,-1294], [-6500,216,-2311,-669,-1294], [-6500,216,-2339,-587,-1294], [-6500,216,-2366,-505,-1294], [-6500,216,-2395,-423,-1294], [-6500,216,-2422,-337,-1294], [-6500,216,-2450,-251,-1294],
					[-6500,124,-2250,-947,-1366], [-6500,124,-2263,-899,-1366], [-6500,124,-2276,-835,-1366], [-6500,124,-2289,-779,-1366], [-6500,124,-2303,-723,-1366], [-6500,124,-2316,-667,-1366], [-6500,124,-2344,-586,-1366], [-6500,124,-2370,-505,-1366], [-6500,124,-2397,-422,-1366], [-6500,124,-2423,-337,-1366], [-6500,124,-2450,-248,-1366],
					[-6500,32,-2250,-946,-1438], [-6500,32,-2264,-901,-1438], [-6500,32,-2278,-833,-1438], [-6500,32,-2292,-777,-1438], [-6500,32,-2307,-720,-1438], [-6500,32,-2322,-664,-1438], [-6500,32,-2348,-584,-1438], [-6500,32,-2373,-504,-1438], [-6500,32,-2399,-422,-1438], [-6500,32,-2424,-337,-1438], [-6500,32,-2450,-246,-1438],
					[-6500,-60,-2250,-945,-1510], [-6500,-60,-2265,-902,-1510], [-6500,-60,-2280,-831,-1510], [-6500,-60,-2296,-774,-1510], [-6500,-60,-2312,-718,-1510], [-6500,-60,-2327,-661,-1510], [-6500,-60,-2352,-582,-1510], [-6500,-60,-2376,-503,-1510], [-6500,-60,-2401,-422,-1510], [-6500,-60,-2425,-338,-1510], [-6500,-60,-2450,-2434,-1510],
					[-6500,-152,-2250,-944,-1582], [-6500,-152,-2266,-904,-1582], [-6500,-152,-2282,-829,-1582], [-6500,-152,-2300,-772,-1582], [-6500,-152,-2316,-715,-1582], [-6500,-152,-2333,-658,-1582], [-6500,-152,-2357,-580,-1582], [-6500,-152,-2380,-502,-1582], [-6500,-152,-2404,-422,-1582], [-6500,-152,-2426,-337,-1582], [-6500,-152,-2450,-242,-1582],
					[-6500,-244,-2250,-943,-1654], [-6500,-244,-2267,-905,-1654], [-6500,-244,-2284,-828,-1654], [-6500,-244,-2303,-770,-1654], [-6500,-244,-2321,-713,-1654], [-6500,-244,-2339,-656,-1654], [-6500,-244,-2361,-579,-1654], [-6500,-244,-2383,-502,-1654], [-6500,-244,-2406,-421,-1654], [-6500,-244,-2427,-336,-1654], [-6500,-244,-2450,-239,-1654],
					[-6500,-336,-2250,-942,-1726], [-6500,-336,-2268,-907,-1726], [-6500,-336,-2286,-826,-1726], [-6500,-336,-2306,-768,-1726], [-6500,-336,-2325,-710,-1726], [-6500,-336,-2344,-653,-1726], [-6500,-336,-2366,-577,-1726], [-6500,-336,-2386,-501,-1726], [-6500,-336,-2408,-421,-1726], [-6500,-336,-2428,-335,-1726], [-6500,-336,-2450,-237,-1726],
					[-6500,-425,-2250,-940,-1800], [-6500,-425,-2270,-882,-1800], [-6500,-425,-2290,-824,-1800], [-6500,-425,-2310,-766,-1800], [-6500,-425,-2330,-708,-1800], [-6500,-425,-2350,-650,-1800], [-6500,-425,-2370,-575,-1800], [-6500,-425,-2390,-500,-1800], [-6500,-425,-2410,-425,-1800], [-6500,-425,-2430,-350,-1800], [-6500,-425,-2450,-275,-1800],
]
	
	for i in range(110):
		tHand = tmovetoCoords[i][0]
		tWrist = tmovetoCoords[i][1]
		tX = tmovetoCoords[i][2]
		tY = tmovetoCoords[i][3]
		tZ = tmovetoCoords[i][4]
		sendTMOVETO()
		#sendCAPTURE()
		picNum += 1
	
	

# Set of commands for Part 2A	
def sendAJMA_Top():
	global picNum
	global aHand
	global aWrist
	global aElbow
	global aShoulder
	global aWaist
	
	jmaCoords = [[2366, 3070, 3036, 5635, -3900], [2298, 3058, 3074, 5607, -3853], [2233, 3049, 3102, 5586, -3805], [2172, 3043, 3120, 5573, -3757], [2115, 3041, 3127, 5567, -3709], [2061, 3041, 3125, 5569, -3661], [2011, 3045, 3113, 5578, -3613], [1964, 3052, 3091, 5594, -3565], [1922, 3063, 3058, 5618, -3518], [1882, 3076, 3015, 5650, -3470], [1847, 3093, 2961, 5690, -3423],
				[2242, 2960, 3384, 5378, -3905], [2175, 2949, 3420, 5351, -3856], [2112, 2941, 3446, 5332, -3808], [2050, 2935, 3462, 5320, -3759], [1994, 2933, 3469, 5314, -3710], [1940, 2934, 3467, 5316, -3661], [1889, 2937, 3456, 5324, -3612], [1843, 2944, 3436, 5339, -3563], [1798, 2953, 3406, 5362, -3514], [1758, 2966, 3366, 5391, -3466], [1721, 2981, 3316, 5428, -3418],
				[2131, 2861, 3702, 5141, -3910], [2064, 2850, 3736, 5115, -3860], [2000, 2842, 3762, 5096, -3810], [1940, 2837, 3778, 5084, -3759], [1882, 2834, 3786, 5078, -3709], [1829, 2835, 3785, 5079, -3658], [1778, 2838, 3775, 5087, -3608], [1730, 2844, 3756, 5101, -3558], [1686, 2853, 3727, 5122, -3507], [1644, 2864, 3690, 5150, -3458], [1606, 2879, 3644, 5185, -3408],
				[2027, 2769, 3996, 4921, -3915], [1961, 2759, 4030, 4895, -3863], [1898, 2751, 4055, 4876, -3812], [1838, 2746, 4072, 4864, -3760], [1780, 2743, 4080, 4858, -3708], [1726, 2744, 4079, 4858, -3656], [1675, 2747, 4070, 4865, -3604], [1627, 2752, 4052, 4879, -3552], [1581, 2760, 4025, 4899, -3500], [1539, 2771, 3990, 4926, -3449], [1500, 2785, 3945, 4959, -3397],
				[1927, 2680, 4287, 4701, -3921], [1860, 2669, 4321, 4675, -3868], [1798, 2662, 4347, 4656, -3815], [1738, 2657, 4364, 4643, -3761], [1680, 2654, 4372, 4637, -3707], [1625, 2654, 4372, 4637, -3654], [1574, 2657, 4363, 4644, -3600], [1525, 2662, 4346, 4657, -3546], [1480, 2670, 4321, 4676, -3493], [1437, 2680, 4287, 4702, -3440], [1397, 2693, 4244, 4734, -3387],
				[1843, 2605, 4532, 4515, -3926], [1777, 2595, 4566, 4489, -3871], [1713, 2587, 4591, 4470, -3816], [1653, 2582, 4608, 4457, -3761], [1596, 2580, 4617, 4450, -3705], [1542, 2580, 4617, 4450, -3650], [1490, 2582, 4609, 4457, -3595], [1441, 2587, 4592, 4469, -3539], [1395, 2595, 4567, 4488, -3484], [1352, 2605, 4534, 4514, -3430], [1311, 2617, 4492, 4546, -3375],
				[1756, 2528, 4789, 4318, -3933], [1689, 2517, 4823, 4292, -3876], [1627, 2510, 4849, 4272, -3819], [1567, 2505, 4866, 4259, -3762], [1509, 2502, 4875, 4252, -3705], [1454, 2502, 4876, 4251, -3647], [1402, 2504, 4868, 4257, -3590], [1353, 2509, 4852, 4270, -3533], [1306, 2516, 4828, 4288, -3476], [1263, 2526, 4795, 4314, -3420], [1222, 2538, 4754, 4345, -3363]]
	
	for i in range(77):
		aHand = jmaCoords[i][0] * 2 * -1
		aWrist = jmaCoords[i][1] * 90 / 40
		aElbow = jmaCoords[i][2] * 90 / 60
		aShoulder = jmaCoords[i][3] * 90 / 84
		aWaist = jmaCoords[i][4] * 180 / 7280 * 10450 / 90
		sendAJMA()
		#sendCAPTURE()
		picNum += 1
	
	
# Set of commands for Part 2B	
def sendAJMA_Front():
	global picNum
	global aHand
	global aWrist
	global aElbow
	global aShoulder
	global aWaist
	
	jmaCoords = []
	
	for i in range(110):
		aHand = jmaCoords[i][0] * 2 * -1
		aWrist = jmaCoords[i][1] * 90 / 40
		aElbow = jmaCoords[i][2] * 90 / 60
		aShoulder = jmaCoords[i][3] * 90 / 84
		aWaist = jmaCoords[i][4] * 180 / 7280 * 10450 / 90
		sendAJMA()
		#sendCAPTURE()
		picNum += 1
	

# Neutral position to return to to avoid hitting the box
def neutralPositionTMOVETO():
	rawCommand("-6500 -8500 -1600 -550 600 TMOVETO")
	
def neutralPositionAJMA():
	rawCommand("-6500 -8500 -1600 -550 600 TMOVETO")
	
# Main controller, to handle startup, in-between stuff, and shutdown
def sendCommands():
	# Import global variables to allow for editing.
	global responseWanted
	
	# Startup
	#responseWanted = False
	clearCaptures()
	
	# First Part
	
	# TMOVETO Top
	neutralPositionTMOVETO()
	print ("Using TMOVETO commands for the Top of the box...")
	#sendTMOVETO_Top()
	
	# TMOVETO Front
	neutralPositionTMOVETO()
	print ("Using TMOVETO commands for the Front of the box...")
	sendTMOVETO_Front()
	
	neutralPositionTMOVETO()
	
	# Second Part
	
	# AJMA TOP
	neutralPositionAJMA()
	print ("Using AJMA commands for the Front of the box...")
	#sendAJMA_Top()
	
	# AJMA Front
	neutralPositionAJMA()
	print ("Using AJMA commands for the Front of the box...")
	#sendAJMA_Front()
	
	# Finishing up
	neutralPositionAJMA()
	print ("Returning Home")
	sendHOME()

	
def testCom():
	rawCommand("-6500 -300 -2000 -550 350 TMOVETO")	
	rawCommand("-6500 400 -2250 -950 -1150 TMOVETO")
	
	
	
# Main
if (username != ""):
	#Sending commands, using the valid user's password password
	print ("Using %s's password...\r\n" % username)
	conn = httplib.HTTPConnection("debatedecide.org");
	sendCommands()
	#calibrate()
	#testCom()
	print ("\r\nDone!")
else:
	print ("It's nobody's hour! The time is %s:%s" %(hour, minute))

