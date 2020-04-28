#FOUR Ultrasonic sensors (HC-SR04) FUNCTION
#Version 2

#Two conditions:
    #1. Every half a second determine location on boardSize_updown
    #2. In front of washer, determine location on board

#Length is 23 cm with pushing mechanism

#Goal: Assign four sensors to the four directions depending on the configuration
    #When turn occurs, the sensor that aligns with each direction will change = FOUR CONFIGURATIONS

    #Four sensors: sensor_1, sensor_2, sensor_3, sensor_4
    #Four directions: sensor_N, sensor_W, sensor_S, sensor_E
    #Starting orientation: S1=S_N, S2=S_W, S3=S_S, S4=S_E


    #if moving straight, will remember configuration (variables sent back from function) and jump straight to determining squareLoc
    #if turning right, add one to rightIndex and match leftIndex - remember both right and leftIndex
    #if turning left, add one to leftIndex and match rightIndex- remember both right and leftIndex

    #Main function (mainFn) will be part of FSM code --> will call determineLoc
        #determineLoc: sends back (location, rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E)
            #i.e. remembers config, indexes, and sends back square location (i.e. location)

    #determineLoc will be called every 0.5 seconds and square location will be sent to display station via bluetooth
        #will also be called if washer is found (these square locations will be remembered in order to print out on LCD at end)

def main (): #This will all be in FSM main code
    #Importing
    import RPi.GPIO as GPIO
    import time
    import numpy as np

    #Declare board setup
    GPIO.setmode(GPIO.BCM) #sets GPIO pin numbering

    #Remove warnings
    GPIO.setwarnings(False)

    #Delarations - these will change
    turningright = 0 #sent to this function by encoder?
    turningleft = 0 #sent to this function by encoder?
    movingforward = 0 #no turning!
    rightIndex = 0 #original orientation
    leftIndex = 0 #original orientation

    #Now, determine location of car
    #Sending back configuration (sensor_N, etc.), so if continuing straight will "remember" configuration until a turn occurs
    (location, rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) = determineLoc(movingforward,turningright,turningleft,rightIndex,leftIndex,washerinFront)

    #Hold onto index values and sensor directions
    #LOCATION is square location
    return (location, rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) #to main function

"""
"""

def determineLoc(movingforward,turningright,turningleft,rightIndex,leftIndex,washerinFront):
    #Adding washer in front = if measuring distance(s) before deploying patch

    #Declare GPIO pins for 4 ultrasonic sensors: THESE DO NOT CHANGE
    #Ultrasonic sensor 1: starting off north
    TRIG_sensor1 = 5 #output pin - triggers the sensor
    ECHO_sensor1 = 6 #input pin - reads the return signal from the sensor
    #Ultrasonic sensor 2: starting off west
    TRIG_sensor2 = 19
    ECHO_sensor2 = 26
    #Ultrasonic sensor 3: starting off south
    TRIG_sensor3 = 8
    ECHO_sensor3 = 7
    #Ultrasonic sensor 4: starting off east
    TRIG_sensor4 = 20
    ECHO_sensor4 = 21

    #Now account for turning - DETERMINE CONFIGURATION
    if (washerinFront == 0): #only determine configuration if NOT during washerinFront condition
        if ((turningright == 1) and (turningleft == 0) and (movingforward == 0)) :
            rightIndex = rightIndex + 1
            #leftIndex does not change -> calling function
            (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
            #leftIndex set to match config of rightIndex

        elif ((turningleft == 1) and (turningright == 0) and (movingforward == 0)):
            leftIndex = leftIndex + 1
            #rightIndex does not change -> calling function
            (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
            #rightIndex set to match config of leftIndex

        elif ((turningright == 1) and (turningleft == 1)):
            #Error: cannot turn both ways at same time!
            print("ERROR!!!! Cannot turn right and left at same time")

        elif ((movingforward == 1) and (turningright == 0) and (turningleft == 0)):
            #No turning, move forward
            print("Continue Moving Forward!")

        else:
            print("ERROR!")

`

    (TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, config_N, config_W, config_S, config_E, sensor1, sensor2, sensor3, sensor4) = declareSensor(sensor_N, sensor_W, sensor_S, sensor_E, TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4)

    #Declare N,W,S,E TRIG & ECHO pins
    #Ultrasonic sensor - North
    GPIO.setup(TRIG_N,GPIO.OUT)
    GPIO.setup(ECHO_N,GPIO.IN)
    #Ultrasonic sensor - West
    GPIO.setup(TRIG_W,GPIO.OUT)
    GPIO.setup(ECHO_W,GPIO.IN)
    #Ultrasonic sensor - South
    GPIO.setup(TRIG_S,GPIO.OUT)
    GPIO.setup(ECHO_S,GPIO.IN)
    #Ultrasonic sensor - East
    GPIO.setup(TRIG_E,GPIO.OUT)
    GPIO.setup(ECHO_E,GPIO.IN)

    #Read distance from each sensor -> calling function
    distance_N = readDistance(1) #determine north distance
    distance_W = readDistance(2) #determine west distance
    distance_S = readDistance(3) #determine south distance
    distance_E = readDistance(4) #determine east distance

    #Assign directions back to sensor numbers

    #First sensor 1
    if (sensor1 == "N"): 
        distance1_full = distance_N
    elif (sensor1 == "W"):
        distance1_full = distance_W
    elif (sensor1 == "S"):
        distance1_full = distance_S
    elif (sensor1 == "E"):
        distance1_full = distance_E
    #Now sensor 2
     if (sensor2 == "N"): 
        distance2_full = distance_N
    elif (sensor2 == "W"):
        distance2_full = distance_W
    elif (sensor2 == "S"):
        distance2_full = distance_S
    elif (sensor2 == "E"):
        distance2_full = distance_E
    #Now sensor 3
    if (sensor3 == "N"): 
        distance3_full = distance_N
    elif (sensor3 == "W"):
        distance3_full = distance_W
    elif (sensor3 == "S"):
        distance3_full = distance_S
    elif (sensor3 == "E"):
        distance3_full = distance_E
    #Finally sensor 4
    if (sensor4 == "N"): 
        distance4_full = distance_N
    elif (sensor4 == "W"):
        distance4_full = distance_W
    elif (sensor4 == "S"):
        distance4_full = distance_S
    elif (sensor4 == "E"):
        distance4_full = distance_E
    #Now distance1, distance2, distance3, distance4 are distances of all 4 sensors
    #Subtract 0.5ft in all directions - 7x7 ft board
    #Distance not a part of the board
    leftoverDistance_all = 0.5
    #Subtract leftoverDistance(s) from total distance
    distance1 = distance1_full - leftoverDistance_all
    distance2 = distance2_full - leftoverDistance_all
    distance3 = distance3_full - leftoverDistance_all
    distance4 = distance4_full - leftoverDistance_all
    #Now all distances within 7x7 ft board
    #Send back distance1, distance2, distance3, and distance4 continuously to function1


    #Assign length and width of car according to configuration
    (dim1, dim2) = assignLengthWidth(config_N, config_S, config_W, config_E, washerinFront):

    #Determine location -> calling function
    if (washerinFront == 0): #determines square in reference to center of car (i.e. length/2, width/2)
        location = squareLocGeneral(distance_N, distance_W, distance_S, distance_E, dim1, dim2) #general square location (every 0.5 sec)
    elif (washerinFront == 1): #determines square in reference to front center of pushing mechanism
        location = squareLocWasher(distance_N, distance_W, distance_S, distance_E, dim1, dim2, sensorPatch) #only called when washer is in front of car (i.e. found)

    #Print out location
    #Will need to send this location to the display station VIA BLUETOOTH!
    print ("Square:",location)

   # return (location, rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, distance_N, distance_W, distance_S, distance_E) #to mainFn (i.e. FSM code)
     return (location, rightIndex, leftIndex, distance1, distance2, distance3, distance4) 
        #now, sends back distance (in feet) of all four sensor in all four directions (N, S, W, E)
"""
"""

def declareSensor(sensor_N, sensor_W, sensor_S, sensor_E, TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4):

    #Set two GPIO ports as inputs/outputs depending on CONFIGURATION!
    #First, declare North sensor
    if (sensor_N == 1):
        TRIG_N = TRIG_sensor1
        ECHO_N = ECHO_sensor1
        config_N = 1 #dummy variable to track which direction of length/width
        sensor1 = "N"
    elif (sensor_N == 2):
        TRIG_N = TRIG_sensor2
        ECHO_N = ECHO_sensor2
        config_N = 0
        sensor2 = "N"
    elif (sensor_N == 3):
        TRIG_N = TRIG_sensor3
        ECHO_N = ECHO_sensor3
        config_N = 1
        sensor3 = "N"
    elif (s == 4):
        TRIG_N = TRIG_sensor4
        ECHO_N = ECHO_sensor4
        config_N = 0
        sensor4 = "N"

    #Second, declare West sensor
    if (sensor_W == 1):
        TRIG_W = TRIG_sensor1
        ECHO_W = ECHO_sensor1
        config_W = 0
        sensor1 = "W"
    elif (sensor_W == 2):
        TRIG_W = TRIG_sensor2
        ECHO_W = ECHO_sensor2
        config_W = 1
        sensor2 = "W"
    elif (sensor_W == 3):
        TRIG_W = TRIG_sensor3
        ECHO_W = ECHO_sensor3
        config_W = 0
        sensor3 = "W"
    elif (sensor_W == 4):
        TRIG_W = TRIG_sensor4
        ECHO_W = ECHO_sensor4
        config_W = 1
        sensor3 = "W"

    #Third, declare South sensor
    if (sensor_S == 1):
        TRIG_S = TRIG_sensor1
        ECHO_S = ECHO_sensor1
        config_S = 1
        sensor1 = "S"
    elif (sensor_S == 2):
        TRIG_S = TRIG_sensor2
        ECHO_S = ECHO_sensor2
        config_S = 0
        sensor2 = "S"
    elif (sensor_S == 3):
        TRIG_S = TRIG_sensor3
        ECHO_S = ECHO_sensor3
        config_S = 1
        sensor3 = "S"
    elif (sensor_S == 4):
        TRIG_S = TRIG_sensor4
        ECHO_S = ECHO_sensor4
        config_S = 0
        sensor4 = "S"

    #Fourth, declare East sensor
    if (sensor_E == 1):
        TRIG_E = TRIG_sensor1
        ECHO_E = ECHO_sensor1
        config_E = 0
        sensor1 = "E"
    elif (sensor_E == 2):
        TRIG_E = TRIG_sensor2
        ECHO_E = ECHO_sensor2
        config_E = 1
        sensor2 = "E"
    elif (sensor_E == 3):
        TRIG_E = TRIG_sensor3
        ECHO_E = ECHO_sensor3
        config_E = 0
        sensor3 = "E"
    elif (sensor_E == 4):
        TRIG_E = TRIG_sensor4
        ECHO_E = ECHO_sensor4
        config_E = 1
        sensor4 = "E"

    return (TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, config_N, config_W, config_S, config_E, sensor1, sensor2, sensor3, sensor4) #to determineLoc -- here!

"""
"""

#Function to read from encoder, assign N,W,S,E sensors
def assignDirection(rightIndex, leftIndex, turningright, turningleft):
    #First check to reset to original orientation, loop complete
    if (rightIndex == 4):
        rightIndex = 0
        #Set leftIndex to match rightIndex
        leftIndex = 0
    elif (leftIndex == 4):
        leftIndex = 0
        #Set rightIndex to match leftIndex
        rightIndex = 0

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
            print("ERROR!!!") #should only be values 1, 2, 3

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
            print("ERROR!!!") #should only be values 1, 2, 3

    else: #No turning, move forward
        print ("Moving forward") #remembers configuration if no turning occurs!

    #Send back all these variables
        #hold onto values of rightIndex and leftIndex (int of values 0, 1, 2, 3)
        #sensor_N, sensor_W, sensor_S, sensor_E are int values of 1, 2, 3, 4
    return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E) #determineLoc

"""
"""

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

    return distance_feet #to determineLoc

"""
"""

#Function to assign length and width of car according to the configuration
def assignLengthWidth(config_N, config_S, config_W, config_E):

    #Assign length and width of car according to configuration
    length = 0.585
    width = 0.36 #width (ft) in original configuration
    if ((config_N == 1) and (config_S == 1) and (config_W == 1) and (config_E == 1)): #N/S up-down, W/E left-right
        dim1 = length #up-down distance
        dim2 = width #left-right distance
    elif ((config_N == 0) and (config_S == 0) and (config_W == 0) and (config_E == 0)): #W/E up-down, N/S left-right
        dim1 = width #up-down distance
        dim2 = length #left-right distance
    else:
        print('ERROR!')

    return(dim1, dim2) #to determineLoc

"""
"""

#Function to determine the car's square location on 7x7 board
#called every half a second to determine square location on board
def squareLocGeneral(distance_N, distance_W, distance_S, distance_E, dim1, dim2):
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

    #Now *measure distance in reference to center of car* - these change according to configuration - determined in assignLengthWidth function
    updown_car = dim1
    leftright_car = dim2

    #Account for length and width of car - adding in the (1/2)(length/width) in all directions
    distance_N = distance_N + (updown_car/2)
    distance_S = distance_S + (updown_car/2)
    distance_W = distance_W + (lefright_car/2)
    distance_E = distance_E + (leftright_car/2)
    #Now all distances are in reference to center of car
    #Overall distance (one direction) = Sensor reading (in ft) + (1/2)*(length/width of car, depending on config)

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

    return location #to determineLoc

"""
"""

#Function to determine the car's square location on 7x7 board
#called every half a second to determine square location on board
def squareLocWasher(distance_N, distance_W, distance_S, distance_E, dim1, dim2, sensorPatch):
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

    #Now *measure distance in reference to center of car* - these change according to configuration - determined in assignLengthWidth function
    updown_car = dim1
    leftright_car = dim2

    #Account for length and width of car - washerinFront condition - ADDED THIS
    #sensorPatch = direction of sensor 1 in CONFIGURATION
    #In direction of sensor1 (i.e. N), subtract distance addition of pushing mechanism
    #In "opposite" direction of sensor1 (i.e. S), add in length of entire updown_car
    #In other directions (i.e. W, E), follow same procedure: 1/2(width) -> center of car
    #Length: all in reference to FRONT CENTER of pushing mechanism
    #Note in original config: length = 0.585 ft, width = 0.36 ft
    #Pushing mechanism adds 0.17ft in sensor1 direction (N in config1)
    pushaddition = 0.17
    if (sensorPatch == "N"): #configuration 1
        distance_N = distance_N - pushaddition #subtract length of pushing mechanism
        distance_S = distance_S + updown_car #add entire length of car to S reading
        distance_W = distance_W + (leftright_car/2)
        distance_E = distance_E + (leftright_car/2)
    elif (sensorPatch == "S"): #configuration 3
        distance_N = distance_N + updown_car
        distance_S = distance_S - pushaddition
        distance_W = distance_W + (leftright_car/2)
        distance_E = distance_E + (leftright_car/2)
    elif (sensorPatch == "W"): #configuration 2
        distance_N = distance_N + (updown_car/2)
        distance_S = distance_S + (updown_car/2)
        distance_W = distance_W - pushaddition
        distance_E = distance_E + leftright_car
    elif (sensorPatch == "E"): #configuration 2 or 4
        distance_N = distance_N + (updown_car/2)
        distance_S = distance_S + (updown_car/2)
        distance_W = distance_W + leftright_car
        distance_E = distance_E - pushaddition
    #Now all distances are in reference to middle center of pushing mechanism!
        #ONLY when we are in front of washer use this!

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

    return location #to determineLoc
