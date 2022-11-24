#from FightAlgorithm import FightAlgorithm
import math as Math

from Astar import Astar as Astar
from Movement import Movement as Movement

# import sys
# sys.path.append('/.../Game')
# from Fight import Fight

# fight = Fight()
# player = Player()

class Fight:
    def __init__(self, Player, Map):
        self.isFighting = True

        self.monsters = [1,2,3]
        self.walkableCells = []

        self.Player = Player
        self.Map = Map

        self.FightAlgorithm = FightAlgorithm(Map, Player, self)

    def socketHandle(self, action, data):
        if action == 'fightStarted':
            self.FightAlgorithm.actionHandle()



class Player:
    def __init__(self):
        self.cellId = 200
        self.spells = [
            {
                'id': 1,
                'PO': 3,
                'POmin': 1,
                'PA': 3,
                'line': True,
                'circle': False,
                'freeZone': True,
                'zone': [[0, 1, 0]]
            },
            {
                'id': 2,
                'PO': 5,
                'POmin': 3,
                'PA': 4,
                'line': False,
                'circle': True,
                'freeZone': False,
                'zone': [
                    [-1, -1,  0, -1, -1], 
                    [-1,  0,  0,  0, -1],
                    [ 0,  0,  1,  0,  0],
                    [-1,  0,  0,  0, -1],
                    [-1, -1,  0, -1, -1],
                ]
            }
        ]

    def move(self, cellId):
        self.cellId = cellId

class Map: 
    def __init__(self):
        self.fightStartCells = [200, 204],
        self.walkableCells = [204, 2345]
    
    def changeMap(self):
        self.walkableCells = [111, 222]




# player = Player()
# mmap = Map()
# fight = Fight(player, mmap)

# fight.socketHandle('fightStarted', 'aaa')

# player.move(289)

# fight.socketHandle('fightStarted', 'aaa')

playerPosX = 24
playerPosY = 10

distanceList = {}
monstersPos = [[6, 21], [7, 21], [11, 22], [12, 20], [12, 22], [13, 22], [21, 7], [23, 7]]

def getDistance(X1, Y1, X2, Y2):
    dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
    return int(dist)

for monster in monstersPos:
    distanceList[int(getDistance(playerPosX, playerPosY, monster[0], monster[1]))] = monster 
    
print("distanceListdistanceList :", distanceList)
print("keys :", list(distanceList.keys()))

key = min(list(distanceList.keys()))

monsterToHitX = distanceList[int(key)][0]
monsterToHitY = distanceList[int(key)][1]

print("monsterToHitX:", monsterToHitX, "monsterToHitY:",monsterToHitY)


playerPos = [10, 10]

deplacementList = {}
possibleDeplacements = [{'movementCell': [14,13], 'hits': [{'spellId': 13065, 'coords': [18, 12]}]}, {'movementCell': [14, 13], 'hits': [{'spellId': 13065, 'coords': [18, 12]}]}]

for d in possibleDeplacements:
    deplacementList[int(getDistance(playerPos[0], playerPos[1], d['movementCell'][0], d['movementCell'][1]))] = d['movementCell'] 

key = min(list(deplacementList.keys()))

print(deplacementList[int(key)])

unwalkable = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

playerPos = [3, 3]
monsterPos = [6, 3]
monstersPos = [monsterPos, [6, 1]]
distanceList = {}

cells = Movement.getMovementCells(playerPos, monsterPos, [monsterPos], 4, unwalkable)

for monster in monstersPos:
    distanceList[int(getDistance(playerPos[0], playerPos[1], monsterPos[0], monsterPos[1]))] = monster 

    # print('--- distance list :', distanceList)
        
key = min(list(distanceList.keys()))
monsterToHitX = distanceList[int(key)][0]
monsterToHitY = distanceList[int(key)][1]

print(monsterToHitX, monsterToHitY)

distanceListFromMonster = {}

for cell in cells:
    distanceListFromMonster[getDistance(monsterToHitX, monsterToHitY, cell[0], cell[1])] = cell

key = max(list(distanceListFromMonster.keys()))

print("distanceListFromMonster :", distanceListFromMonster)
print("final :", distanceListFromMonster[key])



print(cells)

#fightAlgorithm = FightAlgorithm(mmap, player, fight)