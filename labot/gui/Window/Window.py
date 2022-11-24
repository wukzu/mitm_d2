import win32gui
import win32api
import win32con

from ..utils.Constants import Constants

def idToPix(id, onCroppedScreen, delta_x=0, delta_y=0):
    if onCroppedScreen: 
        base_x = 0
        base_y = 0
    else:
        base_x = Constants.g_base_x
        base_y =  Constants.g_base_y

    xhg,yhg = Constants.cell_w / 2, Constants.cell_h / 2

    if delta_x: xhg = xhg + delta_x
    if delta_y: yhg = yhg + delta_y

    xhg = xhg - 2
    
    dx = Constants.cell_w + 0.5
    dy = Constants.cell_h + 0.25

    y,x = divmod(id, 14)
    if y%2==1: x+=.5
    y/=2
    return round(base_x+xhg  +x*dx),round(yhg + y*dy)

class Window():
    def __init__(self):
        self.title = "Lorienta - Dofus 2.65.6.25"
        self.GameWindow = win32gui.FindWindow(None, self.title)
        win32gui.MoveWindow(self.GameWindow, -8, 0, 716, 600, True)

    def clickCellId(self, cellId):
        print("window :clickCellId ", cellId)

        x,y = idToPix(cellId, False)
        self.click(x, y)

    def click(self,x,y):
        lParam = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.GameWindow, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(self.GameWindow, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(self.GameWindow, win32con.WM_LBUTTONUP, None, lParam)