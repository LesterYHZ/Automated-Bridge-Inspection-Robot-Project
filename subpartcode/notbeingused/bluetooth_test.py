import bluetooth

def detect_nearby_devices():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print(" {} - {}". format(addr, name))
        
def connect_to_device(device_name):
    bd_addr = device_name
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    sock.send("A2")
    sock.close()
    
if __name__ == "__main__":
    detect_nearby_devices()
    connect_to_device("2015:10:195789")
    