
def go_straight(distance,safe_distance):
    """
        if sonar(front) > safe_distance --> boldly go straight, there's no wall in front
    """
    if sonar(front) < safe_distance:
        wall_detected(safe_distance)
    else:
        if sonar(left) == distance:
            # robot right on target path, keep going straight
            Send_Signal(1)
        elif sonar(left) < distance:
            # robot on the left of target path, turn right a little bit
            Send_Signal(3)
        elif sonar(left) > distance:
            # robot on the right of target path, turn left a little bit
            Send_Signal(4)
        else:
            pass 

def wall_detected(distance):
    """
        if sonar(front) < safe_distance --> there's wall in front so stop and get back
    """
    Send_Signal(0)
    while sonar(front) < distance:
        Send_Signal(2)
    Send_Signal(0)