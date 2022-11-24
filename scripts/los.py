import math

def getLine(x, y, targetX, targetY):
    line = []
    x = x + 0.5
    y = y + 0.5
    targetY = targetY + 0.5
    targetX = targetX + 0.5

    padX = 0
    padY = 0
    steps = 0
    cas = 0

    if abs(x - targetX) == abs(y - targetY):
        steps = abs(x - targetX)
        padX = 1 if targetX > x else -1
        padY = 1 if targetY > y else -1
        cas = 1

    elif abs(x - targetX) > abs(y - targetY):
        steps = abs(x - targetX)
        
        padX = 1 if targetX > x else -1
        padY = (targetY - y) /steps
        padY = padY * 100
        padY = math.ceil(padY) / 100
        cas = 2
    
    else:
        steps = abs(y - targetY)
        padX = (targetX - x) / steps
        padX = padX * 100
        padX = math.ceil(padX) / 100
        padY = 1 if (targetY > y) else -1
        cas = 3
    
    print(3 + (steps / 2))
    print(97 - (steps / 2))
    errorSup = ~~(int(3 + (steps / 2)))
    errorInf = ~~(int(97 - (steps / 2)))

    for i in range(0, int(steps - 1)):
        cellX = 0
        cellY = 0
        xPadX = x + padX
        yPadY = y + padY

        if cas == 2:
            beforeY = math.ceil(y * 100 + padY * 50) / 100
            afterY = math.floor(y *100 + padY * 150) / 100
            diffBeforeCenterY = math.floor(abs(math.floor(beforeY) * 100 - beforeY * 100)) / 100
            diffCenterAfterY  = math.ceil(abs(math.ceil(afterY) * 100 - afterY * 100)) / 100
            cellX = math.floor(xPadX)

            if math.floor(beforeY) == math.floor(afterY):
                cellY = math.floor(yPadY)
                if ((beforeY == cellY and afterY < cellY) or (afterY == cellY and beforeY < cellY)):
                    cellY = math.ceil(yPadY)
                
                line.append([cellX, cellY])
            elif (math.ceil(beforeY) == math.ceil(afterY)):
                cellY = math.ceil(yPadY)
                if ((beforeY == cellY and afterY < cellY) or (afterY == cellY and beforeY < cellY)):
                    cellY = math.floor(yPadY)
              
                line.append([cellX, cellY])
            elif (~~(int(diffBeforeCenterY * 100)) <= errorSup):
                #attention aux arrondis selon la distance du pt de départ
                line.append([cellX, math.floor(afterY)])
            elif (~~(int(diffCenterAfterY * 100)) >= errorInf):
                #attention aux arrondis selon la distance du pt de départ
                line.append([cellX, math.floor(beforeY) ])
            else:
                line.append([cellX, math.floor(beforeY) ])
                line.append([cellX, math.floor(afterY) ])
          
        elif (cas == 3):
            beforeX = math.ceil(x * 100 + padX * 50) / 100
            afterX  = math.floor(x * 100 + padX * 150) / 100
            diffBeforeCenterX = math.floor(abs(math.floor(beforeX) * 100 - beforeX * 100)) / 100
            diffCenterAfterX  = math.ceil(abs(math.ceil(afterX) * 100 - afterX * 100)) / 100

            cellY = math.floor(yPadY)

            if (math.floor(beforeX) == math.floor(afterX)):
                cellX = math.floor(xPadX)
                if ((beforeX == cellX and afterX < cellX) or (afterX == cellX and beforeX < cellX)):
                    cellX = math.ceil(xPadX)
                
                line.append([cellX, cellY])
            elif (math.ceil(beforeX) == math.ceil(afterX)):
                cellX = math.ceil(xPadX)
                if ((beforeX == cellX and afterX < cellX) or (afterX  == cellX and beforeX < cellX)):
                    cellX = math.floor(xPadX)
                
                line.append([cellX, cellY])
            elif (~~(int(diffBeforeCenterX * 100)) <= errorSup):
                #attention aux arrondis selon la distance du pt de départ
                line.append([math.floor(afterX), cellY])
            elif (~~(int(diffCenterAfterX * 100)) >= errorInf):
                #attention aux arrondis selon la distance du pt de départ
                line.append([math.floor(beforeX), cellY])
            else:
                line.append([math.floor(beforeX), cellY])
                line.append([math.floor(afterX), cellY])
          
        else:
            line.append([math.floor(xPadX), math.floor(yPadY)])
        
        x = (x * 100 + padX * 100) / 100
        y = (y * 100 + padY * 100) / 100
    
    for l in line:
        print(l)

getLine(0, 0, 2, 1)
