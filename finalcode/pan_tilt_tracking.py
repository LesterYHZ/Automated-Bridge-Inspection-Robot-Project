# the goal of this file is to run all of the 4 independent processes
# that are used to control the vision system components as well as update the variables needed for the FSM
# global variable updates allow these processes to constantly update each other

		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
# python pan_tilt_tracking.py


# import necessary packages
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
import pantilthat as pth
import argparse  # used for command line arguments
import signal
import time
import sys
import cv2

global panAngle
global tiltAngle
global washerFound


# define the range for the motors
servo1Range = (-90, 90)
servo2Range = (0, 45)

# function to handle keyboard interrupt (looking for way to exit script)
# kills all 4 processes at once
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")

	# disable the servos
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)

	# exit
	sys.exit()

def obj_center(args, objX, objY, centerX, centerY):  # first process
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# start the video stream and wait for the camera to warm up
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# initialize the object center finder
	obj = ObjCenter(args["canny"])

	# loop indefinitely
	while True:
		# grab the frame from the threaded video stream and flip it
		# vertically (since our camera was upside down)
		frame = vs.read()
		frame = cv2.flip(frame, 0)

		# calculate the center of the frame as this is where we will
		# try to keep the object
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# find the object's location
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc
		# global variable for FSM
		washerFound = (len(rects))
	
		# draw keypoints on frame
		# Draw detected blobs as red circles.
		# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
		# the size of the circle corresponds to the size of blob
		if rect is not None:
			im_with_keypoints = cv2.drawKeypoints(canny, keypoints, np.array([]), (0, 0, 255),
											  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		# Display the resulting frame with blobs
		cv2.imshow('Pan-Tilt blob Tracking', im_with_keypoints)
		out.write(im_with_keypoints)
		cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# create a PID and initialize it
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# calculate the error (camera frame center - object location)
		error = centerCoord.value - objCoord.value

		# update the value (servo angle in degrees)
		output.value = p.update(error)

def in_range(val, start, end):  # servo range checker
	# determine the input value is in the supplied range
	return (val >= start and val <= end)

def set_servos(pan, tlt):  # drives servos to specific angle values (-90-90) and (0 - 45)
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# loop indefinitely
	while True:
		# the pan and tilt angles are reversed
		panAngle = -1 * pan.value
		tltAngle = -1 * tlt.value

		# if the pan angle is within the range, pan
		if in_range(panAngle, servoRange[0], servoRange[1]):
			pth.pan(panAngle)

		# if the tilt angle is within the range, tilt
		if in_range(tltAngle, servoRange[0], servoRange[1]):
			pth.tilt(tltAngle)

		return(panAngle, tltAngle)

# check to see if this is the main body of execution
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	# specify paths
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "blob_canny", type=str, required=True,
		help="path to input blob and canny detector ")
	args = vars(ap.parse_args())

	# start a manager for managing process-safe variables
	with Manager() as manager:
		# enable the servos
		pth.servo_enable(1, True)
		pth.servo_enable(2, True)

		# set integer values for the object center (x, y)-coordinates
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# set integer values for the object's (x, y)-coordinates
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# pan and tilt values will be managed by independed PIDs
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)

		# set PID values for panning
		panP = manager.Value("f", 0.09)
		panI = manager.Value("f", 0.08)
		panD = manager.Value("f", 0.002)

		# set PID values for tilting
		tiltP = manager.Value("f", 0.11)
		tiltI = manager.Value("f", 0.10)
		tiltD = manager.Value("f", 0.002)

		# we have 4 independent processes
		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))
		processPanning = Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX))
		processTilting = Process(target=pid_process,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos = Process(target=set_servos, args=(pan, tlt))

		# start all 4 processes
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		# join all 4 processes
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()

		# disable the servos
		pth.servo_enable(1, False)
		pth.servo_enable(2, False)
