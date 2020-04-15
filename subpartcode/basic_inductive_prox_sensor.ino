/*
Basic Inductive Proximity Sensor Code
"Target Hit!" when washer close to sensor
*/
int limitSwitch = 13;
int state = LOW;

void setup() {
  
  Serial.begin(9600);
  pinMode(limitSwitch,INPUT);
  
}

void loop() {
  
    int val = digitalRead(limitSwitch);

    if( val != state ){
       state = val;
       Serial.print("Sensor value = ");
       if( state == 0 )
         Serial.println( "(0) Target Hit!" );
       else
         Serial.println( "(1) None");
    }
}
