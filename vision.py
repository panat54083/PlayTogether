from turtle import window_width
import cv2 as cv
from cv2 import line
from cv2 import rectangle
import numpy as np

class Vision:

    # proerties
    target_img = None
    tg_w = 0
    tg_w = 0
    method = None
    # constructor
    def __init__(self, taget_img_path, method = cv.TM_CCOEFF_NORMED):

        # imread Methods
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html#ga61d9b0126a3e57d9277ac48327799c80
        # self.target_img = cv.imread(taget_img_path, cv.IMREAD_GRAYSCALE)
        self.target_img = cv.imread(taget_img_path, cv.IMREAD_UNCHANGED)
        # print(self.target_img.dtype)
        self.tg_w = self.target_img.shape[1]
        self.tg_h = self.target_img.shape[0]
        
        # there are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


    def find(self, screen_img, threshold = 0.5):
        
        result = cv.matchTemplate(screen_img, self.target_img, self.method)
        # print(result)

        locations = np.where(result >= threshold)
        # we can zip those up into position tuples 
        # list[start:stop:step] *list == unpack lists
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.tg_w, self.tg_h]
            # make it double because if there is only one rec when you groups your rectangles, it will be disapear.
            rectangles.append(rect)
            rectangles.append(rect)

        # print(rectangles)
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        # print(rectangles)

        return rectangles
        
    def get_click_points(self, rectangles):

        points = []

        for (x, y, w, h) in rectangles:

            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # save points
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, screen_img, rectangles):

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        # determine the box positions
        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(screen_img, top_left, bottom_right, line_color, line_type)
        
        return screen_img
    
    def draw_crosshair(sefl, screen_img, points):
        marker_color = (255, 0 ,255)
        marker_type = cv.MARKER_CROSS
        
        for (center_x, center_y) in points:
            cv.drawMarker(screen_img, (center_x, center_y), marker_color, marker_type)

        return screen_img

if "__main__" == __name__:
    pass