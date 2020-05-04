# goal of this code is to create a PID controller used to update our servos positions with
# outputs sum of PID
# takes error as an input
# sleep can be adjusted to the specific needed for the electromechanical hardware being used
# important to make sure PID is not updating faster than objects(and their coordinates
# are being detected

# import necessary packages
import time

class PID:
	def __init__(self, kP=1, kI=0, kD=0):  # The constructor
		# initialize gains
		self.kP = kP  # proportional to error
		self.kI = kI  # eliminates historical error/ steady state error
		self.kD = kD  # converges faster, eliminates future error

	def initialize(self):  # Initializes values and set current & prev time stamps
		# intialize the current and previous time
		self.currTime = time.time()
		self.prevTime = self.currTime

		# initialize the previous error
		self.prevError = 0

		# initialize the term result variables
		self.cP = 0
		self.cI = 0
		self.cD = 0

	def update(self, error, sleep=0.2):  # Calculations are made
		# pause for a bit so servos can respond in time, can adjust time by "sleep="
		time.sleep(sleep)

		# grab the current time and calculate delta time
		self.currTime = time.time()
		deltaTime = self.currTime - self.prevTime  # updates don't always come at same time

		# delta error
		deltaError = error - self.prevError

		# proportional term
		self.cP = error

		# integral term
		self.cI += error * deltaTime

		# derivative term and prevent divide by zero
		self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

		# save previous time and error for the next update
		self.prevTime = self.currTime
		self.prevError = error

		# sum the terms and return
		return sum([
			self.kP * self.cP,
			self.kI * self.cI,
			self.kD * self.cD])