byte incomingData = '0';
int signal = 0;

void Serial_Intialization() {
    Serial.begin(9600);
}

void Receive_Signal(){
    if(Serial.available()>0) {
        incomingData = Serial.read();
        signal = int(incomingData);
        Serial.println(signal);

        switch(signal){
            case 0:
            // Motor Stop
                Motor(0);
                break;
            case 1:
            // Motor Forward
                Motor(1);
                break;
            case 2:
            // Motor Backward
                Motor(2);
                break;
            case 3:
            // Motor Right
                Motor(3);
                break;
            case 4: 
            // Motor Left
                Motor(4);
                break;
            /*
            * case 5:
            *     pusher(1);
            *     break;
            * case 6:
            *     pusher(0);
            *     break;
            * 
            * case other_number:
            *   lcd("some_coord");
            *   break;
            */
        }
    }
}