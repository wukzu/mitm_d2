

import threading
import queue
import tkinter as tk  # PEP8: `import *` is not preferred
import time
from concurrent.futures import ThreadPoolExecutor

import win32gui

import win32api
import win32con
import sys
sys.setrecursionlimit(10000)


def idToPix(id, onCroppedScreen, delta_x=0, delta_y=0):
    if onCroppedScreen: 
        base_x = 0
        base_y = 0
    else:
        base_x = g_base_x
        base_y =  g_base_y

    xhg,yhg = cell_w / 2,cell_h / 2

    if delta_x: xhg = xhg + delta_x
    if delta_y: yhg = yhg + delta_y

    xhg = xhg - 2
    

    dx = cell_w + 0.5
    dy = cell_h + 0.25
    y,x = divmod(id,14)
    if y%2==1: x+=.5
    y/=2
    return round(base_x+xhg  +x*dx),round(yhg + y*dy)


class Window():
    def __init__(self):
        self.title = "Lorienta - Dofus 2.66.1.11"
        self.GameWindow = win32gui.FindWindow(None, self.title)
        win32gui.MoveWindow(self.GameWindow, -8, 0, 716, 600, True)

    def click(self,x,y):
        lParam = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.GameWindow, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(self.GameWindow, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(self.GameWindow, win32con.WM_LBUTTONUP, None, lParam)


class GUI(threading.Thread):
    
    def __init__(self, qSocket, qForm):
        super().__init__()
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.waitingVar = tk.BooleanVar()

        self.qSocket = qSocket
        self.qForm = qForm
        
        self.window = Window()

        self.waiting = False
        self.var = tk.StringVar()
        self.waitingVar = tk.BooleanVar()
        self.waitingVar.set(False)
        self.var.set("Initiated")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = int(screen_width*.12)
        height = int(screen_height)
        x = int(screen_width - width)
        y = int(screen_height*.025)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

        label = tk.Label(self.root, textvariable=self.var)
        buttonLeft = tk.Button(self.root, text ="Left", command = self.goLeft)
        buttonLeft.pack()
        buttonRight = tk.Button(self.root, text ="Right", command = self.goRight)
        buttonRight.pack()
        label.pack()

        self.listbox = tk.Listbox(
            self.root,
            width=1, height=1,
            selectmode=tk.EXTENDED
        )
        self.listbox.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)

 
        # run first time after 100ms (0.1 second)
        self.root.after(100, self.check_queue)

        self.root.mainloop()
        
    def goLeft(self):
        self.window.click(6, 270)
    def wait(self):
        self.waitingVar.set(True)
        self.root.wait_variable(self.waitingVar)
    def goRight(self):
        print('go right click')

        print('[GUI] sending hello')
        self.qSocket.put(("hello", "bbb"))
        
        self.wait()
        


        print('GO RIGHT CALLBACK SUCCESS')
        
        #self.window.click(692, 270)
    def nextFunc(self):
        print("NEXT called")
        
    def check_queue(self):
        print("[GUI] checking queue... waiting: " + str(self.waiting))
        while not self.qForm.empty():
            msg = self.qForm.get()
            print("[GUI] check_queue msg : " + str(msg))
            if msg == 'callback':
                self.waitingVar.set(False)

    #     # run again after 100ms (0.1 second)
        self.root.after(500, self.check_queue)
            
    def wait_callback(self):
        print("[GUI] wait_callback... waiting: " + str(self.waiting))
        while not self.qForm.empty():
            msg = self.qForm.get()
            print("--- msg :" + msg)
            if msg == 'callback':
                self.waitingVar.set(False)
        if self.waitingVar.get() == True:
            self.root.after(1000, self.wait_callback)


class Bridge():
    def __init__(self, qSocket, qForm):
        self.test = "hello"
        self.qSocket = qSocket
        self.waitForCallback = False
        self.qForm = qForm

    def handle(self):
        i = 0
        while True: 
            time.sleep(1)
            print("[bridge] handle loop...")
            if not self.qSocket.empty():
                action = self.qSocket.get()
                print('[bridge] action :' + str(action))
            i = i + 1
            if i == 7:
                print("[Bridge] sending 'callback'")
                self.qForm.put("callback")




qSocket = queue.Queue()
qForm = queue.Queue()
bridge = Bridge(qSocket, qForm)
gui = GUI(qSocket, qForm)


t1 = threading.Thread(target=bridge.handle, args=())
t1.start()



# def expensive_operation():
#     time.sleep(5)
#     return 6

# executor = ThreadPoolExecutor(1)
# future = executor.submit(expensive_operation)

# print(future.result())

