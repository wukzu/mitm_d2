
from ..utils.Constants import Constants as Constants
from .Spell import Spell as Spell
from .Movement import Movement as Movement

import random

import math as Math

class FightAlgorithm:
    def __init__(self, Map, Player, Fight):
        self.Map = Map
        self.Player = Player
        self.Fight = Fight

        self.count = 0

        print(Constants.hellomsg)

        # Player : cellId
        # Player : characteristics
        # Player : spells

        # map : nonWalkableCells
        # map : nonLosCells

        # Fight : mosnters [
        #     {
        #        'id': -1,
        #        'cellId': 250
        #     }  
        # ]

    def getDistance(self, X1, Y1, X2, Y2):
        dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
        return int(dist)

    def countSpellsCasted(self, spellId):
        count = 0
        for spell in self.Fight.spellsCasted:
            if spellId == spell:
                count = count + 1
        
        return count
    
    def countSpellsCastedMonster(self, spellId, monsterId):
        count = 0

        for spell in self.Fight.spellsCastedMonsters:
            if spell['monsterId'] == monsterId and spell['spellId'] == spellId:
                count = count + 1
        
        return count
    

    def setDatas(self):
        print(Map.fightStartCells)
        print(Player.cellId)
        print(Fight.monsters)

    def findStartPosition(self):
        monstersPos = []
        monstersCells = []

        fightStartPos = []
        
        for m in self.Fight.monsters: 
            monstersCells.append(m['cellId'])

        for x in range(0, len(Constants.cells_game)):
            for y in range(0, len(Constants.cells_game[x])):
                if Constants.cells_game[x][y] != -1:
                    if Constants.cells_game[x][y] in monstersCells:
                        monstersPos.append([x, y])
                    if Constants.cells_game[x][y] in self.Map.fightStartCells:
                        fightStartPos.append([x, y])


        cell = Movement.getStartPosition(fightStartPos, monstersPos)
        timeToWait = random.randint(300, 1500)
        
        self.Fight.waitTime(timeToWait)
        self.Player.moveToCellId(Constants.cells_game[cell[0]][cell[1]])
        
        timeToWait = random.randint(0, 500)
        print("[FightAlgorithm] Attendre ", timeToWait)
        self.Fight.waitTime(timeToWait)
        self.Fight.setFightReady()

    def actionHandle(self, action):

        timeToWait = random.randint(300, 1000)
        self.Fight.waitTime(timeToWait)
        self.count = self.count + 1

        playerPosX = 0
        playerPosY = 0
        playerFound = False

        monstersPos = []
        monstersCells = []
        monstersPositions = []

        for m in self.Fight.monsters: 
            monstersCells.append(m['cellId'])

        for x in range(0, len(Constants.cells_game)):
            for y in range(0, len(Constants.cells_game[x])):
                if Constants.cells_game[x][y] != -1:
                    if self.Player.cellId == Constants.cells_game[x][y] and playerFound == False:
                        playerPosX = x
                        playerPosY = y 
                        playerFound = True
                    if Constants.cells_game[x][y] in monstersCells:
                        monstersPos.append([x, y])
        
        monsterToHitX = 0
        monsterToHitY = 0

        distanceList = {}
        
        for monster in monstersPos:
            distanceList[int(self.getDistance(playerPosX, playerPosY, monster[0], monster[1]))] = monster 

        
        key = min(list(distanceList.keys()))
        monsterToHitX = distanceList[int(key)][0]
        monsterToHitY = distanceList[int(key)][1]
        

        # ------------------------
        # ------------------------
        # ------------------------
        # check sans bouger

        unwalkableCellList = []
        wallCellList = []


        ##############################################################################""
        ##############################################################################""
        ##############################################################################""
        #
        for spell in self.Player.spells:
            print("checking spell without deplacement ", spell['id'], spell['name'])
            if self.countSpellsCasted(spell['id']) < spell['maxPerTurn']:
                
                # print("/ --- spell :", spell['id'], " PA : ", spell['PA'], " | player PA :", self.Player.characteristics['PA'] )
                # print("/ --- player pos :", playerPosX, playerPosY, " | monsterToHit :", monsterToHitX, monsterToHitY )
                # print("/ --- monstersCells :", monstersCells)
                if self.Player.characteristics['PA'] >= spell['PA']:
                    spellsToCast = Spell.getHitCells(playerPosX, playerPosY, monsterToHitX, monsterToHitY, self.Map.nonWalkableCellList, self.Map.wallCellList, spell, monstersPos)
                    if spellsToCast != -1:
                        
                        spellToCast = spellsToCast[0]
                        cellId = Constants.cells_game[spellToCast['coords'][0]][spellToCast['coords'][1]]
                        spellId = spellToCast['spellId']

                        monsterId = self.Fight.getMonsterIdFromCellId(cellId)

                        if self.countSpellsCastedMonster(spellId, monsterId) >= spell['maxPerTarget']:
                            print("nombre maximum par target attenint pour ce spell")
                            pass
                        else:
                            print("///// spell to cast :", spellId, cellId)
                            self.Fight.useSpell(spellId, cellId)
                            return
                    else:
                        print("aucun spell a utiliser")
                else:
                    print("pas assez de PA")
            else:
                print("Nombre max par tour atteint pour ce spell")
        #
        ##############################################################################""
        ##############################################################################""
        ##############################################################################""



        for spell in self.Player.spells:
            print("checking spell with deplacement ", spell['id'], spell['name'])
            if self.Player.characteristics['PA'] >= spell['PA'] and self.Player.characteristics['PM'] > 0:
                #On regarde si un déplacement est possible pour pouvoir lancer un sors
                deplacements = Movement.getMovementSpellCells(playerPosX, playerPosY, monsterToHitX, monsterToHitY, self.Map.nonWalkableCellList, self.Map.wallCellList, spell, monstersPos, self.Player.characteristics['PM'], self.Map.nonWalkableCells)
                
                if deplacements != -1:
                    print("deplacement -1")

                    possibleDeplacements = []
                    for deplacement in deplacements:
                        movementCell = deplacement['movementCell']
                        if movementCell in self.Map.nonWalkableCellList or movementCell in self.Map.wallCellList:
                            pass
                        hits = deplacement['hits']

                        possibleHits = []


                        for hit in hits:
                            spellId = hit['spellId']
                            coords = hit['coords']
                            cellId = Constants.cells_game[coords[0]][coords[1]]
                            monsterId = self.Fight.getMonsterIdFromCellId(cellId)

                            if self.countSpellsCasted(spell['id']) >= spell['maxPerTurn']:
                                print("Nombre max par tour atteint pour ce spell ", spellId)

                            elif self.countSpellsCastedMonster(spellId, monsterId) >= spell['maxPerTarget']:
                                print("Nombre max par target atteint pour ce spell ", spellId)

                            else:
                                possibleHits.append(hit)
                        
                        if len(possibleHits) != 0:
                            possibleDeplacements.append({
                                'movementCell': movementCell,
                                'hits': possibleHits
                            })
                    
                    if len(possibleDeplacements) != 0:

                        deplacementList = {}
                        
                        for d in possibleDeplacements:
                            deplacementList[int(self.getDistance(playerPosX, playerPosY, d['movementCell'][0], d['movementCell'][1]))] = d['movementCell'] 

                        key = min(list(deplacementList.keys()))

                        closerDeplacement = deplacementList[int(key)]

                        print("DEPLACEMENT TO :", closerDeplacement)
                        movementCellId = Constants.cells_game[closerDeplacement[0]][closerDeplacement[1]]
                        self.Player.moveToCellId(movementCellId)
                        return
                    else:
                        print("pas de deplacement possible")
                    

                    # print("movementCell :", movementCell)
                    # print("hit :", hit)

                    # movementCellId = Constants.cells_game[movementCell[0]][movementCell[1]]
                    # print("bouger en ", movementCellId)
                    # self.Player.moveToCellId(movementCellId)
                
                # if deplacements != -1:
                #     return moveToCellId(cellId)
                # else:
                #     print("////// ON NE PLUS BOUGER !")
                    # ON SE DEPLACE A LA CELL ID QUI SERA ACCESSIBLE AVEC LE SORT
                    
        
        # # Impossible de lancer un sort, même en bougeant
        if self.Player.characteristics['PM'] > 0:
        #     # Plus de PA mais encore des PM disponible,
            # ON s'enfuit ou on se rapproche en fonction de l'IA choisie
            # playerPos, monsterPos, [monsterPos], pmLeft, unwalkable, monsterToHitX, monsterToHitY
            if len(self.Fight.spellsCasted) > 0:
                cell = Movement.getMovementCellWithoutSpell([playerPosX, playerPosY], [monsterToHitX, monsterToHitY], monstersPos, int(self.Player.characteristics['PM']), self.Map.nonWalkableCells, monsterToHitX, monsterToHitY, 'far')
                if cell != -1 and cell[0] != playerPosX and cell[1] != playerPosY:
                    movementCellId = Constants.cells_game[cell[0]][cell[1]]
                    self.Player.moveToCellId(movementCellId)
                    return
            if len(self.Fight.spellsCasted) == 0:
                cell = Movement.getMovementCellWithoutSpell([playerPosX, playerPosY], [monsterToHitX, monsterToHitY], monstersPos, int(self.Player.characteristics['PM']), self.Map.nonWalkableCells, monsterToHitX, monsterToHitY, 'close')
                if cell != -1 and cell[0] != playerPosX and cell[1] != playerPosY:
                    movementCellId = Constants.cells_game[cell[0]][cell[1]]
                    self.Player.moveToCellId(movementCellId)
                    return
        
        self.Fight.passTurn()
        return 
        

        # else:
        #     return passTurn()
            


            
        


