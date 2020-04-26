void setup() {
  // put your setup code here, to run once:
  Serial.begin( 9600 );
}

void loop() {
  // put your main code here, to run repeatedly:
   // listen for the data
  if ( Serial.available() > 0 ) {
    // read a numbers from serial port
    String loc = Serial.readString();
    
    //Serial print input
    Serial.print("Location: ");
    Serial.println(loc);
  }
}
