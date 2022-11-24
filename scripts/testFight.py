wallCells = [
  ['-','-','1','-','-','-','-'],
  ['-','-','1','-','-','-','-'],
  ['-','-','1','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','-','-','-','-','-']
]

from pandas import *
import numpy as np

playerPos = [1, 0]
monsterPos = [3, 3]




def remove_np_duplicates(data):
  # Perform lex sort and get sorted data
  sorted_idx = np.lexsort(data.T)
  sorted_data =  data[sorted_idx,:]

  # Get unique row mask
  row_mask = np.append([True],np.any(np.diff(sorted_data,axis=0),1))

  # Get unique rows
  out = sorted_data[row_mask]
  return out

def get_grid_cells_btw(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  dx = x2-x1 
  dy = y2-y1

  if dx == 0: # will divide by dx later, this will cause err. Catch this case up here
    step = np.sign(dy)
    ys = np.arange(0,dy+step,step)
    xs = np.repeat(x1, ys.shape[0])
  else:
    m = dy/(dx+0.0)
    b = y1 - m * x1 

    step = 1.0/(max(abs(dx),abs(dy))) 
    xs = np.arange(x1, x2, step * np.sign(x2-x1))
    ys = xs * m + b

  xs = np.rint(xs)
  ys = np.rint(ys)
  pts = np.column_stack((xs,ys))
  pts = remove_np_duplicates(pts)

  return pts.astype(int)


def checkLineOfSight(playerPos, targetPos, nonLosCells):
  print('start')
  cells = get_grid_cells_btw(tuple(playerPos),tuple(targetPos))
  cells = cells.tolist()
  print(type(cells))
  print(cells)
  # grid = [['.' for row in range(11)] for col in range(11)]
  # for pt in cells:
  #   print(pt)
  #   #if playerPos != pt and targetPos != pt:
  #    # print(pt)
  #     # if nonLosCells[pt[0]][pt[1]] == '1':
  #     #   return False
  #     #   break
  #   x,y=pt
  
  return True



result = checkLineOfSight([0, 0], [1,2], [
  ['-','-','1','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','1','-','-','-','-'],
  ['-','1','-','-','-','-','-'],
  ['-','1','-','-','-','-','-'],
  ['-','1','-','-','-','-','-'],
  ['-','-','-','-','-','-','-'],
  ['-','-','-','-','-','-','-']
])

print("result :", result)
print("---------------")

from bresenham import bresenham

print(list(bresenham(0, 0, 2, 6)))


def test(start, end):
  pente = end[0] / end[1]
  cells = []
  print(pente)
  for y in range(0, end[0] + 1):
    for x in range(0, end[1] + 1):
      result = (x + 1) * pente
      if (result + y) < y + 1:
        cells.append([x, y])

  print(cells)



test([0,0], [2,5])



grid = [[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]]
#start, goal = (0,0),(4,3)
start, goal = (0,0),(1,3)

def los(start, goal):
    x0, y0 = start
    x1, y1 = goal

    dy = y1 - y0
    dx = x1 - x0

    if dy < 0:
        dy = -dy
        sy = -1
    else:
        sy = 1

    if dx < 0:
        dx = -dx
        sx = -1
    else:
        sx = 1

    f = 0
    result = []

    if dx >= dy:
        while x0 != x1:
            f = f + dy

            if f >= dx:
                result.append((x0+(sx-1)/2, y0+(sy-1)/2))
                y0 = y0 + sy
                f = f - dx
            if f != 0:
                result.append((x0+(sx-1)/2, y0+(sy-1)/2))
            if dy == 0:
                a = (x0+(sx-1)/2, y0)
                b = (x0+(sx-1)/2, y0-1)
                result.extend((a, b))
            x0 = x0 + sx
    else:
        while y0 != y1:
            f = f + dx

            if f >= dy:
                result.append((x0+(sx-1)/2, y0+(sy-1)/2))
                x0 = x0 + sx
                f = f - dy
            if f != 0:
                result.append((x0+(sx-1)/2, y0+(sy-1)/2))
            if dx == 0:
                a = (x0, y0+(sy-1)/2)
                b = (x0-1, y0+(sy-1)/2)
                result.extend((a, b))

            y0 = y0 + sy
    return result


check = los(start,goal)
print(check)

