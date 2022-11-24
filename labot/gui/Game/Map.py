from ..utils.FileReader import FileReader
from ..utils.Constants import Constants
import time

class Map:
    def __init__(self, gui):
        print("HELLO from map")
        self.monsters = []
        self.mapId = 0
        self.subAreaId = 0
        self.fightStartCells = []
        self.Gui = gui

        self.nonWalkableCells = []
        self.wallCells = []

        self.nonWalkableCellList = []
        self.wallCellList = []

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

        if action == 'mapInformations':
            self.mapId = data['mapId']
            self.subAreaId = data['subAreaId']
            self.setMonsters(data['monsters'])
            self.fightStartCells = data['fightStartCells']
            self.getNonWalkableCells(int(data['mapId']))
            
        if action == 'updateActorPosition':
            for group in self.monsters:
                if group['groupId'] == data['actorId']:
                    group['cellId'] = data['cellId']
                    break
        
        if action == 'removeElement':
            self.deleteMonster(data['id'])
        
        self.updateGUI()

    def getNonWalkableCells(self, mapId):

        self.wallCellList = []
        self.nonWalkableCellList = []
        mapData = FileReader.openJsonMap(mapId)
        mapDataCell = mapData['cells']
        
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
        self.Gui.qSocket.put(("enterHavenBag", ""))
        self.Gui.waitCallback("mapHavenBagInformations")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(("useHavenBagZaap", ""))
        print(">>> MAP : PUTTED useHavenBagZaap")
        self.Gui.waitCallback('ZaapDestinationsMessage')
        print("--- MAP: end wait")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(("teleportBrakmarZaap", ""))
        print(">>> MAP : PUTTED teleportBrakmarZaap")
        self.Gui.waitCallback('mapInformations')
        print("--- MAP: end wait")
        time.sleep(2)

        self.Gui.Window.clickCellId(65) # Clique sur Zappi 
        print(">>> MAP : PUTTED moveToCellId 63")
        self.Gui.waitCallback('TeleportDestinationsMessage')
        print("--- MAP: end wait")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(("teleportStableZaapi", ""))
        print(">>> MAP : PUTTED teleportStableZaapi")
        self.Gui.waitCallback('mapInformations')
        print("--- MAP: end wait")
        time.sleep(1000/1000)

        self.Gui.Player.moveToCellId(314)
        self.Gui.waitCallback("stableOpened")

        print('<<<<<< CALLBACK FINISHED')


        
