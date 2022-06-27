#ref = https://youtu.be/WymCpVUPWQ4
import numpy as np
import pyautogui as pg
import cv2 as cv
import os
import time
from windowcapture import WindowCapture

window_name = None
# window_name = None
wincap = WindowCapture(window_name)



loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # # we need to do this if we use 3rd party way to capture window screenshot
    # # we need to convert screenshot format to input that open cv understand.
    # screenshot = np.array(screenshot)
    # # Convert RGB to BGR 
    # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
  
    cv.imshow('Computer Vision', screenshot)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()


    # press "q" with the output windows focused to exist.
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")