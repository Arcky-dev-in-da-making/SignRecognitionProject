import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1) #Class based on detecting the hands
offset = 20
imgSize = 300

folder = "Data/space"
counter = 0
while True:
    try:
        success, img = cap.read() #Create webcam
        hands, img = detector.findHands(img) #Finding and mapping the hands
        if hands: #Cropping the image of hands for precise detection
            hand = hands[0]
            x, y, w, h = hand['bbox'] #taking parameters from boundary box.

            imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255 #White image

            imgCrop = img[y-offset:y + h+offset, x-offset:x + w+offset] #Cropped image(only for hands)

            imgCropShape = imgCrop.shape


            aspectRatio = h/w

            if aspectRatio > 1:
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize-wCal)/2)
                imgWhite[:, wGap:wCal+wGap] = imgResize  # merging the images
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images


            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImgWhite", imgWhite)
        cv2.imshow("Image",img)
        key = cv2.waitKey(1)
        if key == ord("s"):
            counter += 1
            cv2.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite)
            print(counter)
    except cv2.error:
        print("hello")