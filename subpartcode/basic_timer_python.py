#Basic timer Code: Start clock; after 75 seconds, stop clock

#Importing
import time

#Switch will be an input value (to function)
#switch = 0
switch = 1

#Length of timer
lenTimer = 75 #length of trial is 75 seconds

#Start timer when switch is turned on
if (switch == 1):
    tstart = time.time()

    #Loop until timer reaches 75 seconds
    while True:
        currentTime = int(time.time() - tstart)
        if (currentTime <= lenTimer):
            print(currentTime)
            time.sleep(1)
        else:  
            break
        
    #Time reached 75 seconds
    print ("Timer has finished ")
        
else:
    print("Switch off")

