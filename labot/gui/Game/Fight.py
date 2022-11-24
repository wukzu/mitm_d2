
from ..Algorithm.FightAlgorithm import FightAlgorithm
from ..utils.Constants import Constants as Constants
from ..utils.Sockets import Socket
import json
import math as Math

class Fight:

    def __init__(self, gui, Player, Map):
        print("HELLO from fight")
        self.Gui = gui

        self.isFighting = False
        self.monsters = []

        self.Player = Player
        self.Map = Map

        self.playerMoved = False

        self.spellsCastedMonsters = []
        self.spellsCasted = []

        self.FightAlgorithm = FightAlgorithm(self.Map, self.Player, self)

    def getMonsterIdFromCellId(self, cellId):
        for monster in self.monsters:
            if monster['cellId'] == cellId:
                return monster['id']

    def passTurn(self):
        print('---->>>> sending PASS TURN')
        self.Gui.qSocket.put(Socket.fightPassTurn())

    def useSpell(self, spellId, cellId):
        print('---->>>> sending useSpell', spellId, cellId)
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
        print('---->>>> sending PASS TURN')
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


            # [{'id': -2, 'cellId': 484}]
            # 458
            # {'PA': 8, 'PM': 4, 'PDV': 1364}
        
        
        if action == "fightMonsterSlide":
            for monster in self.monsters:
                if monster['id'] == data['id']:
                    monster['cellId'] = data['cellId']
                    break
        
        if action == "fightTurnStart":
            self.spellsCastedMonsters = []
            self.spellsCasted = []
            print('### fight turn start')
            # print("---")
            # print(self.monsters)
            # print(self.Player.cellId)
            # print(self.Player.characteristics)
            # print("---")
            # print()
            self.FightAlgorithm.actionHandle(action)

        # if action == "fightDeplacementFinished":
        #     print('### fight deplacement finished')
        #     print("---")
        #     print(self.monsters)
        #     print(self.Player.cellId)
        #     print(self.Player.characteristics)
        #     print("---")
        #     print()
        #     self.FightAlgorithm.actionHandle(action)
        
        # if action == "fightCastSpellFinished":
        #     print('### fight deplacement finished')
        #     print("---")
        #     print(self.monsters)
        #     print(self.Player.cellId)
        #     print(self.Player.characteristics)
        #     print("---")
        #     print()
        #     self.FightAlgorithm.actionHandle(action)
        
        elif action == "allActionsFinished" and self.isFighting == True:
            print('(((((((((((((((( ALL ACTIONS FINISHED. Monsters :', self.monsters)
            
            self.FightAlgorithm.actionHandle(action)

        
        

        self.updateGUI()



