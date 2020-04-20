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

        switch(signal){
            case 0:
            // Motor Stop
                motor(0);
                break;
            case 1:
            // Motor Forward
                motor(1);
                break;
            case 2:
            // Motor Backward
                motor(2);
                break;
            case 3:
            // Motor Right
                motor(3);
                break;
            case 4: 
            // Motor Left
                motor(4);
                break;
            case 5:
                pusher(1);
                break;
            case 6:
                pusher(0);
                break;
            /*
            * case other_number:
            *   lcd("some_coord");
            *   break;
            */
            
        }
    }
}