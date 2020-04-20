byte incomingData;
int signal;

void Serial_Intialization() {
    Serial.begin(9600);
}

void Receive_Signal(){
    if(Serial.available()>0) {
        incomingData = Serial.read();
        signal = int(incomingData);
        Serial.println(signal);
    }
}