#ref = https://youtu.be/WymCpVUPWQ4
from json import detect_encoding
from cv2 import rectangle
import numpy as np
import pyautogui as pg
import cv2 as cv
import os
import time
from windowcapture import WindowCapture
from vision import Vision

window_name = "ApowerMirror Livestream"
# window_name = None
wincap = WindowCapture(window_name)

# load the trained model
cascade_exclamation = cv.CascadeClassifier('cascade/cascade.xml')

vision_exclamation = Vision(None)
loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    
    # do object detection
    rectangles = cascade_exclamation.detectMultiScale(screenshot)
    # draw the detection results onto the original image
    detection_image = vision_exclamation.draw_rectangles(screenshot, rectangles)
    
    cv.imshow('Computer Vision', detection_image)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()
    key = cv.waitKey(1)
    # press "q" with the output windows focused to exist.
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)
        


print("Done...")