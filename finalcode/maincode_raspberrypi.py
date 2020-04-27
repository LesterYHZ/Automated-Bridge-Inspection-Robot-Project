#Main Code: Automated Bridge Inspection - Raspberry Pi
#Group 1, ME588

# import packages here ####################################


# import different functions needed here ##########################


#  FSM ##########################################################
# inputs:
# pan = camera servo1 angle readings (output from servo pid
# tilt = camera servo2 angle readings
# patch = pushing mechanism servo 3
# ts = timer switch that begins 75 sec timer
# rd = counter for the number of times entering row d
# us1 = Ultrasonic sensor distance reading (pi pin)
def fsm(self, pan, tilt, patch, ts, rd, us1, us2, us3, us4):

    return (left_motor, right_motor, patching, state)

  
  


# leave this section at bottom
# Multiprocessing code that runs multiple processes ###################################################
# link to help explain https://pythonprogramming.net/multiprocessing-python-intermediate-python-tutorial/
if __name__ == '__main__':
    for i in range(100):
        p = multiprocessing.Process(target=fsm, args=())


        p.start()
        p.join()
