from turtle import window_width
import cv2 as cv
from cv2 import line
from cv2 import rectangle
import numpy as np


def findClickPosition(taget_img_path, screen_img, threshold = 0.9, debug_mode = None):
    
    # imread Methods
    # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html#ga61d9b0126a3e57d9277ac48327799c80
    # screen_img = cv.imread(screen_img, cv.IMREAD_GRAYSCALE)
    target_img = cv.imread(taget_img_path, cv.IMREAD_GRAYSCALE)

    tg_w = target_img.shape[1]
    tg_h = target_img.shape[0]

    match_method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(screen_img, target_img, match_method)
    # print(result)

    locations = np.where(result >= threshold)
    # we can zip those up into position tuples 
    # list[start:stop:step] *list == unpack lists
    locations = list(zip(*locations[::-1]))
    # print(locations)

    # create the list of [x, y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), tg_w, tg_h]
        # make it double because if there is only one rec when you groups your rectangles, it will be disapear.
        rectangles.append(rect)
        rectangles.append(rect)

    # print(rectangles)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
    # print(rectangles)
    points = []
    if len(rectangles):
        print('Found..')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255 )
        marker_type = cv.MARKER_CROSS
        # need to loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:

            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # save points
            points.append((center_x, center_y))

            if debug_mode == "rectangles":
                # determine the box positions
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # draw the box
                cv.rectangle(screen_img, top_left, bottom_right, 
                            line_color, line_type)
            
            elif debug_mode == "points":
                cv.drawMarker(screen_img, (center_x, center_y), marker_color, marker_type)

    if debug_mode:
        cv.imshow('Matches', screen_img)
        # cv.waitKey()

    # else:
    #     print("Not found..")

    return points

# points = findClickPosition('picture/exclamation point2.PNG', 'picture/test2.PNG',
#                              threshold = 0.9, debug_mode='rectangles')
# print(points)