# goal of this code is to use OpenCV's Blob detector to detector the washers using an
# edge detection filter (not color)
# it needs the video frame as an input
# outputs the x and y coordinate to the closest blob detected
# the blob parameters are needed to limit the things that are detected as a "blob"
# in our case we only want the washers to be detected as blobs

# import necessary packages
import imutils
import numpy as np
import cv2

class ObjCenter:
	def __init__(self, haarPath):  # The constructor
		# load OpenCV's blob detector

		# setting parameters for detector to detect certain blobs only
		params = cv2.SimpleBlobDetector_Params()

		# Change thresholds
		params.minThreshold = 100
		params.maxThreshold = 300

		# Filter by Area.
		params.filterByArea = True
		params.minArea = 10
		# params.maxArea = 5000

		# Filter by Circularity
		params.filterByCircularity = True
		params.minCircularity = 0.1
		# params.maxCircularity = 1

		# Filter by Convexity
		params.filterByConvexity = 1
		params.minConvexity = 0.2
		params.maxConvexity = 1

		# Filter by Inertia
		params.filterByInertia = 1
		params.minInertiaRatio = 0.01
		# params.maxInertiaRatio = 1

		# Create a detector with the specified parameters
		# blob detector detects blobs from video frame
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3:
			self.detector = cv2.SimpleBlobDetector(params)
		else:
			self.detector = cv2.SimpleBlobDetector_create(params)


	def update(self, frame, frameCenter):
		# convert the frame to grayscale, blur image and extract edges
		# uses edges to determine a blob (AKA washer)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (5, 5), 0)
		canny = cv2.Canny(blur, 10, 50)

		# detect all blobs in the input frame
		rects = self.detector.detect(canny)

		# check to see if a blob was found
		if len(rects) > 0:  # blob is detected
			# extract x and y coordinates from detected blobs
			# blob coordinates give the center of blob detected
			# blobs are numbered from the closet y (base of camera) to the furthers (away from the camera)
			number_blob = (len(rects))
			print('number of washers', number_blob) # print out number of blobs
			pts_array = cv2.KeyPoint_convert(rects)  # creates an array of the x and y coordinates for center of blobs
			pts = np.array(pts_array)  # converts to an array we can pull from
			x = pts[0, 0]  # closest blob detected x point
			y = pts[0, 1]  # closest blob detected y point
			blobX = int(x)
			blobY = int(y)

			# return the center (x, y)-coordinates of the first/closet blob
			return ((blobX, blobY), pts[0])

		# otherwise no blobs were found, so return the center of the
		# frame
		return (frameCenter, None)