#ref = https://youtu.be/WymCpVUPWQ4
from cv2 import rectangle
import numpy as np
import pyautogui as pg
import cv2 as cv
import os
import time
from windowcapture import WindowCapture
from vision import Vision

# window_name = "ApowerMirror Livestream"
window_name = None
wincap = WindowCapture(window_name)

vision_exclamation = Vision('picture/exclamation point3.jpg')
# vision_exclamation = Vision('picture/IMG_1545.jpg')    

loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # # we need to do this if we use 3rd party way to capture window screenshot
    # # we need to convert screenshot format to input that open cv understand.
    # screenshot = np.array(screenshot)
    # # Convert RGB to BGR 

    # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGBA2GRAY)

    # do object detection
    rectangles = vision_exclamation.find(screenshot, 0.7)

    output_img = vision_exclamation.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Computer Vision', output_img)
    # cv.imshow('Computer Vision', screenshot)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press "q" with the output windows focused to exist.
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")