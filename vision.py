from unittest import result
import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter
from edgefilter import EdgeFilter

class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"
    
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


    def find(self, screen_img, threshold = 0.5, max_result=10):
        
        result = cv.matchTemplate(screen_img, self.target_img, self.method)
        # print(result)

        locations = np.where(result >= threshold)
        # we can zip those up into position tuples 
        # list[start:stop:step] *list == unpack lists
        locations = list(zip(*locations[::-1]))
        # print(locations)
        
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

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
        if len(rectangles) > max_result:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_result]
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
        # create gui window with controls for adjusting arguments in real-time
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

        # trackbars for edge creation
        cv.createTrackbar('KernelSize', self.TRACKBAR_WINDOW, 1, 30, nothing)
        cv.createTrackbar('ErodeIter', self.TRACKBAR_WINDOW, 1, 5, nothing)
        cv.createTrackbar('DilateIter', self.TRACKBAR_WINDOW, 1, 5, nothing)
        cv.createTrackbar('Canny1', self.TRACKBAR_WINDOW, 0, 200, nothing)
        cv.createTrackbar('Canny2', self.TRACKBAR_WINDOW, 0, 500, nothing)
        # Set default value for Canny trackbars
        cv.setTrackbarPos('KernelSize', self.TRACKBAR_WINDOW, 5)
        cv.setTrackbarPos('Canny1', self.TRACKBAR_WINDOW, 100)
        cv.setTrackbarPos('Canny2', self.TRACKBAR_WINDOW, 200)

    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter 

    # returns a Canny edge filter object based on the control GUI values
    def get_edge_filter_from_controls(self):
        # Get current positions of all trackbars
        edge_filter = EdgeFilter()
        edge_filter.kernelSize = cv.getTrackbarPos('KernelSize', self.TRACKBAR_WINDOW)
        edge_filter.erodeIter = cv.getTrackbarPos('ErodeIter', self.TRACKBAR_WINDOW)
        edge_filter.dilateIter = cv.getTrackbarPos('DilateIter', self.TRACKBAR_WINDOW)
        edge_filter.canny1 = cv.getTrackbarPos('Canny1', self.TRACKBAR_WINDOW)
        edge_filter.canny2 = cv.getTrackbarPos('Canny2', self.TRACKBAR_WINDOW)
        return edge_filter

    # given an image and HSV filter, apply the filter and return the resulting image.
    # if a filter is not supoplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV format
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()
        
        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shif_channel(s, hsv_filter.sAdd)
        s = self.shif_channel(s, -hsv_filter.sSub)
        v = self.shif_channel(v, hsv_filter.vAdd)
        v = self.shif_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)
        
        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    # given an image and a Canny edge filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_edge_filter(self, original_image, edge_filter=None):
        # if we haven't been given a defined filter, use the filter values from the GUI
        if not edge_filter:
            edge_filter = self.get_edge_filter_from_controls()

        kernel = np.ones((edge_filter.kernelSize, edge_filter.kernelSize), np.uint8)
        eroded_image = cv.erode(original_image, kernel, iterations=edge_filter.erodeIter)
        dilated_image = cv.dilate(eroded_image, kernel, iterations=edge_filter.dilateIter)

        # canny edge detection
        result = cv.Canny(dilated_image, edge_filter.canny1, edge_filter.canny2)

        # convert single channel image back to BGR
        img = cv.cvtColor(result, cv.COLOR_GRAY2BGR)

        return img

    def shif_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount

        return c

    def match_keypoints(self, original_image, patch_size=32):
        min_match_count = 5

        orb = cv.ORB_create(edgeThreshold=0, patchSize=patch_size)
        keypoints_needle, descriptors_needle = orb.detectAndCompute(self.needle_img, None)
        orb2 = cv.ORB_create(edgeThreshold=0, patchSize=patch_size, nfeatures=2000)
        keypoints_haystack, descriptors_haystack = orb2.detectAndCompute(original_image, None)

        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH, 
                table_number=6,
                key_size=12,    
                multi_probe_level=1)

        search_params = dict(checks=50)

        try:
            flann = cv.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors_needle, descriptors_haystack, k=2)
        except cv.error:
            return None, None, [], [], None

        # store all the good matches as per Lowe's ratio test.
        good = []
        points = []

        for pair in matches:
            if len(pair) == 2:
                if pair[0].distance < 0.7*pair[1].distance:
                    good.append(pair[0])

        if len(good) > min_match_count:
            print('match %03d, kp %03d' % (len(good), len(keypoints_needle)))
            for match in good:
                points.append(keypoints_haystack[match.trainIdx].pt)
            #print(points)
        
        return keypoints_needle, keypoints_haystack, good, points

    def centeroid(self, point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]
        
if "__main__" == __name__:
    pass