#Bluetooth test: Threading
import threading
import time
import bluetooth

def sendMessageTo(targetBluetoothMacAddress,message):
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))
    sock.send(message)
    sock.close()

    global done
    done = 1

def main():
    #main code
    processes = []
    #For path (every half a second)
    locs = ["A1","B2","D2","F2","F6","D6","B6","C4"]
    tstart = time.time()
    for loc in locs:
        thread = threading.Thread(target = sendMessageTo, args = ["00:14:03:06:04:B2",loc])
        thread.start()
        print("Loc " + loc + " sent")
        time.sleep(1.5)
    totalTime = round(time.time() - tstart, 2)
    print("Total processing time (s): " + str(totalTime))

if __name__ == '__main__':
    main()
