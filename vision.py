from turtle import window_width
import cv2 as cv
import numpy as np

playtogeter_img = cv.imread('picture/test2.PNG', cv.IMREAD_UNCHANGED)
getting_img = cv.imread('picture/getting_button.PNG', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(playtogeter_img, getting_img, cv.TM_CCOEFF_NORMED)

# get the best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left poistion: %s' % str(max_loc))
print('Best match confidence: %s' % str(max_val))

threshold = 0.8
if max_val >= threshold:
    print('Found..')

    # get dimentions of the getting_fish_button image
    getting_w = getting_img.shape[1]
    getting_h = getting_img.shape[0]
    
    top_left = max_loc
    bottom_right = (top_left[0] + getting_w, top_left[1] + getting_h)
    # print(bottom_right)
    
    cv.rectangle(playtogeter_img, top_left, bottom_right,
                    color = (0,0,255), thickness = 2, lineType=cv.LINE_4)
    cv.imshow('Result', playtogeter_img)                
    cv.waitKey()
else:
    print('Not found..')



