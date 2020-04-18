#FOUR Ultrasonic sensors (HC-SR04) code
#Version 2

#Goal: Assign four sensors to the four directions depending on the configuration
    #When turn occurs, the sensor that aligns with each direction will change = FOUR CONFIGURATIONS

    #Four sensors: sensor_1, sensor_2, sensor_3, sensor_4
    #Four directions: sensor_N, sensor_W, sensor_S, sensor_E
    #Starting orientation: S1=S_N, S2=S_W, S3=S_S, S4=S_E

    #STILL NEED TO DO: I will turn this into a function that can be called by the main code
    #The main code will have the initial declarations below

    #[rightIndex, leftIndex, location] = findSquare(turningright, turningleft, rightIndex, leftIndex)
        #findSquare will be called every 0.5 seconds to send location to display station?
        #STILL NEED TO DO: make sure everything still works if "moving forward" and no turning occurs - keep track of necessary variables


#Initial declarations: input variables of function (yet to be created)
if startingoff = True: #only declare ONCE
    turningright = 0 #sent to this function by encoder?
    turningleft = 0 #sent to this function by encoder?
    rightIndex = 0 #original orientation
    leftIndex = 0 #original orientation


#Importing
import RPi.GPIO as GPIO
import time
import numpy as np

#Declare board setup
GPIO.setmode(GPIO.BCM) #sets GPIO pin numbering

#Remove warnings
GPIO.setwarnings(False)

#Declare GPIO pins for 4 ultrasonic sensors: THESE DO NOT CHANGE
#Ultrasonic sensor 1
TRIG_sensor1 = 23 #output pin - triggers the sensor
ECHO_sensor1 = 24 #input pin - reads the return signal from the sensor
#Ultrasonic sensor 2
TRIG_sensor2 = 16
ECHO_sensor2 = 20
#Ultrasonic sensor 3
TRIG_sensor3 = 5
ECHO_sensor3 = 6
#Ultrasonic sensor 4
TRIG_sensor4 = 13
ECHO_sensor4 = 19

#Now account for turning - DETERMINE CONFIGURATION
if (turningright == 1):
    rightIndex = rightIndex + 1
    #leftIndex does not change -> calling function
    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
    #leftIndex set to match config of rightIndex
    
elif (turningleft == 1):
    leftIndex = leftIndex + 1
    #rightIndex does not change -> calling function
    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
    #rightIndex set to match config of leftIndex 
    
elif ((turningright == 1) and (turningleft == 1)):
    #Error: cannot turn both ways at same time!
    print("ERROR!!!! Cannot turn right and left at same time")
    
else: #turningright == 0 and turningleft == 0
    #No turning, move forward
    print("Continue Moving Forward!")

#Set two GPIO ports as inputs/outputs depending on CONFIGURATION!
#First, declare North sensor
if (sensor_N == 1):
    TRIG_N = TRIG_sensor1
    ECHO_N = ECHO_sensor1
elif (sensor_N == 2):
    TRIG_N = TRIG_sensor2
    ECHO_N = ECHO_sensor2
elif (sensor_N == 3):
    TRIG_N = TRIG_sensor3
    ECHO_N = ECHO_sensor3
elif (sensor_N == 4):
    TRIG_N = TRIG_sensor4
    ECHO_N = ECHO_sensor4
    
#Second, declare West sensor
if (sensor_W == 1):
    TRIG_W = TRIG_sensor1
    ECHO_W = ECHO_sensor1
elif (sensor_W == 2):
    TRIG_W = TRIG_sensor2
    ECHO_W = ECHO_sensor2
elif (sensor_W == 3):
    TRIG_W = TRIG_sensor3
    ECHO_W = ECHO_sensor3
elif (sensor_W == 4):
    TRIG_W = TRIG_sensor4
    ECHO_W = ECHO_sensor4
    
#Third, declare South sensor
if (sensor_S == 1):
    TRIG_S = TRIG_sensor1
    ECHO_S = ECHO_sensor1
elif (sensor_S == 2):
    TRIG_S = TRIG_sensor2
    ECHO_S = ECHO_sensor2
elif (sensor_S == 3):
    TRIG_S = TRIG_sensor3
    ECHO_S = ECHO_sensor3
elif (sensor_S == 4):
    TRIG_S = TRIG_sensor4
    ECHO_S = ECHO_sensor4

#Fourth, declare East sensor
if (sensor_E == 1):
    TRIG_E = TRIG_sensor1
    ECHO_E = ECHO_sensor1
elif (sensor_E == 2):
    TRIG_E = TRIG_sensor2
    ECHO_E = ECHO_sensor2
elif (sensor_E == 3):
    TRIG_E = TRIG_sensor3
    ECHO_E = ECHO_sensor3
elif (sensor_E == 4):
    TRIG_E = TRIG_sensor4
    ECHO_E = ECHO_sensor4

#Declare N,W,S,E TRIG & ECHO pins
#Ultrasonic sensor - North
GPIO.setup(TRIG_N,GPIO.OUT)
GPIO.setup(ECHO_N,GPIO.IN)
#Ultrasonic sensor - West
GPIO.setup(TRIG_W,GPIO.OUT)
GPIO.setup(ECHO_W,GPIO.IN)
#Ultrasonic sensor -
GPIO.setup(TRIG_S,GPIO.OUT)
GPIO.setup(ECHO_S,GPIO.IN)
#Ultrasonic sensor 4
GPIO.setup(TRIG_E,GPIO.OUT)
GPIO.setup(ECHO_E,GPIO.IN)

#Read distance from each sensor -> calling function
distance_N = readDistance(1) #determine north distance
distance_W = readDistance(2) #determine west distance
distance_S = readDistance(3) #determine south distance
distance_E = readDistance(4) #determine east distance

#Determine location -> calling function
location = determineLoc(distance_N, distance_W, distance_S, distance_E)

#Print out location
#Will need to send this location to the display station VIA BLUETOOTH!
print ("Square:",location)



""""
""""

#Function to read from encoder, assign N,W,S,E sensors
def assignDirection(rightIndex, leftIndex, turningright, turningleft): 
    #First check to reset to original orientation, loop complete
    if (rightIndex == 4):
        rightIndex = 0
    elif (leftIndex == 4):
        leftIndex = 0

    #Turning right initiated
    if (turningright == 1): #only rightIndex should have changed
        print ("Turned right")   
        if (rightIndex == 0):
            #Assign sensors
            sensor_N = 1 #sensor_1
            sensor_W = 2 #sensor_2
            sensor_S = 3 #sensor_3
            sensor_E = 4 #sensor_4

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 0

        elif (rightIndex == 1):
            #Assign sensors
            sensor_N = 2 #sensor_2
            sensor_W = 3 #sensor_3
            sensor_S = 4 #sensor_4
            sensor_E = 1 #sensor_1

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 3

        elif (rightIndex == 2):
            #Assign sensors
            sensor_N = 3 #sensor_3
            sensor_W = 4 #sensor_4
            sensor_S = 1 #sensor_1
            sensor_E = 2 #sensor_2
            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 2

        elif (rightIndex == 3):
            #Assign sensors
            sensor_N = 4 #sensor_4
            sensor_W = 1 #sensor_1
            sensor_S = 2 #sensor_2
            sensor_E = 3 #sensor_3
            
            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 1
            
        else: #already checked for value of 4!
            print("ERROR!!!")

    elif (turningleft == 1): #only leftIndex should have changed
        print ("Turned left")   
        if (leftIndex == 0):
            #Assign sensors
            sensor_N = 1 #sensor_1
            sensor_W = 2 #sensor_2
            sensor_S = 3 #sensor_3
            sensor_E = 4 #sensor_4

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 0

        elif (leftIndex == 1):
            #Assign sensors
            sensor_N = 4 #sensor_4
            sensor_W = 1 #sensor_1
            sensor_S = 2 #sensor_2
            sensor_E = 3 #sensor_3

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 3

        elif (leftIndex == 2):
            #Assign sensors
            sensor_N = 3 #sensor_3
            sensor_W = 4 #sensor_4
            sensor_S = 1 #sensor_1
            sensor_E = 2 #sensor_2
            
            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 2

        elif (leftIndex == 3):
            #Assign sensors
            sensor_N = 2 #sensor_2
            sensor_W = 3 #sensor_3
            sensor_S = 4 #sensor_4
            sensor_E = 1 #sensor_1

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 1

        else: #already checked for value of 4!
            print("ERROR!!!")
            
    else: #No turning, move forward
        print ("Moving forward")   
    
    #Send back all these variables
        #hold onto values of rightIndex and leftIndex (int of values 0, 1, 2, 3)
        #sensor_N, sensor_W, sensor_S, sensor_E are int values of 1, 2, 3, 4
    return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) #to main function


""""
""""
#Function to read distance from one ultrasonic sensor
def readDistance(direction):
    #First declare TRIG and ECHO
    if (direction == 1): #north
        TRIG = TRIG_N
        ECHO = ECHO_N
    elif (direction == 2): #west
        TRIG = TRIG_W
        ECHO = ECHO_W
    elif (direction == 3): #south
        TRIG = TRIG_S
        ECHO = ECHO_S
    elif (direction == 4): #east
        TRIG = TRIG_E
        ECHO = ECHO_E

    #Now begin determining distance
    #Ensure the trigger pin is set low
    GPIO.output(TRIG, False)

    #Give the sensor a second to settle
    time.sleep(1)

    #Create trigger pulse
    GPIO.output(TRIG,True)

    #Set trigger pin high for 10uS
    time.sleep(0.00001)

    #Set is low again
    GPIO.output(TRIG,False)

    #Determine pulse_start
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    #Determine pulse_end
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    #Speed = Distance/Time, speed of sound at sea level = 343 m/s
        #34300 = distance/(time/2)
        #17150 = distance/time
        #distance = 17150*pulse_duration

    #Calculating distance
    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration*17150
    #distance_cm = round(distance_cm,2)
    distance_inch = distance_cm/2.54 #2.54 cm per inch
    #distance_inch = round(distance_inch,2)
    distance_feet = distance_inch/12 #12 in per foot
    #distance_feet = round(distance_feet,2)

    return distance_feet #to main function


""""
""""
def determineLoc(distance_N, distance_W, distance_S, distance_E):
    #North: A1->G1; West: A7->A1; South:G1->A1; East: A1->A7

    #Declarations
    #All distances in ft - MAYBE change these to be in CENTIMETERS or INCHES?
    maxdistance_updown = 8
    boardSize_updown = 7
    maxdistance_leftright = 8
    boardSize_leftright = 7
    square_updown = 1 
    square_leftright = 1 

    #Distance not a part of the board 
    leftoverDistance_updown = 0.5 
    leftoverDistance_leftright = 0.5

    #Subtract leftoverDistance(s) from total distance
    distance_N = distance_N - leftoverDistance_updown
    distance_S = distance_S - leftoverDistance_updown
    distance_W = distance_W - leftoverDistance_leftright
    distance_E = distance_E - leftoverDistance_leftright
    #Now all distances within 7x7 ft board

    #Determine square: updown first - ROUNDING DOWN
    #Range: 0-6 because ROUNDING DOWN
    distance_N_square = np.ceil(distance_N/square_updown)
    distance_S_square = np.ceil(distance_S/square_updown)

    #Determine square: leftright second - ROUNDING DOWN
    #Range: 0-6 because ROUNDING DOWN
    distance_W_square = np.ceil(distance_W/square_leftright)
    distance_E_square = np.ceil(distance_E/square_leftright)

    #Ranges of squares: updown first
    if ((distance_N_square == 6) and (distance_S_square == 0)):
        letter = 'A'
    elif ((distance_N_square == 5) and (distance_S_square == 1)):
        letter = 'B'
    elif ((distance_N_square == 4) and (distance_S_square == 2)):
        letter = 'C'
    elif ((distance_N_square == 3) and (distance_S_square == 3)):
        letter = 'D'
    elif ((distance_N_square == 2) and (distance_S_square == 4)):
        letter = 'E'
    elif ((distance_N_square == 1) and (distance_S_square == 5)):
        letter = 'F'
    elif ((distance_N_square == 0) and (distance_S_square == 6)):
        letter = 'G'

    #Ranges of squares: updown first
    if ((distance_W_square == 0) and (distance_E_square == 6)):
        digit = '1'
    elif ((distance_W_square == 1) and (distance_E_square == 5)):
        digit = '2'
    elif ((distance_W_square == 2) and (distance_E_square == 4)):
        digit = '3'
    elif ((distance_W_square == 3) and (distance_E_square == 3)):
        digit = '4'
    elif ((distance_W_square == 4) and (distance_E_square == 2)):
        digit = '5'
    elif ((distance_W_square == 5) and (distance_E_square == 1)):
        digit = '6'
    elif ((distance_W_square == 6) and (distance_E_square == 0)):
        digit = '7'

    #Now combine letter and digit
    location = letter + digit

    return location #to main function

    
