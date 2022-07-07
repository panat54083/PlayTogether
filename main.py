#ref = https://youtu.be/WymCpVUPWQ4
from numpy import rec
import pyautogui as pg
import cv2 as cv
import time
from windowcapture import WindowCapture
from vision import Vision
from edgefilter import EdgeFilter 
import pyautogui
window_name = "ApowerMirror Livestream"
# window_name = None
wincap = WindowCapture(window_name)
vision_exclamation = Vision('picture/edge exclam.jpg')
vision_exclamation.init_control_gui()
loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # crop screen shot for detecting only exclamation point
    crop_screenshot = screenshot
    x, w, y, h = [650, 300, 100, 200]
    crop_screenshot = crop_screenshot[y:y+h, x:x+w]
    # do object detection
    edgefilter = EdgeFilter(8, 1, 1, 100, 200)
    edge_process_img = vision_exclamation.apply_edge_filter(crop_screenshot, None)
    rectangles = vision_exclamation.find(edge_process_img, 0.30)
    output_img = vision_exclamation.draw_rectangles(edge_process_img, rectangles)
    
    # display the processed image
    cv.imshow('Computer Vision', output_img)

    # take bot actions
    if len(rectangles) > 0:
        # to click
        # targets = pyautogui.move(1495,631)
        # target = wincap.get_screen_position(targets[0])
        pyautogui.click(x=1582, y=751)
        # time.sleep(1.5)
        # pyautogui.click(x=1482, y=751)

    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press "q" with the output windows focused to exist.
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")