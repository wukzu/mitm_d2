
import math as Math






def rotate_90_degree_clckwise(matrix, times = 1):
  new_matrix = []
  for i in range(0, times):
    print(i, " fois")
    ma = []
    if i == 0:
      ma = matrix
    else: 
      ma = new_matrix.copy()
      new_matrix = []
    for i in range(len(ma[0])):
      li = list(map(lambda x: x[i], ma))
      li.reverse()
      new_matrix.append(li)
  
  return new_matrix

def getDistance(X1, Y1, X2, Y2):
    dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
    return int(dist)


def getHitCells(fromX, fromY, targetX, targetY, cellUnwalkable, cellWall, spell):
  spellZone = spell.get("zone")
  spellXLen = len(spellZone)
  spellYLen = len(spellZone[0])

  print("spellXLen ", spellXLen)
  print("spellYLen ", spellYLen)

  hitPoint = [0, 0]
  for x in range(0, len(spellZone)):
    for y in range(0, len(spellZone[x])):
      if spellZone[x][y] == 1:
        hitPoint = [x, y]
        break

  print(hitPoint)

  spellX = 0
  spellY = 0
  hittingCells = []
  for x in range(targetX - (spellXLen - hitPoint[0]) + 1, targetX +  hitPoint[0] + 1):
    for y in range(targetY - (spellYLen - hitPoint[1]) + 1, targetY +  hitPoint[1] + 1):

      # Check si le point est bien dans le tableau 
      if x >= 0 and y >= 0 and x < len(cellWall) and y < len(cellWall[x]):
        print("-- :", x, y, ", ", spellX, spellY, len(cellWall), len(cellWall[x]))

        # Si n'est pas un mur, une cell non walkable:
        if spellZone[spellX][spellY] != -1  and cellUnwalkable[x][y] != 1 and cellWall[x][y] != 1:
          hittingCells.append([x, y])
        spellY = spellY + 1

    spellX = spellX + 1
    spellY = 0
  
  for a in hittingCells:
    print(a)
  
# gérer l'alignement et la rotation de la zone du sort
# gérer la po min/max
# ajouter les mosntres comme cell unwalkable / wall
# gérer free zone ou pas
# ne pas se taper (quand énemi est pret)


spell = {
  'zone': [
    [-1, 0, -1],
    [0, 1, 0],
    [-1, 0, -1]
  ]
} 

cellUnwalkable = [
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,1, 1, 0 ,0, 0],
  [0, 0 ,0, 0, 1 ,1, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0]]


cellWall = [
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,1, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0],
  [0, 0 ,0, 0, 0 ,0, 0, 0 ,0, 0]]


fromX = 2
fromY = 0

targetX = 9
targetY = 9



getHitCells(fromX, fromY, targetX, targetY, cellUnwalkable, cellWall, spell)


  

print("rotated :")
#print(rotate_90_degree_clckwise(spellZone, 3))

print("dist :", getDistance(0, 0, 1, 4))