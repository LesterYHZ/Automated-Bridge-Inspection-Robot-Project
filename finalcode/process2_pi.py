#Process 2:
    #Timer of 75s
    #Consistently "sends" four sensor distances to process1 (i.e. changes global variables: distance1, distance2, distance3, distance4) 
    #Every half a second determines square location and sends location string to display station via Bluetooth

def Process2(): #Process2

    #Global variables - Assigned in process1
    global rightIndex
    global leftIndex
    global sensor_N
    global sensor_W
    global sensor_S
    global sensor_E
    global config

    #Global variables - Assigned here
    #Keep track of whether time is within 75s
    global STOP
    STOP = 0
    #Keep track of distances from all 4 sensors
    global distance1
    global distance2
    global distance3
    global distance4
    #Bluetooth global variables
    global macAddress
    macAddress = "2015:10:195789"

    #Set initial config in Process1
    #TRIG_sensor1, ECHO_sensor1, TRIG_sensor2, ECHO_sensor2, TRIG_sensor3, ECHO_sensor3, TRIG_sensor4, ECHO_sensor4 are GLOBAL variables initialized in Process1

    lenTrial = 75 #length of trial
    while True:
        if (switch == 1): #switch turned on, start trial
            #begin timer for trial
            tstart = time.time()
            while (time.time() - tstart <= lenTrial):
            #while (STOP == 0):
                #Call function to consistently send location (i.e. change global variables)
                (distance_N, distance_W, distance_S, distance_E) = determineDistance(rightIndex,leftIndex)
                #Determine distances of sensors 1-4 to "send back" to process1
                #Change variables distance1, distance2, distance3, distance4
                (distance1, distance2, distance3, distance4) = sendBackDistance(distance_N, distance_W, distance_S, distance_E)

                #Determine square location EVERY HALF A SECOND ONLY
                #Every half a second determineSquareLoc and send location to display station via Bluetooth
                #Creates a timer that will run repeatFindLoc every half a second
                threading.Timer(0.5, repeatfindLoc).start()
                    
            if (time.time() - tstart > lenTrial):
                #END OF trial
                STOP = 1 #sends to process 1 (because global variable)
                #Pre-shutdown state!
                #state = S5
                threadLCD = threading.Thread(target = printLCD, args = [locs]) #locs is a global variable
                threadBluetooth = threading.Thread(target = printBluetooth, args = [locs]) #locs and macAddress are global variables
                threadLCD.start()
                threadBluetooth.start()

                #NEED BREAK??? Should be stuck in here until shutdown
                break #ensure this breaks out of both while loops!


        else: #switch off
            #don't do anything until trial has started!


def repeatfindLoc():
    location = determineSquareLoc(distance_N, distance_W, distance_S, distance_E)  
    #Send location to display station via Bluetooth
    sendMessageTo(macAddress, location)
    #Location should only be up for 0.5sec
    #Clear location
    sendMessageTo(macAddress, 'xx')
    #Ready to print new location


def determineDistance(rightIndex,leftIndex): #washerinFront condition taken care of in process1

    #Configuration ONLY changed in process1, all related variables saved as global variables
    #Declaring sensors (TRIG, ECHO) and declaring pins completed in process1

    #Read distance from each sensor -> calling function
    distance_N = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 1) #determine north distance
    distance_W = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 2) #determine west distance
    distance_S = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 3) #determine south distance
    distance_E = readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, 4) #determine east distance

    return (distance_N, distance_W, distance_S, distance_E)


#Function to read distance from one ultrasonic sensor
def readDistance(TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E, direction):
    #First declare TRIG and ECHO
    #TRIG_N, ECHO_N, TRIG_W, ECHO_W, TRIG_S, ECHO_S, TRIG_E, ECHO_E are global variables assigned in process1
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

def sendBackDistance(distance_N, distance_W, distance, distance_E):
    #NOTE: sensor1, sensor2, sensor3, sensor4 are GLOBAL variables declared in process1
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
    return (distance1, distance2, distance3, distance4) #all in ft


def determineSquareLoc(distance_N, distance_W, distance_S, distance_E):
    #Assign length and width of car according to configuration
    (dim_updown, dim_leftright) = assignLengthWidth(config) #config is global variable

    #Determine location -> calling function
    #ONLY determine square location every half a second
    location = squareLocGeneral(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright) #general square location (every 0.5 sec)
    #Will need to send this location to the display station VIA BLUETOOTH!

    return (location) #to mainFn (i.e. FSM code)
        #now, sends back distance (in feet) of all four sensor in all four directions (N, S, W, E)


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


#Function to determine the car's square location on 7x7 board
#called every half a second to determine square location on board
def squareLocGeneral(distance_N, distance_W, distance_S, distance_E, dim_updown, dim_leftright):
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
    updown_car = dim_updown
    leftright_car = dim_leftright

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

def printLCD(locs):

    #Declare pins
    lcd_rs = 22
    lcd_en = 17
    lcd_d4 = 25
    lcd_d5 = 24
    lcd_d6 = 23
    lcd_d7 = 18
    lcd_backlight = 4
    lcd_columns = 16
    lcd_rows = 2

    #Declare mylcd
    lcd =LCD.Adafruit_CharLCD (lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

    loop = 0 #count loops
    print("Begin printing LCD")
    while True: #sequence continues until robot turns off; loop forever
        count = 0
        loop = loop + 1
        for x in locs:
            count=count+1
            loc_of_Int = x
            strLoc1 = "Location: #" + str(count)
            strLoc2 = loc_of_Int
            lcd.set_cursor(0,0)
            lcd.message(strLoc1)
            lcd.set_cursor(0, 1)
            lcd.message(strLoc2)
            time.sleep(1) #each location displayed for 1 second
            lcd.clear() #clear to print out next location


#Function to flash the same location sequence as your vehicle once the trial has concluded.
def printBluetooth(locs,macAddress):
    #Only go through sequence once
    print("Begin printing Bluetooth")
    for x in locs:
        loc_of_Int = x
        #Flash loc_of_Int on display station
        sendMessageTo(macAddress,loc_of_Int)
        print("Loc " + loc_of_Int + " sent")
        #Display location for 1 second
        time.sleep(1)
        #Clear location
        sendMessageTo(macAddress,'xx')


def sendMessageTo(targetBluetoothMacAddress,message):
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))
    sock.send(message)
    sock.close()

if __name__ == '__main__':
    main()
