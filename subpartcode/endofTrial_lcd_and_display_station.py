#End of trial with threading
#End state: combining LCD display and display station (bluetooth)

#LCD
#At the end of 75 seconds, your vehicle should cease operation.
#The locations of bridge damage should be presented on the display in sequential form (one at a time),
#with each location displayed for a duration of approximately 1 second.
#This sequence should continue until the robot is turned off by a team member.

#Display station
#Flash washer locations in same sequence as LCD (only once)
#The washer locations determined during trial

#Importing
import Adafruit_CharLCD as LCD
import time
import bluetooth
import threading

def main(): #This will all be in FSM main code
    #The washer locations determined during trial (at most four)
    global locs
    locs = ["A1","B1","C1","D1"] #captured throughout trial, saved as global variable

    #Mac address of display station
    global macAddress
    macAddress = "2015:10:195789"

    #Threading
    thread1 = threading.Thread(target = printLCD, args = [locs])
    thread2 = threading.Thread(target = printBluetooth, args = [locs, macAddress])
    thread1.start()
    thread2.start()

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
