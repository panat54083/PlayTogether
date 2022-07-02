#ref = https://youtu.be/WymCpVUPWQ4
from cv2 import rectangle
import numpy as np
import pyautogui as pg
import cv2 as cv
import os
import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from edgefilter import EdgeFilter

# window_name = "ApowerMirror Livestream"
window_name = None
wincap = WindowCapture(window_name)

vision_exclamation = Vision('picture/process_egg.jpg')
# vision_exclamation = Vision('picture/IMG_1545.jpg')    
vision_exclamation.init_control_gui()
loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # # we need to do this if we use 3rd party way to capture window screenshot
    # # we need to convert screenshot format to input that open cv understand.
    # screenshot = np.array(screenshot)
    # # Convert RGB to BGR 
    # pre-process the image
    # hsvfilter = HsvFilter(18, 0, 255, 58, 46, 255, 0, 0, 0, 0)
    pre_process_img = vision_exclamation.apply_hsv_filter(screenshot)

    edge_process_img = vision_exclamation.apply_edge_filter(screenshot)
    # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGBA2GRAY)
    # do object detection
    # rectangles = vision_exclamation.find(pre_process_img, 0.45)

    # output_img = vision_exclamation.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('HSV filter', pre_process_img)
    cv.imshow('Edge filter', edge_process_img)
    # cv.imshow('Computer Vision', screenshot)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press "q" with the output windows focused to exist.
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")