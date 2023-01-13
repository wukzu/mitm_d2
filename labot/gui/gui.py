
import threading
import queue
import tkinter as tk  # PEP8: `import *` is not preferred
import tkinter.ttk as ttk
from tkinter.constants import *

import time
import json

from .Window.Window import Window
from .Game.Map import Map
from .Game.Player import Player
from .Game.Fight import Fight
from .Game.Mount import Mount

class GUI(threading.Thread):
    
    def __init__(self, qForm, qSocket, fnQuit):
        super().__init__()
        self.start()
        self.langs = []
        self.listbox = None
        self.textArea = None
        self.listTest = []
        self.Map = None
        self.Player = None
        self.Fight = None
        self.Mount = None

        self.fnQuit = fnQuit
        
        self.qForm = qForm
        self.qSocket = qSocket

        self.Window = None
        self.waitingVar = None
        
    def run(self):
        self.root = tk.Tk()

        self.gameVersion = ""
        
        self.Map = Map(self)
        self.Player = Player(self)
        self.Fight = Fight(self, self.Player, self.Map)
        self.Mount = Mount(self)

        self.callbackToWait = ""

        self.waitingVar = tk.BooleanVar()
        self.waitingVar.set(False)

        self.vLogs = tk.IntVar()
        self.vParsedLogs = tk.IntVar()

        self.var = tk.StringVar()
        self.vPlayerName = tk.StringVar()
        self.vPlayerLevel = tk.StringVar()
        self.vPlayerId = tk.StringVar()
        self.vPlayerMovement = tk.StringVar()
        
        self.vPlayerPA = tk.StringVar()
        self.vPlayerPM = tk.StringVar()
        self.vPlayerPDV = tk.StringVar()
        self.vPlayerCellId = tk.StringVar()

        self.monsters = tk.StringVar()
        self.vMapId = tk.StringVar()
        self.vSubAreaId = tk.StringVar()
        
        self.var.set("Launched")
        self.vPlayerName.set("-")
        self.vPlayerLevel.set("-")
        self.vPlayerId.set("-")
        self.vPlayerMovement.set("Idle")
        
        self.vPlayerPA.set("0")
        self.vPlayerPM.set("1")
        self.vPlayerPDV.set("0/0")
        self.vPlayerCellId.set("999")
        
        self.vMapId.set("000000000")
        self.vSubAreaId.set("000")

        self.root.geometry("350x650+660+210")
        self.root.minsize(136, 1)
        self.root.maxsize(3844, 1153)

        #self.logsCheckbox = tk.Checkbutton(self.root, text='Go to mount stable',variable=self.vLogs, onvalue=1, offvalue=0, command=self.Map.routeToMountStable)
        #self.logsCheckbox.pack()
        self.btnMounts =  tk.Button(self.root, text ="Dragrodindes", command = self.openDDWindow)
        self.btnMounts.pack()

        self.lStatus = tk.Label(self.root, textvariable=self.var)
        self.lStatus.place(relx=0.657, rely=0.015, height=36, width=98)
        self.lStatus.configure(anchor='e')

        self.PlayerFrame = tk.LabelFrame(self.root)
        self.PlayerFrame.place(relx=0.029, rely=0.062, relheight=0.275, relwidth=0.937)
        self.PlayerFrame.configure(relief='groove')
        self.PlayerFrame.configure(text='''Personnage''')

        self.lPlayerName = tk.Label(self.PlayerFrame, textvariable=self.vPlayerName)
        self.lPlayerName.place(relx=0.064, rely=0.123, height=33, width=137, bordermode='ignore')
        self.lPlayerName.configure(anchor='w')

        self.lPlayerLevel = tk.Label(self.PlayerFrame, textvariable=self.vPlayerLevel)
        self.lPlayerLevel.place(relx=0.064, rely=0.268, height=34, width=137, bordermode='ignore')
        self.lPlayerLevel.configure(anchor='w')

        self.lPlayerMovement = tk.Label(self.PlayerFrame, textvariable=self.vPlayerMovement)
        self.lPlayerMovement.place(relx=0.064, rely=0.43, height=34, width=137, bordermode='ignore')
        self.lPlayerMovement.configure(anchor='w')
    
        self.lPlayerId = tk.Label(self.PlayerFrame, textvariable=self.vPlayerId)
        self.lPlayerId.place(relx=0.552, rely=0.123, height=33, width=137, bordermode='ignore')
        self.lPlayerId.configure(anchor='w')

        self.lPlayerPA = tk.Label(self.PlayerFrame, textvariable=self.vPlayerPA)
        self.lPlayerPA.place(relx=0.064, rely=0.726, height=34, width=62, bordermode='ignore')
        self.lPlayerPA.configure(anchor='w')

        self.lPlayerPM = tk.Label(self.PlayerFrame, textvariable=self.vPlayerPM)
        self.lPlayerPM.place(relx=0.357, rely=0.726, height=34, width=94, bordermode='ignore')
        self.lPlayerPM.configure(anchor='w')

        self.lPlayerPDV = tk.Label(self.PlayerFrame, textvariable=self.vPlayerPDV)
        self.lPlayerPDV.place(relx=0.649, rely=0.726, height=34, width=94, bordermode='ignore')
        #self.lPlayerPDV.configure(activebackground="#f9f9f9")textvariable=self.vPlayerId
        self.lPlayerPDV.configure(anchor='w')

        self.TSeparator2 = ttk.Separator(self.PlayerFrame)
        self.TSeparator2.place(relx=0.032, rely=0.667, relwidth=0.929, bordermode='ignore')

        self.TSeparator1 = ttk.Separator(self.root)
        self.TSeparator1.place(relx=0.486, rely=0.111,  relheight=0.2)
        self.TSeparator1.configure(orient="vertical")
        
        self.lPlayerCellId = tk.Label(self.PlayerFrame, textvariable=self.vPlayerCellId)
        self.lPlayerCellId.place(relx=0.552, rely=0.302, height=34, width=137, bordermode='ignore')
        self.lPlayerCellId.configure(anchor='w')

        #----------------------------

        self.Labelframe1 = tk.LabelFrame(self.root)
        self.Labelframe1.place(relx=0.029, rely=0.354, relheight=0.337, relwidth=0.943)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Map''')

        self.lMapId = tk.Label(self.Labelframe1, textvariable=self.vMapId)
        self.lMapId.place(relx=0.061, rely=0.137, height=27, width=136, bordermode='ignore')
        self.lMapId.configure(activebackground="#f9f9f9")
        self.lMapId.configure(anchor='w')

        self.lMapSubAreaId = tk.Label(self.Labelframe1, textvariable=self.vSubAreaId)
        self.lMapSubAreaId.place(relx=0.485, rely=0.137, height=27, width=147, bordermode='ignore')
        self.lMapSubAreaId.configure(activebackground="#f9f9f9")
        self.lMapSubAreaId.configure(anchor='w')

        self.monstersTree = ttk.Treeview(self.Labelframe1, column=("c1", "c2", "c3"), show='headings')
        self.monstersTree.place(relx=0.0, rely=0.32, relheight=0.662, relwidth=0.98, bordermode='ignore')

        self.monstersTree.column("# 1", anchor=CENTER)
        self.monstersTree.heading("# 1", text="ID")
        self.monstersTree.column("# 2", anchor=CENTER)
        self.monstersTree.heading("# 2", text="Cell ID")
        self.monstersTree.column("# 3", anchor=CENTER)
        self.monstersTree.heading("# 3", text="Monsters")

        self.Labelframe2 = tk.LabelFrame(self.root)
        self.Labelframe2.place(relx=0.029, rely=0.708, relheight=0.269, relwidth=0.943)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(text='''Combat''')

        self.fightMonstersTree = ttk.Treeview(self.Labelframe2, column=("c1", "c2", "c3"), show='headings')
        self.fightMonstersTree.place(relx=0.0, rely=0.166, relheight=0.766, relwidth=0.982, bordermode='ignore')

        self.fightMonstersTree.column("# 1", anchor=CENTER)
        self.fightMonstersTree.heading("# 1", text="ID")
        self.fightMonstersTree.column("# 2", anchor=CENTER)
        self.fightMonstersTree.heading("# 2", text="Cell ID")
        self.fightMonstersTree.column("# 3", anchor=CENTER)
        self.fightMonstersTree.heading("# 3", text="PDV")


        #buttonLeft = tk.Button(self.root, text ="Quit", command = self.quitProgram)
        #buttonRight = tk.Button(self.root, text ="Right", command = self.goRight)

        #buttonLeft.pack()

        # label.pack()
        # lPlayerName.pack()
        # lPlayerLevel.pack()
        # lPlayerId.pack()
        # lPlayerMovement.pack()
        # lMonsters.pack()
        # lMapId.pack()
        # lSubAreaId.pack()

        # self.listbox = tk.Listbox(
        #     self.root,
        #     width=1, height=1,
        #     selectmode=tk.EXTENDED
        # )
        # self.listbox.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        self.root.after(50, self.check_queue)

        self.root.mainloop()
        
    def quitProgram(self):
        self.fnQuit()

    def openDDWindow(self):
        self.DDWindow = tk.Toplevel(self.root)
        self.DDWindow.title("New Window")

        self.DDWindow.geometry("500x300")
        tk.Label(self.DDWindow, text ="Dragodinde manager").pack()
        self.btnMountlapping =  tk.Button(self.DDWindow, text ="Start baffeurs", command = self.Mount.toggleSlapping)
        self.btnMountlapping.pack()
        
        self.btnMountCaressing =  tk.Button(self.DDWindow, text ="Start caresseurs", command = self.Mount.toggleCaressing)
        self.btnMountCaressing.pack()

        self.btnMountStamina =  tk.Button(self.DDWindow, text ="Start foudroyeurs", command = self.Mount.toggleStamina)
        self.btnMountStamina.pack()
        
        self.btnMountLove =  tk.Button(self.DDWindow, text ="Start dragofesses", command = self.Mount.toggleLove)
        self.btnMountLove.pack()
        
        self.btnMountMaturity =  tk.Button(self.DDWindow, text ="Start maturié", command = self.Mount.toggleMaturity)
        self.btnMountMaturity.pack()

        self.lDDInfos = tk.Label(self.DDWindow, text = "-")
        self.lDDInfos.pack()

        self.sql_commands = tk.Text(self.DDWindow)
        self.sql_commands.insert(tk.INSERT, "#self.qSocket.put(('',''))")
        self.sql_commands.pack()
        self.submit_button = tk.Button(self.DDWindow, text=' Submit ', command=self.submit_click)
        self.submit_button.pack()
    
    def submit_click(self):
        exec(self.sql_commands.get("1.0", 'end'))

    def changeParsedLogs(self):
        if self.vParsedLogs.get() == 1:
            self.qSocket.put(('activateParsedLogs', ''))
        else:
            self.qSocket.put(('deactivateParsedLogs', ''))

    
    def changeLogs(self):
        if self.vLogs.get() == 1:
            self.qSocket.put(('activateLogs', ''))
        else:
            self.qSocket.put(('deactivateLogs', ''))
    
    def waitTime(self, time):
        var = tk.IntVar()
        self.root.after(time, var.set, 1)
        print("waiting ", time, "...")
        self.root.wait_variable(var)

    def waitCallback(self, callback):
        self.waitingVar.set(True)
        self.callbackToWait = callback
        self.root.wait_variable(self.waitingVar)

    def check_queue(self):
        while not self.qForm.empty():
            action, data = self.qForm.get()
            #print("[GUI] check_queue RECV action : " + str(action) + ' - data :' + str(data))

            #print("GUI  qForm :: received ", action)
            infos = {}
            if data != "":
                infos = json.loads(data)

            
            if action == "gameVersion":
                print("qForm game version :", infos['version'])
                self.gameVersion = infos['version']
            if action == "Initialized":
                print("--- Initialize the windows")
                self.Window = Window(self.gameVersion)
                self.var.set("Initialized")
            if action == self.callbackToWait:
                #print("GUI  RECEIVED CALLBACK ", action)
                self.callbackToWait= ""
                self.waitingVar.set(False)
            # if action == 'callback':
            #     print("[GUI] setting waiting to False")
            #     self.waitingVar.set(False)


            self.Map.socketHandler(action, infos)
            self.Player.socketHandler(action, infos)
            self.Fight.socketHandler(action, infos)
            self.Mount.socketHandler(action, infos)

        self.root.after(50, self.check_queue)