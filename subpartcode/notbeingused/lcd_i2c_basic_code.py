#Basic LCD screen (I2C) code

#Inputs: Saved washer locations (i.e. locations of bridge damage)
#At the most four locations in one trial
#NOTE: Python starts counting at 0
locs = ["A1","B1","C1","D1"]

#Import
import I2C_LCD_driver #I2C_LCD_driver.py MUST BE in folder
import time

#Declare mylcd
mylcd = I2C_LCD_driver.lcd()

while True: #sequence continues until robot turns off; loop forever
    count=0;
    for x in locs:
        count=count+1
        loc_of_Int = x
        mylcd.lcd_display_string("Location #%d:" % (count),1)
        mylcd.lcd_display_string("%s" % (loc_of_Int),2)
        time.sleep(1) #each location displayed for 1 second
        mylcd.lcd_clear()
        #time.sleep(1)
    time.sleep(1) #break between continuous loops

#mylcd.lcd_display_string("Hello World!",1,0)
