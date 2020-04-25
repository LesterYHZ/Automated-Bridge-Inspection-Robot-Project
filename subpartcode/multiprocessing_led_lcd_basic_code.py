def Process1():
    #Importing
    import RPi.GPIO as GPIO
    from time import sleep
    GPIO.setwarnings(False)

    #Declarations
    GPIO.setmode(GPIO.BOARD)
    redLED = 33
    blueLED = 35
    greenLED = 37
    GPIO.setup(redLED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(blueLED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(greenLED, GPIO.OUT, initial=GPIO.LOW)

    #Looping
    #while True: #looping forever
    for _ in range(10): #for looping
        GPIO.output(redLED, GPIO.HIGH) #turn on
        sleep(0.5)
        GPIO.output(redLED, GPIO.LOW) #turn off
        GPIO.output(blueLED, GPIO.HIGH) #turn on
        sleep(0.5)
        GPIO.output(blueLED, GPIO.LOW) #turn off
        GPIO.output(greenLED, GPIO.HIGH) #turn on
        sleep (0.5)
        GPIO.output(greenLED, GPIO.LOW) #turn off

    #Turn all on to indicate "done"
    GPIO.output(redLED, GPIO.HIGH)
    GPIO.output(blueLED, GPIO.HIGH)
    GPIO.output(greenLED, GPIO.HIGH)

def Process2():
    import Adafruit_CharLCD as LCD
    import time

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

    #Start timer
    tstart = time.time()
    lcd.clear()

    #Looping
    #while True: #looping forever
    for _ in range(11): #for looping
        lcd.clear()
        currentTime = int(time.time() - tstart)
        strTime1 = "Time elapsed:"
        strTime2 = "  " + str(currentTime) + "  seconds"
        lcd.set_cursor(0,0)
        lcd.message(strTime1)
        lcd.set_cursor(0, 1)
        lcd.message(strTime2)
        time.sleep(1)

    #Timer complete
    lcd.clear()
    strTime1 = strTime2
    strTime2 = "Timer complete!"
    lcd.set_cursor(0,0)
    lcd.message(strTime1)
    lcd.set_cursor(0, 1)
    lcd.message(strTime2)



#main function
from multiprocessing import Process

#If run without multiprocessing, will get stuck in each while loop
#Process1()
#Process2()

#Declare processes
process1 = Process(target=Process1)
process2 = Process(target=Process2)

#Start processes
process1.start()
process2.start()

#Join processes
process1.join()
process2.join()
