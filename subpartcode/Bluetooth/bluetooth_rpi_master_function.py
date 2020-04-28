#Bluetooth Python Code: Raspberry Pi in master mode
    #For trials: display station (two seven-segment displays and a piezoelectric buzzer) in slave mode

def mainFn(): #This will all be in FSM main code
    import bluetooth
    import time

    #Call this to "find" MAC address of display station
    lookupNearbyDevices()

    #Define mac address
    macAddress = "2015:10:195789" #change to mac address of display station
    #station expects to see two-character transmissions from your vehicle

    #Test communication link with Display station
    testDisplay(macAddress)

    #Reset communication link with Display station
        #If communication link isn't working
        #If locations are sent on top of each other (i.e. "A1B1")
    resetDisplay(macAddress)

    #Once communication link has been established, call function
    startComLink(macAddress)

    #Complete all steps here to locate washer
    #Once at washer, sound buzzer for 500 ms (each time bridge damage is located)
    washerFoundSound(macAddress)

    #TRIAL IS OVER
    #Flash washer locations in same sequence as LCD
    #The washer locations determined during trial
    locs = ["A1","B1","C1","D1"]
    printLocs(locs,macAddress)
    #NEED TO INCORPORATE THIS WITH LCD CODE because LCD CODE will be stuck in while loop
    
   
#Function for establishing Bluetooth communication link with display station
def startComLink(macAddress):
    #Once the communication link has been established, your vehicle should flash your team number
    #three times, then sound the buzzer for approximately 250 milliseconds
    #use non-displaying characters to “blank” the display

    #Set reset time (Goal: would be instantaneous)
    resetTime = 4
    #Do we need reset time after each "sendMessageTo" call? Not able to test!
    #4s was the minimum for the functional prototype

    #Flash team number three times
    for x in range(0, 3):
        #Flash team number
        sendMessageTo(macAddress,"x1")
        #Clear team number
        sendMessageTo(macAddress,'xx')
    
    #Turn on buzzer
    sendMessageTo(macAddress,'X1')
    #Wait 250 ms
    time.sleep(0.250)
    #Turn off buzzer
    sendMessageTo(macAddress,'X0')

#Function to sound buzzer when washer is located
def washerFoundSound(macAddress):

    #Turn on buzzer
    sendMessageTo(macAddress,'X1')
    #Wait 500 ms
    time.sleep(0.500)
    #Turn off buzzer
    sendMessageTo(macAddress,'X0')

#Function to flash the same location sequence as your vehicle once the trial has concluded.
def printLocs(locs,macAddress):
    #Only go through sequence once
    for x in locs:
        loc_of_Int = x
        #Flash loc_of_Int on display station
        sendMessageTo(macAddress,loc_of_Int)
        #Display location for 1 second
        time.sleep(1)
        #Clear location
        sendMessageTo(macAddress,'xx')
        
#Function to reset communication with display station (ONLY IF NECESSARY)
def resetDisplay(macAddress):
    #To reset communication with the Display Station, send the character “Z” multiple times.
    #The Display Station will ignore all “Z” characters.
    #The first character to follow a “Z” will be considered the first character of a new two-character string command.

    #Number of times to send character "Z"
    num = 5

    for x in range(0, num):
        #Send "Z"
        sendMessageTo(macAddress,"Z")

#Function to test whether communication link with Display Station is successful
def testDisplay(macAddress):
    #Send character to test communication link with Display Station
    sendMessageTo(macAddress,"A1")
    sendMessageTo(macAddress,'xx')
    sendMessageTo(macAddress,"B1")
    sendMessageTo(macAddress,'xx')

def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")

def sendMessageTo(targetBluetoothMacAddress,message):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send(message)
  sock.close()
    
    
