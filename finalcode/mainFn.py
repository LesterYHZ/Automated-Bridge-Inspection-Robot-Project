#Importing
import RPi.GPIO as GPIO
import time
import numpy as np
import threading
import bluetooth
import time
import Adafruit_CharLCD as LCD

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

    # motor control
    global motor
    # patching mechanism
    global PM
    # Camera Vision System outputs
    global panAngle
    global tiltAngle
    global washer_detected


if __name__ == '__main__':
    main()

def main(sensor1, sensor2, sensor3, sensor4, panAngle,tiltAngle, STOP, TS, RD, washer_detected):

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
        if washer_detected == 0: # Washer Search (State) # Ultrasonic Sensor Navigation
            patch = 0
            if sensor1 << 0.94: # reverse
                case = 2
            if sensor2 << 1.05: # ft Turn right too close to wall
                case = 3
            if sensor3 >= 0.94 and sensor2 >> sensor4: # turn left (going CCW)
                case =4
            if sensor4 << 1.05: # turn left
                case = 1
            if RD == 3 : # turn right on to row D
                case = 3
            else:  #drive straight fwd CW around square
                case = 1
        if washer_detected != 0: # servo and ultrasonic sensor navigation
            if panAngle != 90 and panAngle != -90 and pantilt != 45: # allows car to get 5 in from walls
                if sensor1 << 0.42:  # don't hit wall, turn to servo
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


    motor = case
    PM = patch
    return (motor, PM)
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
    
# leave this section at bottom

	##THREADING!
   	#Define threads
    thread_Process1 = threading.Thread(target = Process1)
    thread_Process2 = threading.Thread(target = Process2)
    thread_pan_tilt_tracking = threading.Thread(target = pan_tilt_tracking)
    #Start threads
    thread_Process1.start()
    thread_Process2.start()
    thread_pan_tilt_tracking.start()
    #Deal with ALL global variables in here?
