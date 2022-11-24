
from .Astar import Astar as Astar
from .Spell import Spell as Spell

import numpy as np
import math as Math


cellUnwalkable = [
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 1 ,1, 0, 0 ,0, 0],
  [0, 0 ,0, 1, 1 ,1, 0, 0 ,0, 0],
  [0, 0 ,0, 1, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0]]


cellWall = [
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 1 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 1, 1 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 1, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0]]

fromX = 5
fromY = 5

monsterX = 2
monsterY = 3

monsters = [[2, 3], [6, 3]]

path = Astar.search(cellUnwalkable, 1, [0, 0], [2, 2])


def getDistance(X1, Y1, X2, Y2):
    dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
    return int(dist)

def getMovementCells(player_pos, monster_pos, monsters, pm_left, cells_unwalkable):
    player_movement_zone = []
        
    x = player_pos[0]
    y = player_pos[1]

    movement_radius = pm_left

    top_movement_radius = x - movement_radius 
    bottom_movement_radius = x + movement_radius + 1
    left_movement_radius = y - movement_radius
    right_movement_radius = y + movement_radius  +1

    if(left_movement_radius < 0):
        while left_movement_radius < 0:
            left_movement_radius = left_movement_radius + 1

    if(right_movement_radius > len(cells_unwalkable)):
        while right_movement_radius > len(cells_unwalkable):
            right_movement_radius = right_movement_radius - 1

    if(bottom_movement_radius > len(cells_unwalkable[0])):
        while bottom_movement_radius > len(cells_unwalkable[0]):
            bottom_movement_radius = bottom_movement_radius - 1

    if(top_movement_radius < 0):
        while top_movement_radius < 0:
            top_movement_radius = top_movement_radius + 1

    player_mask = np.ogrid[top_movement_radius:bottom_movement_radius,left_movement_radius:right_movement_radius]

    player_movement_zone = []

    print(player_mask)

    for xx in player_mask[0]:
        arr = []
        for yy in player_mask[1][0]:
            try:
                arr.append(cells_unwalkable[xx[0]][yy])
            except:
                print("ERROR arr.append :", xx[0], yy)
                pass
        player_movement_zone.append(arr)

    player_start_x = top_movement_radius
    player_end_x = bottom_movement_radius
    player_start_y = left_movement_radius
    player_end_y = right_movement_radius

    finalCells = []

    for x in range (player_start_x, player_end_x):
        for y in range(player_start_y, player_end_y):
            mask_cell_x = x - player_start_x
            mask_cell_y = y - player_start_y
            
            if [x, y] not in monsters:
                diff = getDistance(player_pos[0], player_pos[1], x, y)
                if diff <= pm_left:
                    path = Astar.search(player_movement_zone, 1,  [player_pos[0] - player_start_x, player_pos[1] - player_start_y], [mask_cell_x, mask_cell_y])
                    if(path != None and path[mask_cell_x][mask_cell_y] <= pm_left):
                        finalCells.append([x, y])
    
    print("play mvmt zone")
    for a in player_movement_zone:
        print(a)
    
    if len(finalCells) == 0:
        return -1
    
    print("final cells :", finalCells)

    return finalCells




unwalkableList = []
for x in range(0, len(cellUnwalkable)):
    for y in range(0, len(cellUnwalkable[x])):
        if cellUnwalkable[x][y] == 1:
            unwalkableList.append([x, y])

wallList = []
for x in range(0, len(cellWall)):
    for y in range(0, len(cellWall[x])):
        if cellWall[x][y] == 1:
            wallList.append([x, y])


spell = {
  'align': True,
  'id': 1,
  'zone': [
    [-1,-1, -1, -1, 0, -1, -1, -1, -1],
    [-1,-1, -1, -1, 0, -1, -1, -1, -1],
    [-1,-1, -1, -1, 0, -1, -1, -1, -1],
    [-1,-1, -1, -1, 0, -1, -1, -1, -1],
    [-1,-1, -1, -1, 1, -1, -1, -1, -1],
    [-1,-1, -1, -1,-1, -1, -1, -1, -1],
    [-1,-1, -1, -1,-1, -1, -1, -1, -1],
    [-1,-1, -1, -1,-1, -1, -1, -1, -1],
    [-1,-1, -1, -1,-1, -1, -1, -1, -1],
  ],
#   'zone': [
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#     [-1,-1, -1, -1, -1, -1, -1, -1, -1],
#     [-1,-1, -1, -1, 0, -1, -1, -1, -1],
#     [-1,-1, -1, 0, 1, -1, -1, -1, -1],
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#     [-1,-1, -1, -1,-1, -1, -1, -1, -1],
#   ],
  'POmin': 1,
  'PO': 15
} 

fichier = open("test.txt", "a")

class Movement:

    def getMovementCells(fromPos, monsterPos, monsters, pmLeft, cellUnwalkable):
        return getMovementCells(fromPos, monsterPos, monsters, pmLeft, cellUnwalkable)

    def getMovementSpellCells(fromX, fromY, monsterX, monsterY, unwalkableList, wallList, spell, monsters, pmLeft, cellUnwalkable):

        print("GET MOUVEMENT SPELL CELLS")
        movementCells = getMovementCells([fromX, fromY], [monsterX, monsterY], monsters, pmLeft, cellUnwalkable)
        print("### movementCells :", movementCells)
        if movementCells == -1:
            return -1
        final = []

        for cell in movementCells:
            hits = Spell.getHitCells(cell[0], cell[1], monsterX, monsterY, unwalkableList, wallList, spell, monsters)#, mapWidth = 10, mapHeight = 10)
            #print(cell, hits)
            if hits != -1:
                final.append({
                    'movementCell': cell,
                    'hits': hits
                })
            # fichier.write("-- Déplacement: " + str(cell) +" ( " + str(len(hits)) + " hits)\n")
            # for hit in hits:
            #     fichier.write("- Hit: " + str(hit) + "\n")
            #     for x in range(0, len(cellWall)):
            #         for y in range(0, len(cellWall[x])):
            #             if [x, y] == hit:
            #                 fichier.write("H ")
            #             elif cellWall[x][y] == 1:
            #                 fichier.write("X ")
            #             elif [x, y] == [monsterX, monsterY]:
            #                 fichier.write("M ")
            #             elif [x, y] == [fromX, fromY]:
            #                 fichier.write("P ")
            #             elif [x, y] == cell:
            #                 fichier.write("D ")
            #             else:
            #                 fichier.write("- ")
                    
            #         fichier.write("\n")
            #     fichier.write("\n")
            # fichier.write("\n")

        if len(final) == 0:
            return -1
        return final

    def getMovementCellWithoutSpell(playerPos, monsterPos, monsters, pmLeft, unwalkable, monsterToHitX, monsterToHitY, AIType):
        
        distanceListFromMonster = {}
        cells = getMovementCells(playerPos, monsterPos, monsters, pmLeft, unwalkable)

        if cells == -1:
            return -1
        
        for cell in cells:
            distanceListFromMonster[getDistance(monsterToHitX, monsterToHitY, cell[0], cell[1])] = cell

        key = 0
        if AIType == 'close':
            key = min(list(distanceListFromMonster.keys()))
        
        if AIType == 'far':
            key = max(list(distanceListFromMonster.keys()))

        return distanceListFromMonster[key]
            
    def getStartPosition(fightStartPositions, monstersPos):
        distanceMinPos = []
        allKeys = []
        finalDistance = {}

        print("fightStartPositions :", fightStartPositions)
        print("monstersPos :", monstersPos)

        for start in fightStartPositions:
            distanceList = {}
            for monster in monstersPos:
                distanceList[int(getDistance(start[0], start[1], monster[0], monster[1]))] = monster
            key = min(list(distanceList.keys()))
            print("-- key:", key)
            pos = distanceList[int(key)]
            print("-- pos:", pos)
            finalDistance[key] = start
            print("-- pos:", pos)


        finalKey = max(list(finalDistance.keys()))
        print("finalKey :", finalKey)
        finalCell = finalDistance[int(finalKey)]

        print("final cel :", finalCell)
        return finalCell