#Basic timer Function: Start clock; after 75 seconds, stop clock

def mainFn(): #FSM code
    #Importing
    import time

    #Switch will be an input value (to function)
    #switch = 0
    switch = 1
    
    #Variable to track switch on or off
    timerOn = 0
    
    while (timerOn == 0):
        #Check if switch has been turned on
        (timerOn, tstart) = switchCheck(switch, timerOn)
        #Exits while loop once switch = 1
        #Timer started (tstart)
    
    #Do stuff here
    #Every so often, call checkTimer
    stopTimer = checkTimer(tstart)    
    
    while (stopTimer == 0):
        print("Timer running")
        time.sleep(1)
        
    if (stopTimer == 1):
        print("Timer finished")
        
"""
"""

def switchCheck(switch, timerOn):
    if (switch == 1): #switch turned on
        tstart = time.time()
        timerOn = 1
    else:
        timerOn = 0
        tstart = 0
        
    return (timerOn, tstart) ##to main function

"""
"""
    
def checkTimer(tstart):
    #Length of timer
    lenTimer = 75 #length of trial is 75 seconds
    
    #Determine  current time
    currentTime = int(time.time() - tstart)
    
    #Check to make sure currentTime is within Timer
    if (currentTime <= lenTimer):
        stopTimer = 0
    else:
        stopTimer = 1
        
    return stopTimer #to main function
    
    
    