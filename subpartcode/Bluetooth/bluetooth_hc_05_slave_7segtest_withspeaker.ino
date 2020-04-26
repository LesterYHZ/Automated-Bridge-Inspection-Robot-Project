//Bluetooth Arduino code: HC-05 is in slave mode
  //Raspberry Pi is in master mode
  //Prints letter and then digit on seven-segment display

//Declarations
int led = 13;
char letter;
String digit1;
int digit;

//Declare pins of 7-digit display
const int pinA = 5;
const int pinB = 4;
const int pinC = 10;
const int pinD = 11;
const int pinE = 12;
const int pinF = 6;
const int pinG = 7;

//Speaker uses an analog pin
int speakerPin = A2;
int freq = 250;
int duration = 2000;

// the setup routine runs once when you press reset:
void setup() {
  Serial.begin( 9600 );
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT); //to visualize
  pinMode(speakerPin, OUTPUT); //to hear
}

// the loop routine runs over and over again forever:
void loop() {
  // listen for the data
  if ( Serial.available() > 0 ) {
    // read a numbers from serial port
    String loc = Serial.readString();

    //Serial print input
    Serial.print("Location: ");
    Serial.println(loc);

    //Split up letter and digit
    letter = char(loc[0]);
    digit1 = String(loc[1]);
    digit = digit1.toInt();
    
    //Call functions
    delay(1000); //delay 1 sec
    printLetter(letter);
    delay(2000); //delay 2 sec
    printDigit(digit);
    delay(2000); //delay 2 sec
    //Note: Will need to update delays

    // turn the led on to indicate "finished"
    digitalWrite(led, HIGH);

    //Turn on speaker
    tone(speakerPin,freq,duration);

    //Clear seven seg display
    clearSevenSeg();

    //turn the led off to indicate "reset"
    delay(duration); //wait for speaker to finish
    digitalWrite(led, LOW);
  }
}


//Function to print letter
void printLetter(char letter)
{
  //Character A
  if (letter == 'A')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Character B
  if (letter == 'B')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Character C
  if (letter == 'C')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, LOW);
  }

  //Character D
  if (letter == 'D')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, LOW);
  }

  //Character E
  if (letter == 'E')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Character F
  if (letter == 'F')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Character G
  if (letter == 'G')
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }
}

//Function to print digit
void printDigit(int digit)
{
  //Digit 1
  if (digit == 1)
  {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, LOW);
  }

  //Digit 2
  if (digit == 2)
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, LOW);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, HIGH);
  }

  //Digit 3
  if (digit == 3)
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, HIGH);
  }

  //Digit 4
  if (digit == 4)
  {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Digit 5
  if (digit == 5)
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Digit 6
  if (digit == 6)
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, LOW);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, HIGH);
    digitalWrite(pinE, HIGH);
    digitalWrite(pinF, HIGH);
    digitalWrite(pinG, HIGH);
  }

  //Digit 7
  if (digit == 7)
  {
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    digitalWrite(pinC, HIGH);
    digitalWrite(pinD, LOW);
    digitalWrite(pinE, LOW);
    digitalWrite(pinF, LOW);
    digitalWrite(pinG, LOW);
  }

}

//Function to clear seven segment display
void clearSevenSeg()
{
  digitalWrite(pinA,LOW);
  digitalWrite(pinB,LOW);
  digitalWrite(pinC,LOW);
  digitalWrite(pinD,LOW);
  digitalWrite(pinE,LOW);
  digitalWrite(pinF,LOW);
  digitalWrite(pinG,LOW);
}
