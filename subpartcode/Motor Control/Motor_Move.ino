#define enA
#define enB
#define motorL1
#define motorL2
#define motorR1
#define motorR2

int Speed = 0;

void Motor(int state);  // state is from Serial reading
void Stop();
void Forward();
void Backward();
void Right();
void Left();

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
    // left motor moves forward and right motor moves backward
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, HIGH);
    digitalWrite(motorL2, LOW);
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, HIGH);
}

void Left() {
    // right motor moves forward and left motor moves backward 
    analogWrite(enA, Speed);
    analogWrite(enB, Speed);
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, HIGH);
    digitalWrite(motorR1, HIGH);
    digitalWrite(motorR2, LOW);
}
