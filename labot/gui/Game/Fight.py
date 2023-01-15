
from ..Algorithm.FightAlgorithm import FightAlgorithm
from ..utils.Constants import Constants as Constants
from ..utils.Sockets import Socket
import json
import math as Math

class Fight:

    def __init__(self, gui, Player, Map):
        print("HELLO from fight")
        self.Gui = gui
        self.Player = Player
        self.Map = Map

        self.fightRoutine = False

        self.isFighting = False
        self.monsters = []

        self.playerMoved = False

        self.spellsCastedMonsters = []
        self.spellsCasted = []

        self.monsterRestrictions = {
            'maximumNumber': None,
            'ids': None
        }

        self.FightAlgorithm = FightAlgorithm(self.Map, self.Player, self)

    def getMonsterIdFromCellId(self, cellId):
        for monster in self.monsters:
            if monster['cellId'] == cellId:
                return monster['id']

    def passTurn(self):
        self.Gui.qSocket.put(Socket.fightPassTurn())

    def useSpell(self, spellId, cellId):
        monsterId = 0
        for monster in self.monsters:
            if monster['cellId'] == cellId:
                self.spellsCastedMonsters.append({
                    'spellId': spellId,
                    'monsterId': monster['id']
                })
                break
        
        self.spellsCasted.append(int(spellId))

        self.Gui.qSocket.put(Socket.useSpell(spellId, cellId))

    def setFightReady(self):
        self.Gui.qSocket.put(Socket.setFightReady())

    def getDistance(self, X1, Y1, X2, Y2):
        dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
        return int(dist)
    
    

    def waitTime(self, time):
        self.Gui.waitTime(time)

    def deleteMonster(self, monsterId):
        self.monsters = [x for x in self.monsters if x['id'] != monsterId]

    def updateGUI(self):
        for item in self.Gui.fightMonstersTree.get_children():
            self.Gui.fightMonstersTree.delete(item)
        i = 1
        for monster in self.monsters:
            self.Gui.fightMonstersTree.insert('', 'end', text=str(i), values=(str(monster['id']), str(monster['cellId']), str(0)))
            i = i + 1


    def socketHandler(self, action, data):
        
        if action == 'fightEnded':
            print('### fight ended')
            self.isFighting = False
    
        
        if action == "fightStarted":
            print('### fight stared')
            # print("---")
            # print(self.monsters)
            # print(self.Player.cellId)
            # print("Start Positions :", self.Map.fightStartCells)
            # print()

            self.isFighting = True
            self.FightAlgorithm.findStartPosition()

        if action == 'fightUpdateMonsterCells':
            self.monsters = data['monstersCellId']
        
        if action == 'updateActorPosition':
            for monster in self.monsters:
                if monster['id'] == data['actorId']:
                    monster['cellId'] = data['cellId']
                    break
        
        if action == 'fightDeathMonster':
            print('(((((((((((((((( FIGHT DEATH MONSTER. Monsters :', self.monsters)
            self.deleteMonster(data['id'])
            print('Nouveaux monstres :::', self.monsters)
            if len(self.monsters) == 0:
                self.isFighting = False
        
        if action == "fightMonsterSlide":
            for monster in self.monsters:
                if monster['id'] == data['id']:
                    monster['cellId'] = data['cellId']
                    break
        
        if action == "fightTurnStart":
            self.spellsCastedMonsters = []
            self.spellsCasted = []
            print('### fight turn start')
            if self.fightRoutine == True:
                self.FightAlgorithm.actionHandle(action)
        
        elif action == "allActionsFinished" and self.isFighting == True:
            print('(((((((((((((((( ALL ACTIONS FINISHED. Monsters :', self.monsters)
            if self.fightRoutine == True:
                self.FightAlgorithm.actionHandle(action)

        
        

        self.updateGUI()



