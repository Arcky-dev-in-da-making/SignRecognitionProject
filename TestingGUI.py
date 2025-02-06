#Importing modules
import cv2
import numpy as np

#Loading image
imgName = input("Enter image name:")
img = cv2.imread('{}.jpg').format(imgName)

#Convert image to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#Define range of red color in HSV
lowerRed = np.array([0, 100, 100])
upperRed = np.array([10, 255, 255])

#Threshold the HSV image to get only red colors (binary mask application)
binMask = cv2.inRange(hsv, lowerRed, upperRed)

#Bitwise-AND mask and original image
imgFinal = cv2.bitwise_and(img, img, mask=binMask)

# Display the original image and the red color detected image
cv2.imshow('Original', img)
cv2.imshow('Red', imgFinal)
cv2.waitKey(0)
cv2.destroyAllWindows()