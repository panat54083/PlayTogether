from turtle import window_width
import cv2 as cv
import numpy as np

# imread Methods
# https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html#ga61d9b0126a3e57d9277ac48327799c80
playtogeter_img = cv.imread('picture/test2.PNG', cv.IMREAD_GRAYSCALE)
exclamation_img = cv.imread('picture/exclamation point2.PNG', cv.IMREAD_GRAYSCALE)

result = cv.matchTemplate(playtogeter_img, exclamation_img, cv.TM_CCOEFF_NORMED)

# get the best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left poistion: %s' % str(max_loc))
print('Best match confidence: %s' % str(max_val))

threshold = 0.3
if max_val >= threshold:
    print('Found..')

    # get dimentions of the exclamation point image
    exclamation_w = exclamation_img.shape[1]
    exclamation_h = exclamation_img.shape[0]
    
    top_left = max_loc
    bottom_right = (top_left[0] + exclamation_w, top_left[1] + exclamation_h)
    # print(bottom_right)
    
    cv.rectangle(playtogeter_img, top_left, bottom_right,
                    color = (0,0,255), thickness = 2, lineType=cv.LINE_4)
    cv.imshow('Result', playtogeter_img)                
    cv.waitKey()
else:
    print('Not found..')



