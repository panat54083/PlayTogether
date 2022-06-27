import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    w = 0
    h = 0
    hwnd = None

    def __init__(self, window_name = None):

        
        if window_name == None:    
            self.hwnd = None
            self.w = 1920
            self.h = 1680

        else:
            self.hwnd = win32gui.FindWindow(None, window_name)  
            if not self.hwnd:
                raise Exception('Window not found:{}'.format(window_name))

            # get the window size
            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]

        self.bmpfilenamename = "debug.bmp" #set this

    def get_screenshot(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (0,0), win32con.SRCCOPY)
        
        # save the screenshot
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h,self.w,4)


        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # get rid of the alpha channel data
        img = img[...,:3]

        img = np.ascontiguousarray(img)

        return img

    def list_window_name(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0], pos[1])

if __name__ == "__main__":
    
    a = WindowCapture()
    a.list_window_name()

