#Ultrasonic sensor basic code
#Basic Ultrasonic sensor (HC-SR04) code

import RPi.GPIO as GPIO #GPIO RPI library
import time # makes sure Pi waits between steps
GPIO.setmode(GPIO.BCM) #sets GPIO pin numbering
#GPIO.setmode(GPIO.BOARD)

#Remove warnings
GPIO.setwarnings(False)

#Create loop variable
#loop = 1

#BCM
TRIG = 23 #output pin - triggers the sensor
ECHO = 24 #input pin - reads the return signal from the sensor

#BOARD
#TRIG=16
#ECHO=18

#Looping not necessary
#Print a message to let the user know that distance measurement is in progress
print ("Distance Measurement In Progress")

#Set two GPIO ports as inputs/outputs
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#while loop == 1: #Looping forever
while True: #Looping forever
    #Ensure the trigger pin is set low
    GPIO.output(TRIG, False)

    #Give the sensor a second to settle
    print ("Waiting for Sensor to Settle")
    #time.sleep(2)
    time.sleep(1)

    #Create trigger pulse
    GPIO.output(TRIG,True)

    #Set trigger pin high for 10uS
    time.sleep(0.00001)

    #Set it low again
    GPIO.output(TRIG,False)

    #Record the last low timestamp for ECHO (just before the return signal is received and the pin goes high)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        
    #Once a signal is received, the value changes from low to high, and the signal will remain high for the duration of the echo pulse
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    #speed=distance/time
    #speed of sound at sea level = 343m/s
    #34300 = distance/(time/2)
    #17150 = distance/time
    #17150*time = distance

    #Calculating...
    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration*17150
    #distance_cm = pulse_duration*0.034/2;
    distance_cm = round(distance_cm,2)
    distance_inch = distance_cm/2.54 #2.54 cm in 1 inch
    #distance_inch = pulse_duration*0.0133/2
    distance_inch = round(distance_inch,2)
    distance_feet = distance_inch/12
    distance_feet = round(distance_feet,2)
    

    #Print distance
    #print ("Distance:",distance_cm,"cm")
    #print ("Distance:",distance_inch,"in")
    print ("Distance:",distance_feet,"ft")
    
    #Delay
    time.sleep(2)

#Clean GPIO pins to ensure all inputs/outputs are reset
GPIO.cleanup()


