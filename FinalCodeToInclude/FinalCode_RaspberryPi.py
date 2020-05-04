####################################################################################################################
# Main function
# Importing necessary functions
import RPi.GPIO as GPIO
import time
import numpy as np
import threading
import bluetooth
import time
import Adafruit_CharLCD as LCD
import serial
import sys
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
import pantilthat as pth
import argparse  # used for command line arguments
import signal
import cv2

# Keep track all global variables
# PROCESS 1
# All global variables below are assigned in process1, needed in process2
# Configuration-related (remember current config of car)
global rightIndex
global leftIndex
global sensor_N
global sensor_W
global sensor_S
global sensor_E
global sensor1
global sensor2
global sensor3
global sensor4
global config
global sensorPatch
# Remember which I/O pin is for which direction
global TRIG_N
global ECHO_N
global TRIG_W
global ECHO_W
global TRIG_S
global ECHO_S
global TRIG_E
global ECHO_E

# I/O pins of TRIG & ECHO for each ultrasonic sensor
global TRIG_sensor1
global ECHO_sensor1
global TRIG_sensor2
global ECHO_sensor2
global TRIG_sensor3
global ECHO_sensor3
global TRIG_sensor4
global ECHO_sensor4

# Global array for washer locations
global locs

# PROCESS 2
# Global variables - Assigned in process1, needed in process2
global rightIndex
global leftIndex
global sensor_N
global sensor_W
global sensor_S
global sensor_E
global config

# Global variables - Assigned in process2, needed in process1
# Keep track of whether time is within 75s
global STOP
# Keep track of distances from all 4 sensors
global distance1
global distance2
global distance3
global distance4
# Bluetooth global variables
global macAddress
macAddress="2015:10:195789"

# motor control
global motor
# patching mechanism
global PM
# Camera Vision System outputs
global panAngle
global tiltAngle
global washerFound

global TS  # switch to start trial
TS = 0  # initialize switch as OFF

# Main function that initializes bluetooth communication and begins processing after switch turned on
def main():
    # Declare board setup
    GPIO.setmode(GPIO.BCM)  # sets GPIO pin numbering
    # Remove warnings
    GPIO.setwarnings(False)

    # Initialize Serial communications
    Initialization()

    # Initialize Bluetooth
    while (success == 0):
        # First establish Bluetooth communication link with display station
        startComLink(macAddress)
        if (success == 1):
            break
        elif (success == 0):
            resetDisplay(macAddress)  # try resetting the display
            # try again to create communication link
    # Communication link now established!
    # Now begin processing code...
    while (TS == 0):  # waiting for switch to be turned on
        if (TS == 1):  # SWITCH TURNED ON, begin trial
   	        # Define threads
            thread_Process1 = threading.Thread(target=Process1)
            thread_Process2 = threading.Thread(target=Process2)
            thread_pan_tilt_tracking = threading.Thread(
                target=pan_tilt_tracking)
            # Start threads
            thread_Process1.start()
            thread_Process2.start()
            thread_pan_tilt_tracking.start()
            # This main function threads the two subprocesses and starts them both
            break  # break out of loop now that processing has been started

# Function for establishing Bluetooth communication link with display station
def startComLink(macAddress):
    # Flash team number three times
    try:
        for x in range(0, 3):
            # Flash team number
            sendMessageTo(macAddress, "x1")
            # Clear team number
            sendMessageTo(macAddress, 'xx')
        # Turn on buzzer
        sendMessageTo(macAddress, 'X1')
        # Wait 250 ms
        time.sleep(0.250)
        # Turn off buzzer
        sendMessageTo(macAddress, 'X0')
        # Sucessful
        success = 1
    except:
        # Something went wrong, communication link not established
        success = 0

    return success

# Function to reset communication with display station (if necessary)
def resetDisplay(macAddress):
    # To reset communication with the Display Station, send the character “Z” multiple times.
    # The Display Station will ignore all “Z” characters.
    # The first character to follow a “Z” will be considered the first character of a new two-character string command.

    # Number of times to send character "Z"
    num = 5
    for x in range(0, num):
        # Send "Z"
        sendMessageTo(macAddress, "Z")


# Main Function to be called
if __name__ == '__main__':
    main()  # call main function

####################################################################################################################
# Process 1:
def Process1():  # Process1
    # Global variables
    global rightIndex
    global leftIndex
    global sensor_N
    global sensor_W
    global sensor_S
    global sensor_E
    global sensor1
    global sensor2
    global sensor3
    global sensor4
    global config
    global sensorPatch
	# Only change index in process1 by turning, but need to keep track of both indexes in process2
	global TRIG_sensor1
	global ECHO_sensor1
	global TRIG_sensor2
	global ECHO_sensor2
	global TRIG_sensor3
	global ECHO_sensor3
	global TRIG_sensor4
	global ECHO_sensor4

    # Declare GPIO pins for 4 ultrasonic sensors: THESE DO NOT CHANGE
    # Ultrasonic sensor 1: starting off north
    TRIG_sensor1 = 5  # output pin - triggers the sensor
    ECHO_sensor1 = 6  # input pin - reads the return signal from the sensor
    # Ultrasonic sensor 2: starting off west
    TRIG_sensor2 = 19
    ECHO_sensor2 = 26
    # Ultrasonic sensor 3: starting off south
    TRIG_sensor3 = 8
    ECHO_sensor3 = 7
    # Ultrasonic sensor 4: starting off east
    TRIG_sensor4 = 20
    ECHO_sensor4 = 21

	# Global array for washer locations
	global locs
	# Remember the configuration until configuration is changed (i.e. turning)
	global TRIG_N
	global ECHO_N
	global TRIG_W
	global ECHO_W
	global TRIG_S
	global ECHO_S
	global TRIG_E
	global ECHO_E
	# motor control
    global motor
    # patching mechanism
    global PM
    # Camera Vision System outputs
    global panAngle
    global tiltAngle
    global washerFound

    # Set all values to 0 to start
    # MUST ONLY DO THIS AT BEGINNING
    rightIndex = 0
    leftIndex = 0
    # Set first configuration of car -- only do this at beginning!
    # Initial config is CONFIGURATION 1
    config = 1
 	sensorPatch = 1  # sensor that is the same direction as patch deploying
    sensor_N = 1
    sensor_W = 2
    sensor_S = 3
    sensor_E = 4
    sensor1 = "N"
    sensor2 = "W"
    sensor3 = "S"
    sensor4 = "E"

    # Append to locs when washer is found
    locs = []

    # Declare GPIO pins for 4 ultrasonic sensors: THESE DO NOT CHANGE
    # Ultrasonic sensor 1: starting off north
    TRIG_sensor1 = 5  # output pin - triggers the sensor
    ECHO_sensor1 = 6  # input pin - reads the return signal from the sensor
    # Ultrasonic sensor 2: starting off west
    TRIG_sensor2 = 19
    ECHO_sensor2 = 26
    # Ultrasonic sensor 3: starting off south
    TRIG_sensor3 = 8
    ECHO_sensor3 = 7
    # Ultrasonic sensor 4: starting off east
    TRIG_sensor4 = 20
    ECHO_sensor4 = 21

    # initialize
    TS = 0
    RD = 0
    washerFound = 0
    STOP = 0
    # distance values are global variables sent from Process 2, should exist

    # Call FSM function, will constantly loop through FSM function until program terminates (shutdown state)
    FSM(distance1, distance2, distance3, distance4,
        panAngle, tiltAngle, STOP, TS, RD, washerFound)

# Main FSM function that is run by Process 1
def FSM(distance1, distance2, distance3, distance4, panAngle, tiltAngle, STOP, TS, RD, washerFound):
    # This is the main FSM function
    #  FSM
    # inputs:
    # panAngle = camera servo1 angle readings (output from servo pid
    # tiltAngle = camera servo2 angle readings
    # TS = timer switch that begins 75 sec timer
    # RD = counter for the number of times entering row d
    # sensor1 = Ultrasonic sensor distance reading (pi pin)

    # outputs:
    # (Motor state) case=1-4 (Stop, fwd, backward, turn right, turn left)
    # (Patching Mechanism) Patch = 0 or 1 (patching or not patching)

    # Begin Session (state) waterfalls into Vision Sweep (state)
    while (STOP == 0):  # loop until trial is finished
    	if ((TS == 1) and (STOP == 0):
        # Process 1 and Process 2 are started (location tracker, bluetooth connection, buzzer)
        # Pan and tilt rotations start
            if (washerFound == 0):  # Washer Search (State), Ultrasonic Sensor Navigation
          		patch=0
		    if (distance1 < 0.94):  # reverse movement, no turning
                case=2
		    if (distance2 < 1.05):  # in ft, TURN RIGHT too close to wall
			    case=3
                turningright=1
                turningleft=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
            if ((distance3 >= 0.94) and (distance2 > distance4)):  # TURN LEFT (going CCW)
			    case=4
                turningleft=1
                turningright=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
            if (sensor4 < 1.05):  # TURN LEFT
			    case=1
                turningleft=1
                turnightright=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
            if (RD == 3):  # TURN RIGHT on to row D
			    case=3
                turningright=1
                turningleft=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
            else:  # drive straight fwd CW around square
			    case=1
                # No need to account for turning because moving straight

       # Washer detected! Enter second navigation mode!
	   if (washerFound != 0):  # Enter servo and ultrasonic sensor navigation
		    if ((panAngle != 90) and (panAngle != -90) and (pantilt != 45)):  # allows car to get 5 in from walls
			if (distance1 < 0.42):  # don't hit wall, turn to servo
			    if (panAngle > 0):  # TURN RIGHT
                    case=3
				    patch=0
                    turningright=1
                    turningleft=0
                    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                        turningright, turningleft)  # rightIndex and leftIndex are global variables
                    # Turning completed, reset
                    turningright=0
                    turningleft=0
			    if (panAngle > 0):  # TURN LEFT
                    case=4
				    patch=0
                    turningleft=1
                    turnightright=0
                    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                        turningright, turningleft)  # rightIndex and leftIndex are global variables
                    # Turning completed, reset
                    turningright=0
                    turningleft=0
			else:  # drive fwd until servos direct a turn or stop
			    case=1
			    patch=0
                # Moving forward, no turning

		    if (panAngle == 90):  # TURN RIGHT
                case=3
                patch=0
                turningright=1
                turningleft=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
		    if (panAngle == -90):  # TURN LEFT
                case=4
                patch=0
                turningleft=1
                turnightright=0
                (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)=accountforTurning(
                    turningright, turningleft)  # rightIndex and leftIndex are global variables
                # Turning completed, reset
                turningright=0
                turningleft=0
		    # AT WASHER, stop motors and Deploy patch
		    if ((tiltAngle == 45) and (panAngle >= -5) and (panAngle <= 5)):
                # WASHER FOUND
                washerFound=1
                case=0
                patch=1
                if (washerFound == 1):
                    # Once at washer, sound buzzer for 500 ms (each time bridge damage is located)
    	            washerFoundSound(macAddress)
                    # Determine square right before the patch is deployed, robot located right in front of washer ready to patch
                    # First, assign length and width of car according to configuration
                 	(dim_updown, dim_leftright)=assignLengthWidth(config)
                 	# Declare sensors
                 	(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S,
                 	 TRIG_E, ECHO_E, sensor1, sensor2, sensor3, sensor4)=declareSensor(sensor_N, sensor_W, sensor_S, sensor_E)
                 	# GLOBAL: (TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4)
                 	# Declare TRIG/ECHO pins
                 	declarePins(TRIG_N, ECHO_N, TRIG_W, ECHO_W,
                 	            TRIG_S, ECHO_S, TRIG_E, ECHO_E)
                 	# Read distance from each sensor -> calling function
                 	distance_N=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                 	                        ECHO_S, TRIG_E, ECHO_E, 1)  # determine north distance
                 	distance_W=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                 	                        ECHO_S, TRIG_E, ECHO_E, 2)  # determine west distance
                 	distance_S=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                 	                        ECHO_S, TRIG_E, ECHO_E, 3)  # determine south distance
                 	distance_E=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                 	                        ECHO_S, TRIG_E, ECHO_E, 4)  # determine east distance
                 	# Determine square location
                 	location_of_washer=squareLocWasher(
                 	    distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright, sensorPatch)
                 	# Add location to locs array
                 	locs.append(location_of_washer)

                    #Complete patching
                    if (patch == 1):
                     	# Now washer location has been saved into locs
                        # Now deploy patch
                        servPin=13
                        GPIO.setup(servPin, GPIO.OUT)
                        p=GPIO.PWM(servPin, 50)
                        p.start(2.5)  # starting at 0 degree
                        p.ChangeDutyCycle(12.5)  # turn towards 180 degree
                        time.sleep(0.5)
                        p.ChangeDutyCycle(2.5)  # turn towards 0 degrees
                        patch=0

                    # Changing motor and PM global variables
                  	motor=case
                  	PM=patch
                    Send_Signal(motor)

	    if (STOP != 0):  # Stop motors and go to Pre-shut down (state)
            case=0
            patch=0
            break  # break out of loop
            # Printing LCD and Bluetooth completed in Process 2
		# STOP also signals Process 1 and 2
		if (TS == 0):  # Shut down (state), switch turned off
		    # signals battery source to turn off and all communications to shut down
            # exit from Python
            sys.exit()

# Function to initialize serial communication to Arduino
def Initialization():
    global ser  # to remember ser in Send_Signal
    ser=serial.Serial("/dev/ttyUSB0", 9600)

#Function to send motor signal to Arduino
 def Send_Signal(signal):
        global ser
	    # signal: [Int]
	    # signal = motor
	    ser.write(bytes(signal))
        # Arduino code performs motor control based on value of signal (0-4)

#Function to alter configuration of robot after turning
def accountforTurning(turningright, turningleft):

 	# Define global variables that will be changed in this function
 	global rightIndex
 	global leftIndex
 	global sensorPatch
 	global config

   # Now account for turning - DETERMINE CONFIGURATION
    if ((turningright == 1) and (turningleft == 0)):
        rightIndex=rightIndex + 1
        # leftIndex does not change -> calling function
        (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E,
         config)=assignDirection(rightIndex, leftIndex, turningright, turningleft)
        # leftIndex set to match config of rightIndex
    elif ((turningleft == 1) and (turningright == 0)):
        leftIndex=leftIndex + 1
        # rightIndex does not change -> calling function
        (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E,
         config)=assignDirection(rightIndex, leftIndex, turningright, turningleft)
        # rightIndex set to match config of leftIndex
    elif ((turningright == 0) and (turningleft == 0)):
        # No turning, move forward

    # Keep track of sensor1 direction for pushing mechanism
    # Sensor 1 is same direction as pushing mechanism, always (this would change if original config was different)
    if (sensor_N == 1):
        sensorPatch="N"
    elif (sensor_W == 1):
        sensorPatch="W"
    elif (sensor_S == 1):
        sensorPatch="S"
    elif (sensor_E == 1):
        sensorPatch="E"
    # Need to keep track of what direction (N,W,S,E) sensor 1 is in EACH TIME
    # Only one (sensor_N, sensor_W, sensor_S, and sensor_E) should be equal to SENSOR 1

    return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)

# Function to read from encoder, assign N,W,S,E sensors
def assignDirection(rightIndex, leftIndex, turningright, turningleft):
    # First check to reset to original orientation, loop complete, back to original configuration (C1)
    if (rightIndex == 4):
        rightIndex=0
        # Set leftIndex to match rightIndex
        leftIndex=0
    elif (leftIndex == 4):
        leftIndex=0
        # Set rightIndex to match leftIndex
        rightIndex=0

    # Turning right initiated
    if (turningright == 1):  # only rightIndex should have changed
        if (rightIndex == 0):  # CONFIGURATION 1
            # Assign sensors
            sensor_N=1  # sensor_1
            sensor_W=2  # sensor_2
            sensor_S=3  # sensor_3
            sensor_E=4  # sensor_4
            config=1
            # Match not-changed leftIndex with changed rightIndex config
            leftIndex=0

        elif (rightIndex == 1):  # CONFIGURATION 2
            # Assign sensors
            sensor_N=2  # sensor_2
            sensor_W=3  # sensor_3
            sensor_S=4  # sensor_4
            sensor_E=1  # sensor_1
            config=2
            # Match not-changed leftIndex with changed rightIndex config
            leftIndex=3

        elif (rightIndex == 2):  # CONFIGURATION 3
            # Assign sensors
            sensor_N=3  # sensor_3
            sensor_W=4  # sensor_4
            sensor_S=1  # sensor_1
            sensor_E=2  # sensor_2
            config=3
            # Match not-changed leftIndex with changed rightIndex config
            leftIndex=2

        elif (rightIndex == 3):  # CONFIGURATION 4
            # Assign sensors
            sensor_N=4  # sensor_4
            sensor_W=1  # sensor_1
            sensor_S=2  # sensor_2
            sensor_E=3  # sensor_3
            config=4
            # Match not-changed leftIndex with changed rightIndex config
            leftIndex=1

    elif (turningleft == 1):  # only leftIndex should have changed
        if (leftIndex == 0):  # CONFIGURATION 1
            # Assign sensors
            sensor_N=1  # sensor_1
            sensor_W=2  # sensor_2
            sensor_S=3  # sensor_3
            sensor_E=4  # sensor_4
            config=1
            # Match not-changed rightIndex with changed leftIndex config
            rightIndex=0

        elif (leftIndex == 1):  # CONFIGURATION 4
            # Assign sensors
            sensor_N=4  # sensor_4
            sensor_W=1  # sensor_1
            sensor_S=2  # sensor_2
            sensor_E=3  # sensor_3
            config=4
            # Match not-changed rightIndex with changed leftIndex config
            rightIndex=3

        elif (leftIndex == 2):  # CONFIGURATION 3
            # Assign sensors
            sensor_N=3  # sensor_3
            sensor_W=4  # sensor_4
            sensor_S=1  # sensor_1
            sensor_E=2  # sensor_2
            config=3
            # Match not-changed rightIndex with changed leftIndex config
            rightIndex=2

        elif (leftIndex == 3):  # CONFIGURATION 2
            # Assign sensors
            sensor_N=2  # sensor_2
            sensor_W=3  # sensor_3
            sensor_S=4  # sensor_4
            sensor_E=1  # sensor_1
            config=2
            # Match not-changed rightIndex with changed leftIndex config
            rightIndex=1

    # Send back all these variables
        # hold onto values of rightIndex and leftIndex (int of values 0, 1, 2, 3)
        # sensor_N, sensor_W, sensor_S, sensor_E are int values of sensor numbers 1, 2, 3, 4
    # determineLoc
    return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config)

#Function to assign TRIG/ECHO pins accordingly
def declareSensor(sensor_N, sensor_W, sensor_S, sensor_E):
	# All TRIG and ECHO pins for each sensor are global variables (i.e. TRIG_sensor1, ECHO_sensor1)
    # Set two GPIO ports as inputs/outputs depending on CONFIGURATION!
    # First, declare North sensor
    if (sensor_N == 1):
        TRIG_N=TRIG_sensor1
        ECHO_N=ECHO_sensor1
        sensor1="N"
    elif (sensor_N == 2):
        TRIG_N=TRIG_sensor2
        ECHO_N=ECHO_sensor2
        sensor2="N"
    elif (sensor_N == 3):
        TRIG_N=TRIG_sensor3
        ECHO_N=ECHO_sensor3
        sensor3="N"
    elif (s == 4):
        TRIG_N=TRIG_sensor4
        ECHO_N=ECHO_sensor4
        sensor4="N"

    # Second, declare West sensor
    if (sensor_W == 1):
        TRIG_W=TRIG_sensor1
        ECHO_W=ECHO_sensor1
        sensor1="W"
    elif (sensor_W == 2):
        TRIG_W=TRIG_sensor2
        ECHO_W=ECHO_sensor2
        sensor2="W"
    elif (sensor_W == 3):
        TRIG_W=TRIG_sensor3
        ECHO_W=ECHO_sensor3
        sensor3="W"
    elif (sensor_W == 4):
        TRIG_W=TRIG_sensor4
        ECHO_W=ECHO_sensor4
        sensor3="W"

    # Third, declare South sensor
    if (sensor_S == 1):
        TRIG_S=TRIG_sensor1
        ECHO_S=ECHO_sensor1
        sensor1="S"
    elif (sensor_S == 2):
        TRIG_S=TRIG_sensor2
        ECHO_S=ECHO_sensor2
        sensor2="S"
    elif (sensor_S == 3):
        TRIG_S=TRIG_sensor3
        ECHO_S=ECHO_sensor3
        sensor3="S"
    elif (sensor_S == 4):
        TRIG_S=TRIG_sensor4
        ECHO_S=ECHO_sensor4
        sensor4="S"

    # Fourth, declare East sensor
    if (sensor_E == 1):
        TRIG_E=TRIG_sensor1
        ECHO_E=ECHO_sensor1
        sensor1="E"
    elif (sensor_E == 2):
        TRIG_E=TRIG_sensor2
        ECHO_E=ECHO_sensor2
        sensor2="E"
    elif (sensor_E == 3):
        TRIG_E=TRIG_sensor3
        ECHO_E=ECHO_sensor3
        sensor3="E"
    elif (sensor_E == 4):
        TRIG_E=TRIG_sensor4
        ECHO_E=ECHO_sensor4
        sensor4="E"

    # to determineLoc -- here!
    return (TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, sensor1, sensor2, sensor3, sensor4)

#Function to declare input and output pins for each direction
def declarePins(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E):
	# Declare N,W,S,E TRIG & ECHO pins
    # Ultrasonic sensor - North
    GPIO.setup(TRIG_N, GPIO.OUT)
    GPIO.setup(ECHO_N, GPIO.IN)
    # Ultrasonic sensor - West
    GPIO.setup(TRIG_W, GPIO.OUT)
    GPIO.setup(ECHO_W, GPIO.IN)
    # Ultrasonic sensor - South
    GPIO.setup(TRIG_S, GPIO.OUT)
    GPIO.setup(ECHO_S, GPIO.IN)
    # Ultrasonic sensor - East
    GPIO.setup(TRIG_E, GPIO.OUT)
    GPIO.setup(ECHO_E, GPIO.IN)

# Function to determine the car's square location on 7x7 board, called every half a second to determine square location on board
def squareLocWasher(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright, sensorPatch):
    # North: A1->G1; West: A7->A1; South:G1->A1; East: A1->A7
    # Declarations
    # All distances in ft
    maxdistance_updown=8
    boardSize_updown=7
    maxdistance_leftright=8
    boardSize_leftright=7
    square_updown=1
    square_leftright=1

    # Distance not a part of the board
    leftoverDistance_updown=0.5
    leftoverDistance_leftright=0.5

    # Subtract leftoverDistance(s) from total distance
    distance_N=distance_N - leftoverDistance_updown
    distance_S=distance_S - leftoverDistance_updown
    distance_W=distance_W - leftoverDistance_leftright
    distance_E=distance_E - leftoverDistance_leftright
    # Now all distances within 7x7 ft board!

    # Dimensions of car (based on configuration, see assignLengthWidth function)
    updown_car=dim_updown
    leftright_car=dim_leftright

    # sensorPatch = direction of sensor 1 in CONFIGURATION
    # In direction of sensor1 (i.e. N), subtract distance addition of pushing mechanism
    # In "opposite" direction of sensor1 (i.e. S), add in length of entire updown_car
    # In other directions (i.e. W, E), follow same procedure: 1/2(width) -> center of car
    # Length: all in reference to FRONT CENTER of pushing mechanism
    # Note in original config: length = 0.585 ft, width = 0.36 ft
    # Pushing mechanism adds 0.17ft in sensor1 direction (N in config1)
    pushaddition=0.17
    if (sensorPatch == "N"):  # configuration 1
        distance_N=distance_N - pushaddition  # subtract length of pushing mechanism
        distance_S=distance_S + updown_car  # add entire length of car to S reading
        distance_W=distance_W + (leftright_car / 2)
        distance_E=distance_E + (leftright_car / 2)
    elif (sensorPatch == "S"):  # configuration 3
        distance_N=distance_N + updown_car
        distance_S=distance_S - pushaddition
        distance_W=distance_W + (leftright_car / 2)
        distance_E=distance_E + (leftright_car / 2)
    elif (sensorPatch == "W"):  # configuration 2
        distance_N=distance_N + (updown_car / 2)
        distance_S=distance_S + (updown_car / 2)
        distance_W=distance_W - pushaddition
        distance_E=distance_E + leftright_car
    elif (sensorPatch == "E"):  # configuration 2 or 4
        distance_N=distance_N + (updown_car / 2)
        distance_S=distance_S + (updown_car / 2)
        distance_W=distance_W + leftright_car
        distance_E=distance_E - pushaddition
    # Now all distances are in reference to middle center of pushing mechanism!
        # ONLY when we are in front of washer use this!

    # Determine square: updown first - ROUNDING DOWN
    # Range: 0-6 because ROUNDING DOWN
    distance_N_square=np.ceil(distance_N / square_updown)
    distance_S_square=np.ceil(distance_S / square_updown)

    # Determine square: leftright second - ROUNDING DOWN
    # Range: 0-6 because ROUNDING DOWN
    distance_W_square=np.ceil(distance_W / square_leftright)
    distance_E_square=np.ceil(distance_E / square_leftright)

    # Ranges of squares: updown first
    if ((distance_N_square == 6) and (distance_S_square == 0)):
        letter='A'
    elif ((distance_N_square == 5) and (distance_S_square == 1)):
        letter='B'
    elif ((distance_N_square == 4) and (distance_S_square == 2)):
        letter='C'
    elif ((distance_N_square == 3) and (distance_S_square == 3)):
        letter='D'
    elif ((distance_N_square == 2) and (distance_S_square == 4)):
        letter='E'
    elif ((distance_N_square == 1) and (distance_S_square == 5)):
        letter='F'
    elif ((distance_N_square == 0) and (distance_S_square == 6)):
        letter='G'

    # Ranges of squares: updown first
    if ((distance_W_square == 0) and (distance_E_square == 6)):
        digit='1'
    elif ((distance_W_square == 1) and (distance_E_square == 5)):
        digit='2'
    elif ((distance_W_square == 2) and (distance_E_square == 4)):
        digit='3'
    elif ((distance_W_square == 3) and (distance_E_square == 3)):
        digit='4'
    elif ((distance_W_square == 4) and (distance_E_square == 2)):
        digit='5'
    elif ((distance_W_square == 5) and (distance_E_square == 1)):
        digit='6'
    elif ((distance_W_square == 6) and (distance_E_square == 0)):
        digit='7'

    # Now combine letter and digit
    location_of_washer=letter + digit

    return location_of_washer  # to determineLoc

# Function to sound buzzer when washer is located
def washerFoundSound(macAddress):
    # Turn on buzzer
    sendMessageTo(macAddress, 'X1')
    # Wait 500 ms
    time.sleep(0.500)
    # Turn off buzzer
    sendMessageTo(macAddress, 'X0')

####################################################################################################################
# Process 2:
def Process2():
    # Global variables - Assigned in process1
    global rightIndex
    global leftIndex
    global sensor_N
    global sensor_W
    global sensor_S
    global sensor_E
    global config

    # Global variables - Assigned here
    # Keep track of whether time is within 75s
    global STOP
    STOP=0
    # Keep track of distances from all 4 sensors
    global distance1
    global distance2
    global distance3
    global distance4
    # Bluetooth global variables
    global macAddress
    #Switch to start trial
    global TS

    # Set initial config in Process1
    # TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4 are GLOBAL variables initialized in Process1

    lenTrial=75  # length of trial
    while True:
        if (TS == 1):  # switch turned on, start trial
            # begin timer for trial
            tstart=time.time()
            while (time.time() - tstart <= lenTrial):
            # while (STOP == 0):
                # Call function to consistently send location (i.e. change global variables)
                (distance_N, distance_W, distance_S,
                 distance_E)=determineDistance(rightIndex, leftIndex)
                # Determine distances of sensors 1-4 to "send back" to process1
                # Change variables distance1, distance2, distance3, distance4
                (distance1, distance2, distance3, distance4)=sendBackDistance(
                    distance_N, distance_W, distance_S, distance_E)

                # Determine square location EVERY HALF A SECOND ONLY
                # Every half a second determineSquareLoc and send location to display station via Bluetooth
                # Creates a timer that will run repeatFindLoc every half a second
                threading.Timer(0.5, repeatfindLoc).start()

                if (time.time() - tstart > lenTrial):
                    # END OF trial
                    STOP=1  # sends to process 1 (because global variable)
                    # Pre-shutdown state!
                    # locs is a global variable
                    threadLCD=threading.Thread(target=printLCD, args=[locs])
                    # locs and macAddress are global variables
                    threadBluetooth=threading.Thread(
                        target=printBluetooth, args=[locs])
                    threadLCD.start()
                    threadBluetooth.start()
                    break  # ensure this breaks out of both while loops!
        else:  # switch off
            # don't do anything until trial has started!

# Function to determine robot's square location on board
def repeatfindLoc():
    location=determineSquareLoc(distance_N, distance_W, distance_S, distance_E)
    # Send location to display station via Bluetooth
    sendMessageTo(macAddress, location)
    # Location should only be up for 0.5sec
    # Clear location
    sendMessageTo(macAddress, 'xx')
    # Ready to print new location

# Function to determine read N, W, S, E distances
# washerinFront condition taken care of in process1
def determineDistance(rightIndex, leftIndex):

    # Configuration ONLY changed in process1, all related variables saved as global variables
    # Declaring sensors (TRIG, ECHO) and declaring pins completed in process1

    # Read distance from each sensor -> calling function
    distance_N=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                            ECHO_S, TRIG_E, ECHO_E, 1)  # determine north distance
    distance_W=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                            ECHO_S, TRIG_E, ECHO_E, 2)  # determine west distance
    distance_S=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                            ECHO_S, TRIG_E, ECHO_E, 3)  # determine south distance
    distance_E=readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S,
                            ECHO_S, TRIG_E, ECHO_E, 4)  # determine east distance

    return (distance_N, distance_W, distance_S, distance_E)

def sendBackDistance(distance_N, distance_W, distance, distance_E):
    # NOTE: sensor1, sensor2, sensor3, sensor4 are GLOBAL variables declared in process1
    # First sensor 1
    if (sensor1 == "N"):
        distance1_full=distance_N
    elif (sensor1 == "W"):
        distance1_full=distance_W
    elif (sensor1 == "S"):
        distance1_full=distance_S
    elif (sensor1 == "E"):
        distance1_full=distance_E
    # Now sensor 2
     if (sensor2 == "N"):
        distance2_full=distance_N
    elif (sensor2 == "W"):
        distance2_full=distance_W
    elif (sensor2 == "S"):
        distance2_full=distance_S
    elif (sensor2 == "E"):
        distance2_full=distance_E
    # Now sensor 3
    if (sensor3 == "N"):
        distance3_full=distance_N
    elif (sensor3 == "W"):
        distance3_full=distance_W
    elif (sensor3 == "S"):
        distance3_full=distance_S
    elif (sensor3 == "E"):
        distance3_full=distance_E
    # Finally sensor 4
    if (sensor4 == "N"):
        distance4_full=distance_N
    elif (sensor4 == "W"):
        distance4_full=distance_W
    elif (sensor4 == "S"):
        distance4_full=distance_S
    elif (sensor4 == "E"):
        distance4_full=distance_E
    # Now distance1, distance2, distance3, distance4 are distances of all 4 sensors
    # Subtract 0.5ft in all directions - 7x7 ft board
    # Distance not a part of the board
    leftoverDistance_all=0.5
    # Subtract leftoverDistance(s) from total distance
    distance1=distance1_full - leftoverDistance_all
    distance2=distance2_full - leftoverDistance_all
    distance3=distance3_full - leftoverDistance_all
    distance4=distance4_full - leftoverDistance_all
    # Now all distances within 7x7 ft board
    # Send back distance1, distance2, distance3, and distance4 continuously to function1
    return (distance1, distance2, distance3, distance4)  # all in ft


def determineSquareLoc(distance_N, distance_W, distance_S, distance_E):
    # Assign length and width of car according to configuration
    (dim_updown, dim_leftright)=assignLengthWidth(
        config)  # config is global variable

    # Determine location -> calling function
    # ONLY determine square location every half a second
    location=squareLocGeneral(distance_N, distance_W, distance_S, distance_E,
                              dim_updown, dim_leftright)  # general square location (every 0.5 sec)
    # Will need to send this location to the display station VIA BLUETOOTH!

    return (location)  # to mainFn (i.e. FSM code)
        # now, sends back distance (in feet) of all four sensor in all four directions (N, S, W, E)

# Function to determine the car's square location on 7x7 board
# called every half a second to determine square location on board
def squareLocGeneral(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright):
    # North: A1->G1; West: A7->A1; South:G1->A1; East: A1->A7

    # Declarations
    # All distances in ft - MAYBE change these to be in CENTIMETERS or INCHES?
    maxdistance_updown=8
    boardSize_updown=7
    maxdistance_leftright=8
    boardSize_leftright=7
    square_updown=1
    square_leftright=1

    # Distance not a part of the board
    leftoverDistance_updown=0.5
    leftoverDistance_leftright=0.5

    # Subtract leftoverDistance(s) from total distance
    distance_N=distance_N - leftoverDistance_updown
    distance_S=distance_S - leftoverDistance_updown
    distance_W=distance_W - leftoverDistance_leftright
    distance_E=distance_E - leftoverDistance_leftright
    # Now all distances within 7x7 ft board

    # Now *measure distance in reference to center of car* - these change according to configuration - determined in assignLengthWidth function
    updown_car=dim_updown
    leftright_car=dim_leftright

    # Account for length and width of car - adding in the (1/2)(length/width) in all directions
    distance_N=distance_N + (updown_car / 2)
    distance_S=distance_S + (updown_car / 2)
    distance_W=distance_W + (lefright_car / 2)
    distance_E=distance_E + (leftright_car / 2)
    # Now all distances are in reference to center of car
    # Overall distance (one direction) = Sensor reading (in ft) + (1/2)*(length/width of car, depending on config)

    # Determine square: updown first - ROUNDING DOWN
    # Range: 0-6 because ROUNDING DOWN
    distance_N_square=np.ceil(distance_N / square_updown)
    distance_S_square=np.ceil(distance_S / square_updown)

    # Determine square: leftright second - ROUNDING DOWN
    # Range: 0-6 because ROUNDING DOWN
    distance_W_square=np.ceil(distance_W / square_leftright)
    distance_E_square=np.ceil(distance_E / square_leftright)

    # Ranges of squares: updown first
    if ((distance_N_square == 6) and (distance_S_square == 0)):
        letter='A'
    elif ((distance_N_square == 5) and (distance_S_square == 1)):
        letter='B'
    elif ((distance_N_square == 4) and (distance_S_square == 2)):
        letter='C'
    elif ((distance_N_square == 3) and (distance_S_square == 3)):
        letter='D'
    elif ((distance_N_square == 2) and (distance_S_square == 4)):
        letter='E'
    elif ((distance_N_square == 1) and (distance_S_square == 5)):
        letter='F'
    elif ((distance_N_square == 0) and (distance_S_square == 6)):
        letter='G'

    # Ranges of squares: updown first
    if ((distance_W_square == 0) and (distance_E_square == 6)):
        digit='1'
    elif ((distance_W_square == 1) and (distance_E_square == 5)):
        digit='2'
    elif ((distance_W_square == 2) and (distance_E_square == 4)):
        digit='3'
    elif ((distance_W_square == 3) and (distance_E_square == 3)):
        digit='4'
    elif ((distance_W_square == 4) and (distance_E_square == 2)):
        digit='5'
    elif ((distance_W_square == 5) and (distance_E_square == 1)):
        digit='6'
    elif ((distance_W_square == 6) and (distance_E_square == 0)):
        digit='7'

    # Now combine letter and digit
    location=letter + digit

    return location  # to determineLoc

# Function to print out washer locations in sequential format
def printLCD(locs):
    # Declare pins
    lcd_rs=22
    lcd_en=17
    lcd_d4=25
    lcd_d5=24
    lcd_d6=23
    lcd_d7=18
    lcd_backlight=4
    lcd_columns=16
    lcd_rows=2

    # Declare mylcd
    lcd=LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                             lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

    loop=0  # count loops
    print("Begin printing LCD")
    while True:  # sequence continues until robot turns off; loop forever
        count=0
        loop=loop + 1
        for x in locs:
            count=count + 1
            loc_of_Int=x
            strLoc1="Location: #" + str(count)
            strLoc2=loc_of_Int
            lcd.set_cursor(0, 0)
            lcd.message(strLoc1)
            lcd.set_cursor(0, 1)
            lcd.message(strLoc2)
            time.sleep(1)  # each location displayed for 1 second
            lcd.clear()  # clear to print out next location


# Function to flash the same location sequence as your vehicle once the trial has concluded.
def printBluetooth(locs, macAddress):
    # Only go through sequence once
    print("Begin printing Bluetooth")
    for x in locs:
        loc_of_Int=x
        # Flash loc_of_Int on display station
        sendMessageTo(macAddress, loc_of_Int)
        print("Loc " + loc_of_Int + " sent")
        # Display location for 1 second
        time.sleep(1)
        # Clear location
        sendMessageTo(macAddress, 'xx')

####################################################################################################################
# Process 3: Vision system and associated algorithm
# the goal of this file is to run all of the 4 independent processes
# that are used to control the vision system components as well as update the variables needed for the FSM
# global variable updates allow these processes to constantly update each other

		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center

#Gloabl variables that will be changed in this function
global panAngle
global tiltAngle
global washerFound

# define the range for the motors
servo1Range=(-90, 90)
servo2Range=(0, 45)

# function to handle keyboard interrupt (looking for way to exit script)
# kills all 4 processes at once
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")

	# disable the servos
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)

	# exit
	sys.exit()

def obj_center(args, objX, objY, centerX, centerY):  # first process
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# start the video stream and wait for the camera to warm up
	vs=VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# initialize the object center finder
	obj=ObjCenter(args["canny"])

	# loop indefinitely
	while True:
		# grab the frame from the threaded video stream and flip it
		# vertically (since our camera was upside down)
		frame=vs.read()
		frame=cv2.flip(frame, 0)

		# calculate the center of the frame as this is where we will
		# try to keep the object
		(H, W)=frame.shape[:2]
		centerX.value=W // 2
		centerY.value=H // 2

		# find the object's location
		objectLoc=obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect)=objectLoc
		# global variable for FSM
		washerFound=(len(rects))

		# draw keypoints on frame
		# Draw detected blobs as red circles.
		# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
		# the size of the circle corresponds to the size of blob
		if rect is not None:
			im_with_keypoints=cv2.drawKeypoints(canny, keypoints, np.array([]), (0, 0, 255),
											  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		# Display the resulting frame with blobs
		cv2.imshow('Pan-Tilt blob Tracking', im_with_keypoints)
		out.write(im_with_keypoints)
		cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# create a PID and initialize it
	p=PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# calculate the error (camera frame center - object location)
		error=centerCoord.value - objCoord.value

		# update the value (servo angle in degrees)
		output.value=p.update(error)

def in_range(val, start, end):  # servo range checker
	# determine the input value is in the supplied range
	return (val >= start and val <= end)

def set_servos(pan, tlt):  # drives servos to specific angle values (-90-90) and (0 - 45)
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# loop indefinitely
	while True:
		# the pan and tilt angles are reversed
		panAngle=-1 * pan.value
		tltAngle=-1 * tlt.value

		# if the pan angle is within the range, pan
		if in_range(panAngle, servoRange[0], servoRange[1]):
			pth.pan(panAngle)

		# if the tilt angle is within the range, tilt
		if in_range(tltAngle, servoRange[0], servoRange[1]):
			pth.tilt(tltAngle)

		return(panAngle, tltAngle)

# check to see if this is the main body of execution
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	# specify paths
	ap=argparse.ArgumentParser()
	ap.add_argument("-c", "blob_canny", type=str, required=True,
		help="path to input blob and canny detector ")
	args=vars(ap.parse_args())

	# start a manager for managing process-safe variables
	with Manager() as manager:
		# enable the servos
		pth.servo_enable(1, True)
		pth.servo_enable(2, True)

		# set integer values for the object center (x, y)-coordinates
		centerX=manager.Value("i", 0)
		centerY=manager.Value("i", 0)

		# set integer values for the object's (x, y)-coordinates
		objX=manager.Value("i", 0)
		objY=manager.Value("i", 0)

		# pan and tilt values will be managed by independed PIDs
		pan=manager.Value("i", 0)
		tlt=manager.Value("i", 0)

		# set PID values for panning
		panP=manager.Value("f", 0.09)
		panI=manager.Value("f", 0.08)
		panD=manager.Value("f", 0.002)

		# set PID values for tilting
		tiltP=manager.Value("f", 0.11)
		tiltI=manager.Value("f", 0.10)
		tiltD=manager.Value("f", 0.002)

		# we have 4 independent processes
		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
		processObjectCenter=Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))
		processPanning=Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX))
		processTilting=Process(target=pid_process,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos=Process(target=set_servos, args=(pan, tlt))

		# start all 4 processes
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		# join all 4 processes
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()

		# disable the servos
		pth.servo_enable(1, False)
		pth.servo_enable(2, False)

####################################################################################################################
# Functions used for more than just one Process

# Function to read distance from one ultrasonic sensor
def readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, direction):
    # First declare TRIG and ECHO
    if (direction == 1):  # north
        TRIG=TRIG_N
        ECHO=ECHO_N
    elif (direction == 2):  # west
        TRIG=TRIG_W
        ECHO=ECHO_W
    elif (direction == 3):  # south
        TRIG=TRIG_S
        ECHO=ECHO_S
    elif (direction == 4):  # east
        TRIG=TRIG_E
        ECHO=ECHO_E

    # Now begin determining distance
    # Ensure the trigger pin is set low
    GPIO.output(TRIG, False)

    # Give the sensor a second to settle
    time.sleep(1)

    # Create trigger pulse
    GPIO.output(TRIG, True)

    # Set trigger pin high for 10uS
    time.sleep(0.00001)

    # Set is low again
    GPIO.output(TRIG, False)

    # Determine pulse_start
    while (GPIO.input(ECHO) == 0):
        pulse_start=time.time()

    # Determine pulse_end
    while (GPIO.input(ECHO) == 1):
        pulse_end=time.time()

    # Speed = Distance/Time, speed of sound at sea level = 343 m/s
        # 34300 = distance/(time/2)
        # 17150 = distance/time
        # distance = 17150*pulse_duration

    # Calculating distance
    pulse_duration=pulse_end - pulse_start
    distance_cm=pulse_duration * 17150
    # distance_cm = round(distance_cm,2)
    distance_inch=distance_cm / 2.54  # 2.54 cm per inch
    # distance_inch = round(distance_inch,2)
    distance_feet=distance_inch / 12  # 12 in per foot
    # distance_feet = round(distance_feet,2)

    return distance_feet  # to determineLoc

# Function to assign length and width of car according to the configuration
def assignLengthWidth(config):
    # Not changing any global variables in this function!

    # Assign length and width of car according to configuration
    length=0.585
    width=0.36  # width (ft) in original configuration
    if ((config == 1) or (config == 3)):  # car is vertical
        dim_updown=length  # up-down distance
        dim_leftright=width  # left-right distance
    elif ((config == 2) or (config == 4)):  # car is horizontal
        dim_updown=width  # up-down distance
        dim_leftright=length  # left-right distance

    return(dim_updown, dim_leftright)  # to determineLoc

# Function to send single Message to Display station via wireless communication
def sendMessageTo(targetBluetoothMacAddress, message):
    port=1
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((targetBluetoothMacAddress, port))
    sock.send(message)
    sock.close()
