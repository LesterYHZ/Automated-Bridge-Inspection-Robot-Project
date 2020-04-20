#Bluetooth Python Code: Raspberry Pi in master mode
    #Arduino HC-05 in slave mode (for functional prototype)

import bluetooth
import time

lookUpNearbyBluetoothDevices()
#sendmessageTo(macAddress,message)
sendMessageTo("00:14:03:06:04:B2","A1") #HC-05 MAC Address 
time.sleep(4) #reset time
sendMessageTo("00:14:03:06:04:B2","B2")
time.sleep(4) #reset time
sendMessageTo("00:14:03:06:04:B2","C3")


def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  
  data = client_sock.recv(1024)
  print ("received [%s]" % data)
  
  client_sock.close()
  server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress,message):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send(message)
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
    



