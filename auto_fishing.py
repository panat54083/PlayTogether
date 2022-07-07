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

window_name = "ApowerMirror Livestream"
# window_name = None
wincap = WindowCapture(window_name)

vision_exclamation = Vision('picture/edge exclam.jpg')
# vision_exclamation = Vision('picture/IMG_1545.jpg')    
vision_exclamation.init_control_gui()
loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # crop screen shot for detecting only exclamation point
    crop_screenshot = screenshot
    x, w, y, h = [550, 400, 100, 200]
    # screenshot = crop_screenshot[y:y+h, x:x+w]

    # pre-process the image
    # hsvfilter = HsvFilter(18, 0, 255, 58, 46, 255, 0, 0, 0, 0)
    edgefilter = EdgeFilter(8, 1, 1, 100, 200)
    pre_process_img = vision_exclamation.apply_hsv_filter(screenshot)

    edge_process_img = vision_exclamation.apply_edge_filter(screenshot, None)
    # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGBA2GRAY)
    # do object detection
    rectangles = vision_exclamation.find(edge_process_img, 0.50)

    output_img = vision_exclamation.draw_rectangles(edge_process_img, rectangles)


    # display the processed image
    # cv.imshow('HSV filter', pre_process_img)
    cv.imshow('Edge filter', edge_process_img)
    # cv.imshow('Computer Vision', screenshot)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press "q" with the output windows focused to exist.
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")