import serial

def Initialization():
    ser = serial.Serial("/dev/ttyUSB0",9600)

def Send_Signal(signal):
    # signal: [Int] 
    ser.write(bytes(signal))