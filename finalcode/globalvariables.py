###Keep track of global variables we are using in our FSM

##PROCESS 1
	#All global variables below are assigned in process1, needed in process2
	#Configuration-related (remember current config of car)
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
    #Remember which I/O pin is for which direction
	global TRIG_N
	global ECHO_N
	global TRIG_W
	global ECHO_W
	global TRIG_S
	global ECHO_S
	global TRIG_E
	global ECHO_E

 	#I/O pins of TRIG & ECHO for each ultrasonic sensor
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

##PROCESS 2
	#Global variables - Assigned in process1, needed in process2
    global rightIndex
    global leftIndex
    global sensor_N
    global sensor_W
    global sensor_S
    global sensor_E
    global config

	#Global variables - Assigned in process2, needed in process1
    #Keep track of whether time is within 75s
    global STOP
    #Keep track of distances from all 4 sensors
    global distance1
    global distance2
    global distance3
    global distance4
    #Bluetooth global variables
    global macAddress
