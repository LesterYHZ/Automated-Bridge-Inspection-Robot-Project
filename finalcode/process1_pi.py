#Process 1
	#Turning -> changes configuration -> changes global variables
	#Washer found -> Determine location of washer -> Saves into locs

def Process1(): #Process1
    #Declare board setup
    GPIO.setmode(GPIO.BCM) #sets GPIO pin numbering

    #Remove warnings
    GPIO.setwarnings(False)

    #Global variables
    #global turningright
    #global turningleft
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
	#Only change index in process1 by turning, but need to keep track of both indexes in process2
	global TRIG_sensor1
	global ECHO_sensor1
	global TRIG_sensor2
	global ECHO_sensor2
	global TRIG_sensor3
	global ECHO_sensor3
	global TRIG_sensor4
	global ECHO_sensor4
	#Global array for washer locations
	global locs
	#Remember the configuration until configuration is changed (i.e. turning)
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

    #Set all values to 0 to start
    #MUST ONLY DO THIS AT BEGINNING
#     turningright = 0
#     turningleft = 0
    rightIndex = 0
    leftIndex = 0
    #Set first configuration of car -- only do this at beginning!
    #Initial config is CONFIGURATION 1
    config = 1
 	sensorPatch = 1 #sensor that is the same direction as patch deploying
    sensor_N = 1
    sensor_W = 2
    sensor_S = 3
    sensor_E = 4
    sensor1 = "N"
    sensor2 = "W"
    sensor3 = "S"
    sensor4 = "E"

    #Append to locs when washer is found
    locs = []

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
    
    # FSM
      # motor control
    global motor
    # patching mechanism
    global PM
    # Camera Vision System outputs
    global panAngle
    global tiltAngle
    global washerFound


    def FSM(distance1, distance2, distance3, distance4, panAngle,tiltAngle, STOP, TS, RD, washerFound):

    #This is the main FSM function
    #  FSM ##########################################################
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
    	if TS == 1 and STOP ==0:
        # Process 1 and Process 2 are started (location tracker, bluetooth connection, buzzer)
        # Pan and tilt rotations start
            if washerFound == 0: # Washer Search (State) # Ultrasonic Sensor Navigation
          		patch = 0
		    if distance1 << 0.94: # reverse
			case = 2
		    if distance2 << 1.05: # ft Turn right too close to wall
			case = 3
		    if distance3 >= 0.94 and distance2 >> distance4: # turn left (going CCW)
			case =4
		    if sensor4 << 1.05: # turn left
			case = 1
		    if RD == 3 : # turn right on to row D
			case = 3
		    else:  #drive straight fwd CW around square
			case = 1
	   if washerFound != 0: # servo and ultrasonic sensor navigation
		    if panAngle != 90 and panAngle != -90 and pantilt != 45: # allows car to get 5 in from walls
			if distance1 << 0.42:  # don't hit wall, turn to servo
			    if panAngle >>0: # turn right
				case = 3
				patch = 0
			    if panAngle >>0: # turn left
				case = 4
				patch = 0
			else: # drive fwd until servos direct a turn or stop
			    case = 1
			    patch = 0
		    if panAngle == 90:  # turn right
			case = 3
			patch = 0
		    if panAngle == -90: # turn left
			case = 4
			patch = 0
		    if tiltAngle =45 and panAngle >= -5 and panAngle <= 5: # stop motors and Deploy patch
			case = 0
			patch = 1

	    if STOP !=0: # Stop motors and go to Pre-shut down (state)
		case = 0
		patch = 0
		print('washer location', locs)  # print to LCD display
		# STOP also signals Process 1 and 2
		if TS == 0: # Shut down (state)
		    # signals battery source to turn off and all communications to shut down

	    If case == 3:
		turningright = 1
		turningleft = 0
	    If case == 4:
		turningright = 0
		turningleft = 1
	    If case == 0 or case == 1"
		turningright = 0
		turningleft == 0

	    motor = case
	    PM = patch

	    return (motor, PM)

   def Initialization():  # Seriial communication to Arduino
	    ser = serial.Serial("/dev/ttyUSB0",9600)
   def Send_Signal(signal):
	    # signal: [Int] 
	    signal = motor
	    ser.write(bytes(signal))
		 #      case 0:
		 #    // Motor Stop
		 #        Motor(0);
		 #        break;
		 #    case 1:
		 #    // Motor Forward
		 #        Motor(1);
		 #        break;
		 #    case 2:
		 #    // Motor Backward
		 #        Motor(2);
		 #        break;
		 #    case 3:
		 #    // Motor Right
		 #        Motor(3);
		 #        break;
		 #    case 4:
		 #    // Motor Left
		 #        Motor(4);
		 #        break;
		# PM = 0 don't patch (patch =0)
		# PM = 1 Need to patch (patch =1))
	
    ##Car turning!
    #Put this in motor code
    #Car turns right
    turningright = 1
    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch) = accountforTurning(turningright, turningleft) #rightIndex and leftIndex are global variables
    
	#Car turns left
    turningleft = 1
    (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch) = accountforTurning(turningright, turningleft) #rightIndex and leftIndex are global variables

    #Only change configuration if car turns! Otherwise, it will remember the configuration via sensor_N, sensor_W, sensor_S, and sensor_E values


    ##Found a washer, determine square location of washer
    washerFound = 0

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

    #Complete all steps to locate washer....

    #Washer found!
    #Determine square right before the patch is deployed, robot located right in front of washer ready to patch
    if (washerFound == 1): 
    	#Once at washer, sound buzzer for 500 ms (each time bridge damage is located)
    	washerFoundSound(macAddress)
    	#First, assign length and width of car according to configuration
    	(dim_updown, dim_leftright) = assignLengthWidth(config)
    	#Declare sensors
    	(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, sensor1, sensor2, sensor3, sensor4) = ...
    	declareSensor(sensor_N, sensor_W, sensor_S, sensor_E) # GLOBAL: (TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4)
    	#Declare TRIG/ECHO pins
    	declarePins(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E)
    	#Read distance from each sensor -> calling function
    	distance_N = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 1) #determine north distance
    	distance_W = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 2) #determine west distance
    	distance_S = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 3) #determine south distance
    	distance_E = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 4) #determine east distance

    	#Determine square location
    	location_of_washer = squareLocWasher(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright, sensorPatch)
    	#Add location to locs array
    	locs.append(location_of_washer)
    	#Now washer location has been saved into locs 


 def accountforTurning(turningright, turningleft):

 	#Define global variables that will be changed in this function
 	global rightIndex
 	global leftIndex
 	global sensorPatch
 	global config

   #Now account for turning - DETERMINE CONFIGURATION
        if ((turningright == 1) and (turningleft == 0)):
            rightIndex = rightIndex + 1
            #leftIndex does not change -> calling function
            (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
            #leftIndex set to match config of rightIndex

        elif ((turningleft == 1) and (turningright == 0)):
            leftIndex = leftIndex + 1
            #rightIndex does not change -> calling function
            (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config) = assignDirection(rightIndex, leftIndex, turningright, turningleft)
            #rightIndex set to match config of leftIndex

        elif ((turningright == 1) and (turningleft == 1)): #error state?
            #Error: cannot turn both ways at same time!
            print("ERROR!!!! Cannot turn right and left at same time")

        elif ((turningright == 0) and (turningleft == 0)):
            #No turning, move forward
            print("Continue Moving Forward!")

        else: #error state?
            print("ERROR!")


    #Keep track of sensor1 direction for pushing mechanism
    #Sensor 1 is same direction as pushing mechanism, always (this would change if original config was different)
    if (sensor_N == 1):
        sensorPatch = "N"
    elif (sensor_W == 1):
        sensorPatch = "W"
    elif (sensor_S == 1):
        sensorPatch = "S"
    elif (sensor_E == 1):
        sensorPatch = "E"
    #Need to keep track of what direction (N,W,S,E) sensor 1 is in EACH TIME
    #Only one (sensor_N, sensor_W, sensor_S, and sensor_E) should be equal to SENSOR 1

        return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config, sensorPatch)


#Function to read from encoder, assign N,W,S,E sensors
def assignDirection(rightIndex, leftIndex, turningright, turningleft):
    #First check to reset to original orientation, loop complete, back to original configuration (C1)
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
        if (rightIndex == 0): #CONFIGURATION 1
            #Assign sensors
            sensor_N = 1 #sensor_1
            sensor_W = 2 #sensor_2
            sensor_S = 3 #sensor_3
            sensor_E = 4 #sensor_4
            config = 1

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 0

        elif (rightIndex == 1): #CONFIGURATION 2
            #Assign sensors
            sensor_N = 2 #sensor_2
            sensor_W = 3 #sensor_3
            sensor_S = 4 #sensor_4
            sensor_E = 1 #sensor_1
            config = 2

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 3

        elif (rightIndex == 2): #CONFIGURATION 3
            #Assign sensors
            sensor_N = 3 #sensor_3
            sensor_W = 4 #sensor_4
            sensor_S = 1 #sensor_1
            sensor_E = 2 #sensor_2
            config = 3

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 2

        elif (rightIndex == 3): #CONFIGURATION 4
            #Assign sensors
            sensor_N = 4 #sensor_4
            sensor_W = 1 #sensor_1
            sensor_S = 2 #sensor_2
            sensor_E = 3 #sensor_3
            config = 4

            #Match not-changed leftIndex with changed rightIndex config
            leftIndex = 1

        else: #already checked for value of 4! error state?
            print("ERROR!!!") #should only be values 1, 2, 3

    elif (turningleft == 1): #only leftIndex should have changed
        print ("Turned left")
        if (leftIndex == 0): #CONFIGURATION 1
            #Assign sensors
            sensor_N = 1 #sensor_1
            sensor_W = 2 #sensor_2
            sensor_S = 3 #sensor_3
            sensor_E = 4 #sensor_4
            config = 1

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 0

        elif (leftIndex == 1): #CONFIGURATION 4
            #Assign sensors
            sensor_N = 4 #sensor_4
            sensor_W = 1 #sensor_1
            sensor_S = 2 #sensor_2
            sensor_E = 3 #sensor_3
            config = 4

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 3

        elif (leftIndex == 2): #CONFIGURATION 3
            #Assign sensors
            sensor_N = 3 #sensor_3
            sensor_W = 4 #sensor_4
            sensor_S = 1 #sensor_1
            sensor_E = 2 #sensor_2
            config = 3

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 2

        elif (leftIndex == 3): #CONFIGURATION 2
            #Assign sensors
            sensor_N = 2 #sensor_2
            sensor_W = 3 #sensor_3
            sensor_S = 4 #sensor_4
            sensor_E = 1 #sensor_1
            config = 2

            #Match not-changed rightIndex with changed leftIndex config
            rightIndex = 1

        else: #already checked for value of 4!
            print("ERROR!!!") #should only be values 1, 2, 3

    #Send back all these variables
        #hold onto values of rightIndex and leftIndex (int of values 0, 1, 2, 3)
        #sensor_N, sensor_W, sensor_S, sensor_E are int values of sensor numbers 1, 2, 3, 4
    return (rightIndex, leftIndex, sensor_N, sensor_W, sensor_S, sensor_E, config) #determineLoc


#Function to assign length and width of car according to the configuration
def assignLengthWidth(config):
	#Not changing any global variables in this function!

    #Assign length and width of car according to configuration
    length = 0.585
    width = 0.36 #width (ft) in original configuration
    if ((config == 1) or (config == 3)): #car is vertical
    	dim_updown = length #up-down distance
        dim_leftright = width #left-right distance
    elif ((config == 2) or (config == 4)): #car is horizontal
    	dim_updown = width #up-down distance
        dim_leftright = length #left-right distance

    return(dim_updown, dim_leftright) #to determineLoc


def declareSensor(sensor_N, sensor_W, sensor_S, sensor_E):

	#All TRIG and ECHO pins for each sensor are global variables (i.e. TRIG_sensor1, ECHO_sensor1)

    #Set two GPIO ports as inputs/outputs depending on CONFIGURATION!
    #First, declare North sensor
    if (sensor_N == 1):
        TRIG_N = TRIG_sensor1
        ECHO_N = ECHO_sensor1
        sensor1 = "N"
    elif (sensor_N == 2):
        TRIG_N = TRIG_sensor2
        ECHO_N = ECHO_sensor2
        sensor2 = "N"
    elif (sensor_N == 3):
        TRIG_N = TRIG_sensor3
        ECHO_N = ECHO_sensor3
        sensor3 = "N"
    elif (s == 4):
        TRIG_N = TRIG_sensor4
        ECHO_N = ECHO_sensor4
        sensor4 = "N"

    #Second, declare West sensor
    if (sensor_W == 1):
        TRIG_W = TRIG_sensor1
        ECHO_W = ECHO_sensor1
        sensor1 = "W"
    elif (sensor_W == 2):
        TRIG_W = TRIG_sensor2
        ECHO_W = ECHO_sensor2
        sensor2 = "W"
    elif (sensor_W == 3):
        TRIG_W = TRIG_sensor3
        ECHO_W = ECHO_sensor3
        sensor3 = "W"
    elif (sensor_W == 4):
        TRIG_W = TRIG_sensor4
        ECHO_W = ECHO_sensor4
        sensor3 = "W"

    #Third, declare South sensor
    if (sensor_S == 1):
        TRIG_S = TRIG_sensor1
        ECHO_S = ECHO_sensor1
        sensor1 = "S"
    elif (sensor_S == 2):
        TRIG_S = TRIG_sensor2
        ECHO_S = ECHO_sensor2
        sensor2 = "S"
    elif (sensor_S == 3):
        TRIG_S = TRIG_sensor3
        ECHO_S = ECHO_sensor3
        sensor3 = "S"
    elif (sensor_S == 4):
        TRIG_S = TRIG_sensor4
        ECHO_S = ECHO_sensor4
        sensor4 = "S"

    #Fourth, declare East sensor
    if (sensor_E == 1):
        TRIG_E = TRIG_sensor1
        ECHO_E = ECHO_sensor1
        sensor1 = "E"
    elif (sensor_E == 2):
        TRIG_E = TRIG_sensor2
        ECHO_E = ECHO_sensor2
        sensor2 = "E"
    elif (sensor_E == 3):
        TRIG_E = TRIG_sensor3
        ECHO_E = ECHO_sensor3
        sensor3 = "E"
    elif (sensor_E == 4):
        TRIG_E = TRIG_sensor4
        ECHO_E = ECHO_sensor4
        sensor4 = "E"

    return (TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, sensor1, sensor2, sensor3, sensor4) #to determineLoc -- here!

def declarePins(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E):
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


#Function to read distance from one ultrasonic sensor
def readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, direction):
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
    while (GPIO.input(ECHO) == 0):
        pulse_start = time.time()

    #Determine pulse_end
    while (GPIO.input(ECHO) == 1):
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


#Function to determine the car's square location on 7x7 board
#called every half a second to determine square location on board
def squareLocWasher(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright, sensorPatch):
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
    #Now all distances within 7x7 ft board!

    #Dimensions of car (based on configuration, see assignLengthWidth function)
    updown_car = dim_updown
    leftright_car = dim_leftright

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
    location_of_washer = letter + digit

    return location_of_washer #to determineLoc

#Function to sound buzzer when washer is located
def washerFoundSound(macAddress):
    #Turn on buzzer
    sendMessageTo(macAddress,'X1')
    #Wait 500 ms
    time.sleep(0.500)
    #Turn off buzzer
    sendMessageTo(macAddress,'X0')

#Function to send "message" to display station
def sendMessageTo(targetBluetoothMacAddress,message):
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))
    sock.send(message)
    sock.close()





