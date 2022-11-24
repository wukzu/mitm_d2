

class Player:
    def __init__(self, Gui):
        print("HELLO from player")
        self.name = ""
        self.level = 0
        self.id = 0
        self.cellId = 999

        self.Gui = Gui

        self.isMoving = False
        
        self.characteristics = {
            "PA": 0,
            "PM": 1,
            "PDV": 2
        }

        self.spells = [
            {
                'name': "Fleche explosive",
                'id': 13065,
                'PO': 12,
                'POmin': 1,
                'PA': 4,
                'align': False,
                'freeZone': True,
                'zone': [
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1,  1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1,- 1, -1, -1, -1, -1],
                ],
                'maxPerTarget': 1,
                'maxPerTurn': 2
            },
            {
                'name': "Fleche répulsive",
                'id': 13072,
                'PO': 9,
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
            },
            {
                'name': "Fleche glacée",
                'id': 13049,
                'PO': 14,
                'POmin': 3,
                'PA': 3,
                'align': False,
                'freeZone': True,
                'zone': [
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1,  1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1,-1, -1, -1,- 1, -1, -1, -1, -1],
                ],
                'maxPerTarget': 2,
                'maxPerTurn': 3
            },
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

    def socketHandler(self, action, data):

        #print("-- Player socket handler :", action, data)
        
        if action == 'playerInformations':
            self.name = str(data['name'])
            self.level = int(data['level'])
            self.id = data['id']
        
        if action == 'playerUpdateCellId':
            self.isMoving = False
            self.cellId = int(data['cellId'])
        
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
    
