# Finding-Object-by-Robotic-Arm
Dependencies  

OpenCV The Open Computer Vision library, in the form of python, was used to perform image parsing and analysis. This was used to apply a masking filter to each image, then parse each image for the contours of the marker / target. 

Numpy The Numerical Python (Numpy) library was used to provide advanced array and matrix functionality for the mathematics used in the program. In particular, the arrays were used for creating and passing the necessary RGB (in this instance, BGR) vectors for creating the appropriate mask.  

Access  

The Python program has been designed to run at the allocated hours of each member of Team 4 automatically (See below for a time table). It first starts by retrieving the system time of the executing host and compares it to the hard-coded times for each member. If the system time does not coincide with members' time, the program will inform the user through Standard Output and close. Otherwise, the program will continue with the Execution Procedure.

Function Definitions 

readResponse() 
Takes the encoded response from the server after issuing a command and parses through the encoded white-space characters for more a more user-friendly report.  getCoords(output) Given the output from the server, it parses through the data to find the X, Y, and Z co-ordinates. 

sendAJMA() 
Sends the Angular commands to the server to move the arm. After issuing, it acquires the resulting X, Y, and Z co-ordinates from the parsed return output.  

sendCapture() 
Sends the capture command to the server and prints the response. 

find_marker(image) 
Given an input image, the function parses over each pixel, applying a mask. After massaging the data, it attempts to find contours within the image to find a target marker (for example, a piece of paper).

download_image(url, filename) 
Issues a HTTP request for an image.  rawCommand(givenData) Parses through the encoded response from the server and makes it more user-friendly. 

printData()
Does the actual printing of parsed data for the user's benefit.

downloadCheckImage()
First, it attempts to download the latest image from the server and reports any errors it encounters. Then, it parses the image for the marker if possible and displays the image to the user.

testCom()
With an initial list of commands for the arm, it proceeds to iterate through them while checking each image for the marker/box. After locating it, it proceeds to center the camera horizontally on the box and then vertically. After having centered the camera on the box, it will proceed to use forward kinematics to calculate the box's location. 

Execution Procedure 

The program proceeds to first authenticate with the R12 server. On success, it proceeds to call on the primary driver, testComm, to find the box. This process then instructs the arm for move, capture an image, downloads the image, and parses it for the target. All the while, reporting all pertinent data to the user for diagnostics purposes.
