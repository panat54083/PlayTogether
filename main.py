#ref = https://youtu.be/WymCpVUPWQ4
from numpy import rec
import pyautogui as pg
import cv2 as cv
import time
from windowcapture import WindowCapture
from vision import Vision
from edgefilter import EdgeFilter 
import pyautogui
window_name = "LDPlayer"
# window_name = None
wincap = WindowCapture(window_name)
win_auto = pyautogui.getWindowsWithTitle(window_name)[0]
x_win = win_auto.topleft[0]
y_win = win_auto.topleft[1]

vision_exclamation = Vision('picture/edge exclamLD.jpg')
vision_take = Vision('picture/takeLD.jpg')

vision_exclamation.init_control_gui()
loop_time = time.time()
while(True):

    screenshot = wincap.get_screenshot()
    # crop screen shot for detecting only exclamation point
    # x, w, y, h = [650, 300, 100, 200]
    #LDplayer
    x, w, y, h = [650, 300, 200, 200]
    crop_screenshot1 = screenshot[y:y+h, x:x+w]
    # do object detection
    edgefilter = EdgeFilter(8, 1, 1, 100, 200)
    edge_process_img = vision_exclamation.apply_edge_filter(crop_screenshot1)
    exclamation_rectangles = vision_exclamation.find(edge_process_img, 0.30)
    output_img = vision_exclamation.draw_rectangles(edge_process_img, exclamation_rectangles)

    # take detector and poistion
    # x, w, y, h = [1000, 500, 500, 100]
    #LDplayer
    x, w, y, h = [1000, 500, 685, 100]
    crop_screenshot2 = screenshot[y:y+h, x:x+w]

    take_rectangles = vision_take.find(crop_screenshot2, 0.5)
    take_detector = vision_take.draw_rectangles(crop_screenshot2, take_rectangles)

    # display the processed image
    cv.imshow('Computer Vision1', output_img)
    cv.imshow('Computer Vision2', take_detector)

    # take bot actions
    if len(exclamation_rectangles) > 0:
        # to click
        # targets = pyautogui.move(1495,631)
        # target = wincap.get_screen_position(targets[0])
        # pyautogui.click(x=1550, y=751)
        pyautogui.click(x=x_win+1000+400, y=y_win+685)
        # time.sleep(1.5)
        # pyautogui.click(x=1482, y=751)
    if len(take_rectangles) > 0:
        # https://pyautogui.readthedocs.io/en/latest/roadmap.html
        
        points = vision_take.get_click_points(take_rectangles)
        x_point = points[0][0]
        y_point = points[0][1]

        
        # pyautogui.moveTo(x= x_point+x_win+1000, y=y_point+y_win+500)
        # LDPlayer
        pyautogui.click(x= x_point+x_win+1000, y=y_point+y_win+685)
        time.sleep(1)
        pyautogui.click(x= 1494, y=635)
        
    print("FPS {}".format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press "q" with the output windows focused to exist.
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print("Done...")