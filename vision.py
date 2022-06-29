from turtle import window_width
import cv2 as cv
from cv2 import line
import numpy as np

# imread Methods
# https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html#ga61d9b0126a3e57d9277ac48327799c80
playtogeter_img = cv.imread('picture/test2.PNG', cv.IMREAD_GRAYSCALE)
exclamation_img = cv.imread('picture/exclamation point2.PNG', cv.IMREAD_GRAYSCALE)

result = cv.matchTemplate(playtogeter_img, exclamation_img, cv.TM_CCOEFF_NORMED)

# print(result)

threshold = 0.90
locations = np.where(result >= threshold)
# print(locations)

# we can zip those up into position tuples 
# list[start:stop:step] *list == unpack lists
locations = list(zip(*locations[::-1]))
print(locations)

if locations:
    print('Found..')

    ecm_w = exclamation_img.shape[1]
    ecm_h = exclamation_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # need to loop over all the locations and draw their rectangle
    for loc in locations:
        # determine the box positions
        top_left = loc
        print(top_left)
        bottom_right = (top_left[0] + ecm_w, top_left[1] + ecm_h)
        print(bottom_right)

        # draw the box
        cv.rectangle(playtogeter_img, top_left, bottom_right, 
                    line_color, line_type)

    cv.imshow('Matches', playtogeter_img)
    cv.waitKey()

else:
    print("Not found..")
    

