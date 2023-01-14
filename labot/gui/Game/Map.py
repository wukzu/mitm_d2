from ..utils.FileReader import FileReader
from ..utils.Constants import Constants
from ..utils.Sockets import Socket
from ..Algorithm.PathFinder.Pathfinder import Pathfinder
import time
import json

class Map:
    def __init__(self, gui):
        print("HELLO from map")
        self.monsters = []
        self.mapData = None
        self.mapId = 0
        self.subAreaId = 0
        self.fightStartCells = []
        self.Gui = gui

        self.autoFight = False
        self.monsterTargeted = None

        self.nonWalkableCells = []
        self.wallCells = []
        self.zaap = {}

        self.nonWalkableCellList = []
        self.wallCellList = []

        self.pathFinder = Pathfinder()

    def setMonsters(self, monsters):
        self.monsters = monsters.copy()
    
    def deleteMonster(self, groupId):
        self.monsters = [x for x in self.monsters if x['groupId'] != groupId]

    def updateMonsterPosition(self, groupId, position):
        for group in self.monsters:
            if group['groupId'] == groupId:
                group['cellId'] = position
    
    def updateGUI(self):
        
        for item in self.Gui.monstersTree.get_children():
            self.Gui.monstersTree.delete(item)
        i = 1
        for group in self.monsters:
             self.Gui.monstersTree.insert('', 'end', text=str(i), values=(str(group['groupId']), str(group['cellId']), str(len(group['monsters']))))
             i = i + 1
            
        self.Gui.vMapId.set("Map ID: " + str(self.mapId))
        self.Gui.vSubAreaId.set("MapSubAera ID: " + str(self.subAreaId))
    
    def socketHandler(self, action, data):

        if action == 'mapHavenBagInformations':
            self.zaap = data['zaap']
        

        if action == 'mapInformations':
            self.mapId = data['mapId']
            self.subAreaId = data['subAreaId']
            self.setMonsters(data['monsters'])
            self.fightStartCells = data['fightStartCells']
            self.getNonWalkableCells(int(data['mapId']))
            
            self.zaap = data['zaap']
            
        if action == 'updateActorPosition':
            for group in self.monsters:
                if group['groupId'] == data['actorId']:
                    group['cellId'] = data['cellId']
                    break
        
        if action == 'removeElement':
            self.deleteMonster(data['id'])
        
        if action == 'fightEnded':
            print("------- fight ended : cell id player :", self.Gui.Player.cellId)
        
        self.updateGUI()

    


    def PFSetMap(self):
        self.pathFinder.SetMap(self.mapData, True)

    def getNonWalkableCells(self, mapId):

        self.wallCellList = []
        self.nonWalkableCellList = []
        self.mapData = FileReader.openJsonMap(mapId)
        self.pathFinder.SetMap(self.mapData, True)
        mapDataCell = self.mapData['cells']
        
        nonWalkableLine = []
        wallLine = []

        nonWalkableCells = []
        wallCells = []

        for cellLine in Constants.cells_game:
            for cellId in cellLine:
                if cellId != -1:
                    if mapDataCell[cellId]['mov'] == False or mapDataCell[cellId]['nonWalkableDuringFight'] == True or mapDataCell[cellId]['los'] == False:
                        nonWalkableLine.append(1)
                        if mapDataCell[cellId]['los'] == False:
                            wallLine.append(1)
                        else:
                            wallLine.append(0)
                    else:
                        nonWalkableLine.append(0)
                        wallLine.append(0)
                else:
                    nonWalkableLine.append(1)
                    wallLine.append(1)
            nonWalkableCells.append(nonWalkableLine)
            wallCells.append(wallLine)
            nonWalkableLine = []
            wallLine = []
        self.nonWalkableCells = nonWalkableCells
        self.wallCells = wallCells
        # for cellLine in nonWalkableCells:
        #     print(cellLine)
        # print("-------")
        # print("-------")
        # print("-------")
        # for nLosLine in wallCells:
        #     print(nLosLine)

        for x in range(0, len(nonWalkableCells)):
            for y in range(0, len(nonWalkableCells[x])):
                if nonWalkableCells[x][y] == 1:
                    self.nonWalkableCellList.append([x, y])
        
        for x in range(0, len(wallCells)):
            for y in range(0, len(wallCells[x])):
                if wallCells[x][y] == 1:
                    self.wallCellList.append([x, y])

    def routeToMountStable(self):
        self.Gui.Mount.routeToUpMount()
        return
        
        self.Gui.qSocket.put(Socket.EnterHavenBag(self.Gui.Player.id))
        
        self.Gui.waitCallback("mapHavenBagInformations")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(Socket.useHavenbagZaap(self.zaap))
        self.Gui.waitCallback('ZaapDestinationsMessage')
        
        time.sleep(1000/1000)

        self.Gui.qSocket.put(Socket.teleportBrakmar())
        self.Gui.waitCallback('mapInformations')
        
        time.sleep(2)

        self.Gui.Window.clickCellId(65) # Clique sur Zappi 
        self.Gui.waitCallback('TeleportDestinationsMessage')
        
        time.sleep(1000/1000)

        self.Gui.qSocket.put(Socket.teleportAnimals())
        self.Gui.waitCallback('mapInformations')
        
        time.sleep(1000/1000)

        self.Gui.Player.moveToCellId(314)
        self.Gui.waitCallback("stableOpened")
        print('<<<<<< CALLBACK FINISHED, timer 4 sec')
        time.sleep(4000/1000)

        print('<<<<<< Launch routeToUpMount()')

        #self.Gui.Mount.routeToUpMount()


        
