#Importing
import RPi.GPIO as GPIO
import time
import numpy as np
import threading
import bluetooth
import time
import Adafruit_CharLCD as LCD


if __name__ == '__main__':
    main()

def main(): #This is the main FSM function

	##THREADING!
   	#Define threads
    thread_Process1 = threading.Thread(target = Process1)
    thread_Process2 = threading.Thread(target = Process2)
    #Start threads
    thread_Process1.start()
    thread_Process2.start()

    #Deal with ALL global variables in here?