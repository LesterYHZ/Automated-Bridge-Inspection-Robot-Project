# List of States for Pi--Arduino signals

- Pi converts an int signal to byte and sends it to Arduino through Serial Communicaiton
- Arduino receives the byte signal and converts it back to int
- The int signal functions as an indicator of which state the robot is at and what function Arduino needs to proceed
- Arduino functions include 
  - LCD screen (All 49 Possible Coord Readings)
  - Motor Forward
  - Motor Backward
  - Motor Stop
  - Motor Turn Right
  - Motor Turn Left
  - Pusher Servo Move (Activate / Reset)

| Signal   |      Function      |
|:----------:|:-------------:|
| 0 |Motor Stop|
| 1 |Motor Forward|
| 2 |Motor Backward|
| 3 |Motor Right|
| 4 |Motor Left|
| 5 |Pusher Activate|
| 6 |Pusher Reset|
| 100 | LCD Reset|
| 101 | LCD A1|
| ... | ... |
| 149 | LCD G7|

