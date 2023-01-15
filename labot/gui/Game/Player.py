from ..utils.Sockets import Socket

class Player:
    def __init__(self, Gui, Map):
        print("HELLO from player")
        self.name = ""
        self.level = 0
        self.id = 0
        self.Map = Map
        self.cellId = 999

        self.readyForNextFight = False

        self.autoFight = False
        self.monsterTargeted = None

        self.Gui = Gui

        self.isMoving = False
        
        self.characteristics = {
            "PA": 0,
            "PM": 1,
            "PDV": 2
        }

        self.spells = [
            # {
            #     'name': "Fleche explosive",
            #     'id': 13065,
            #     'PO': 14,
            #     'POmin': 1,
            #     'PA': 4,
            #     'align': False,
            #     'freeZone': True,
            #     'zone': [
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1,  1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1,- 1, -1, -1, -1, -1],
            #     ],
            #     'maxPerTarget': 1,
            #     'maxPerTurn': 2
            # },
            # {
            #     'name': "Fleche enflammée",
            #     'id': 13051,

            # },
            {
                'name': "Fleche répulsive",
                'id': 13072,
                'PO': 11,
                'POmin': 1,
                'PA': 3,
                'align': True,
                'freeZone': True,
                'zone': [
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1,  0,  1,  0, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1,- 1, -1, -1, -1, -1],
                ],
                'maxPerTarget': 2,
                'maxPerTurn': 2
            }
            # {
            #     'name': "Fleche glacée",
            #     'id': 13049,
            #     'PO': 16,
            #     'POmin': 3,
            #     'PA': 3,
            #     'align': False,
            #     'freeZone': True,
            #     'zone': [
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1,  1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1, -1, -1, -1, -1, -1],
            #         [-1,-1, -1, -1,- 1, -1, -1, -1, -1],
            #     ],
            #     'maxPerTarget': 2,
            #     'maxPerTurn': 3
            # },
        ]


    def moveToCellId(self, cellId):
        self.Gui.Window.clickCellId(cellId)


    def updateGUI(self):
        
        self.Gui.vPlayerLevel.set("Level: " + str(self.level))
        self.Gui.vPlayerName.set("Name: " + str(self.name))
        self.Gui.vPlayerId.set("ID: " + str(self.id))
        self.Gui.vPlayerCellId.set("Cell ID: " + str(self.cellId))

        if self.isMoving:
            self.Gui.vPlayerMovement.set("Moving...")
        else:
            self.Gui.vPlayerMovement.set("Idle")

            
        self.Gui.vPlayerPA.set("PA:" + str(self.characteristics['PA']))
        self.Gui.vPlayerPM.set("PM:" + str(self.characteristics['PM']))
        self.Gui.vPlayerPDV.set("PDV: " + str(self.characteristics['PDV']))

    def move(self, fromCellId, toCellId):
        fromCID = fromCellId
        if fromCID == 999:
            fromCID = self.cellId
        print("fromCID, toCellId :", fromCID, toCellId)
        path = self.Map.pathFinder.GetCompressedPath(fromCID, toCellId)
        self.Map.PFSetMap()
        print("path :", path)
        if path != None and len(path) > 0:
            self.Gui.qSocket.put(Socket.moveToCellId(path, float(self.Map.mapId)))
        
    
    def fightOnMap(self, monster = None):
        if len(self.Map.monsters) > 0:
            self.autoFight = True
            monsterTarget = self.Map.monsters[0]
            if monster != None:
                monsterTarget = monster
            cellId = monsterTarget['cellId']
            self.move(999, cellId)
            self.monsterTargeted = monsterTarget
        else:
            print(">>>>>>>>> plus de monstres sur la carte")
        
    
    def handleMovementConfirm(self):
        print("--handle movement confirm| cellid :", self.cellId)
        print("---", self.monsterTargeted)
        print("---", self.Map.monsters)
        if self.autoFight == True:
            if self.monsterTargeted != None:
                for monster in self.Map.monsters:
                    if self.monsterTargeted['groupId'] == monster['groupId']:
                        if self.monsterTargeted['cellId'] == monster['cellId']:
                            self.Gui.qSocket.put(Socket.attackMonster(self.monsterTargeted['groupId']))
                            self.monsterTargeted = None
                            break
                        else:
                            self.autoFight = False
                            self.fightOnMap(monster)
                            break
            #else:
            #    self.fightOnMap()


    def socketHandler(self, action, data):

        # #print("-- Player socket handler :", action, data)
        # if action == 'fightEnded':
        #     print("<<<<< fight ended ")
        #     print("PLAYER cellId ::", self.cellId)
        
        if action == 'playerInformations':
            self.name = str(data['name'])
            self.level = int(data['level'])
            self.id = data['id']
        
        if action == 'playerUpdateCellId':
            self.isMoving = False
            self.cellId = int(data['cellId'])
            if self.autoFight == True and self.monsterTargeted != None:
                self.handleMovementConfirm()
            if self.readyForNextFight == True:
                self.readyForNextFight = False
                self.fightOnMap()
        
        if action == 'mapInformations':
            if self.autoFight == True:
                self.readyForNextFight = True

        
        if action == 'PlayerMovementStart':
            self.isMoving = True

        if action == 'playerUpdateCharacteristics':
            self.characteristics = {
                "PA": int(data['PA']),
                "PM": int(data['PM']),
                "PDV": int(data['PDV'])
            }
        
        if action == 'fightPlayerSlide':
            self.cellId = data['cellId']
        
        #if action == 'playerUpdateLossCharacteristic':
        #    self.characteristics[data['type']] = int(self.characteristics[data['type']]) + int(data['delta'])

        if action == 'playerUpdateCharacteristicsList':
            characteristics = data['characteristics']

            for characteristic in characteristics:
                self.characteristics[characteristic['type']] = int(characteristic['value'])

        self.updateGUI()
    
