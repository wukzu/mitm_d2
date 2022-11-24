#from FightAlgorithm import FightAlgorithm
import math as Math

fightStartPositions = [[1, 1], [1, 3], [1, 6]]

monstersPos = [[3, 1], [3, 4]]


# test:

# -  -  -  -  -  -  -  
# -  C  -  C  -  C  -  
# -  -  -  -  -  -  -  
# -  M  -  -  M  -  -  
# -  -  -  -  -  -  -  
# -  -  -  -  -  -  -  



def getDistance(X1, Y1, X2, Y2):
    dist = Math.fabs(X2 - X1) + Math.fabs(Y2 - Y1)
    return int(dist)

distanceMinPos = []

allKeys = []

finalDistance = {}

for start in fightStartPositions:
    distanceList = {}
    for monster in monstersPos:
        distanceList[int(getDistance(start[0], start[1], monster[0], monster[1]))] = monster
    key = min(list(distanceList.keys()))
    pos = distanceList[int(key)]
    print("start:", start, ", ", distanceList)
    print("pos :", pos, key)
    finalDistance[key] = start


finalKey = max(list(finalDistance.keys()))
finalCell = finalDistance[int(finalKey)]

print("---")
print(finalCell)
print('---')
print('---')





    



