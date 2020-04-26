// pins 
#define enA 9
#define enB 10
#define motorL1 4
#define motorL2 5
#define motorR1 6
#define motorR2 7
#define encoderL1 11
#define encoderL2 12
#define encoderR1 2
#define encoderR2 3 

// variables
byte incomingData = '0';
int signal = 0;
int Speed = 0;
int counter = 0; 
int aState = 0;
int aLastState = 0;  

// sub-functions
void Serial_Intialization();
void Receive_Signal();
void Motor(int state);  // state is from Serial reading
void Stop();
void Forward();
void Backward();
void Right();
void Left();

// setup 
void setup() {
    // pinmode setup 
    for (int num = 4; num <=10; num++) {
        pinMode(num,OUTPUT);
    }
    pinMode(encoderL1,INPUT);
    pinMode(encoderL2,INPUT);
    pinMode(encoderR1,INPUT);
    pinMode(encoderR2,INPUT);

    // serial communication setup 
    Serial_Intialization();
    Serial.println("Start");
}

// main loop 
void loop() {
    Receive_Signal();
}

// sub-functions 
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
        }
    }
}

void Motor(int state) {
    switch(state) {
        case 0:
            Stop();
            break;
        case 1:
            Forward();
            break;
        case 2:
            Backward();
            break;
        case 3:
            Right();
            break;
        case 4:
            Left();
            break;
        default:
            Serial.println("Not a motor state");
            break;
    }
}

void Stop() {
    // both motors stop 
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, LOW);
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, LOW);
}

void Forward() {
    // both motors move forward 
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, HIGH);
    digitalWrite(motorL2, LOW);
    digitalWrite(motorR1, HIGH);
    digitalWrite(motorR2, LOW);
}

void Backward() {
    // both motors move backward 
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, HIGH);
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, HIGH);
}

void Right() {
    // left motor moves forward and right motor stops
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, HIGH);
    digitalWrite(motorL2, LOW);
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, LOW);
}

void Left() {
    // right motor stops and left motor moves backward 
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, LOW);
    digitalWrite(motorR1, HIGH);
    digitalWrite(motorR2, LOW);
}

int encoder_count(int outputA,int outputB) {
    aState = digitalRead(outputA); // Reads the "current" state of the outputA
    // If the previous and the current state of the outputA are different, that means a Pulse has occured
    if (aState != aLastState){     
        // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
        if (digitalRead(outputB) != aState) { 
            counter ++;
        } else {
            counter --;
        }
    } 
    aLastState = aState; // Updates the previous state of the outputA with the current state
}