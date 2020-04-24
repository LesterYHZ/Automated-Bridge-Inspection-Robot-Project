#End state: combining LCD display and display station (bluetooth)

#manager


#LCD
#At the end of 75 seconds, your vehicle should cease operation.
#The locations of bridge damage should be presented on the display in sequential form (one at a time),
#with each location displayed for a duration of approximately 1 second.
#This sequence should continue until the robot is turned off by a team member.

#Display station
#Flash washer locations in same sequence as LCD (only once)
#The washer locations determined during trial

#How to do two things at once?

def mainFn(): #This will all be in FSM main code
    #For LCD
    import Adafruit_CharLCD as LCD
    import time
    
    #For bluetooth
    import bluetooth
    import time

    #The washer locations determined during trial (at most four)
    locs = ["A1","B1","C1","D1"]

    #Mac address of display station
    macAddress = "2015:10:195789"

    #Call function to print LCD
        #In function, call display station bluetooth function (in while loop)
    printLCD()


def printLCD(locs, macAddress): #sending in macAddress because printLocs called in while loop
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

    #Print display station on y-th run-through of LCD
    #FIX THIS!!
    y = 5;
    
    while True: #sequence continues until robot turns off; loop forever
        count=0
        if (count == y): #stop to print sequence onto display station
            printLocs(locs,macAddress)
            #Continue with LCD printing now
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

def sendMessageTo(targetBluetoothMacAddress,message):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send(message)
  sock.close()
    

    
