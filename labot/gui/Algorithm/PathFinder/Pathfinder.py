import json
import time
import math
import cmath
# from .Cell import Cell
# from .CellWithOrientation import CellWithOrientation

from .Cell import Cell
from .CellWithOrientation import CellWithOrientation

class PathingUtils:
    MapHeight = 20
    MapWidth = 14
    MapCellsCount = 560
    cellsPositions = [(0,0) for _ in range(MapCellsCount)]

    @staticmethod
    def CoordToCellId(cellX: int, cellY: int) -> int:
        return (cellX - cellY) * PathingUtils.MapWidth + cellY + (cellX - cellY) // 2

    @staticmethod
    def CellIdToCoord(cellId: int) -> tuple:
        if cellId < 0 or cellId >= len(PathingUtils.cellsPositions):
            raise ValueError("Invalid cell id")
        return PathingUtils.cellsPositions[cellId]

    @staticmethod
    def GetCompressedPath(path):
        compressedPath = []
        if len(path) < 2:
            for node in path:
                node.GetCompressedValue()
                compressedPath.append(node.CompressedValue)
        else:
            for i in range(len(path) - 1):
                path[i].SetOrientation(path[i + 1])
            path[-1].SetOrientationInt(path[-2].Orientation)
            for cell in path:
                cell.GetCompressedValue()
            compressedPath.append(path[0].CompressedValue)
            for i in range(1, len(path) - 1):
                if path[i].Orientation != path[i - 1].Orientation:
                    compressedPath.append(path[i].CompressedValue)
            compressedPath.append(path[-1].CompressedValue)
        return compressedPath

    @staticmethod
    def DistanceToPoint(point1: tuple, point2: tuple) -> float:
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

class Pathfinder:
    def __init__(self):
        self.useDiagonals = False
        self.find = False
        self.destinationCell = None
        self.startCell = None
        self.currentMap = None
        self.matrix = {}
        self.openList = []
        self.MapWidth = 20
        self.MapHeight = 14

    @property
    def LoadedMapId(self):
        if self.currentMap:
            return self.currentMap.Data.Id
        return 0

    def SetMap(self, mapp, useDiagonal):
        self.currentMap = mapp
        self.useDiagonals = useDiagonal
        self.matrix.clear()
        self.openList.clear()
        self.find = False
        cell = None
        id = 0
        loc1 = 0
        loc2 = 0
        loc3 = 0
        for line in range(20):
            for column in range(14):
                cell = self.currentMap['cells'][id]
                #if mapp.IsEntityOnCell(id):
                #    #cell.Mov = False
                self.matrix[id] = Cell(cell['mapChangeData'] != 0, cell['mov'], True, column, loc3, id, (loc1 + column, loc2 + column))
                id += 1
            loc1 += 1
            loc3 += 1
            for column in range(14):
                cell = self.currentMap['cells'][id]
                #if mapp.IsEntityOnCell(id):
                #    cell.Mov = False
                self.matrix[id] = Cell(cell['mapChangeData'] != 0, cell['mov'], True, column, loc3, id, (loc1 + column, loc2 + column))
                id += 1
            loc3 += 1
            loc2 -= 1

    def GetCompressedPath(self, startCellId: int, destinationCellId: int):
        return PathingUtils.GetCompressedPath(self.Find(startCellId, destinationCellId))
    
    def GetPath(self, startCellId: int, destinationCellId: int):
        return self.Find(startCellId, destinationCellId)

    def Find(self, startCellId: int, destinationCellId: int):
        self.startCell = self.matrix[startCellId]
        self.destinationCell = self.matrix[destinationCellId]

        self.matrix[startCellId].Start = True
        self.matrix[startCellId].InClosedList = True

        self.matrix[destinationCellId].End = True
        self.destinationCell = self.matrix[destinationCellId]
        for cell in self.matrix.values():
            cell.SetH(self.matrix[destinationCellId])

        currentCell = self.matrix[startCellId]

        startTime = int(time.time())

        while not self.find:
            self.FindAvalableCell(currentCell)

            if not self.find:
                if len(self.openList) == 0:
                    print("CLOSED LIST")
                    return None

                currentCell = self.openList[0]
                currentCell.InClosedList = True
                currentCell.InOpenList = False
                self.openList.pop(0)
            if int(time.time() - startTime) > 500:
                return None

        cells = []
        currentCell = self.matrix[destinationCellId]

        while currentCell.Parent != None:
            cells.insert(0, CellWithOrientation(currentCell.Id, currentCell.Location[0], currentCell.Location[1]))
            currentCell = currentCell.Parent
        cells.insert(0, CellWithOrientation(startCellId, self.matrix[startCellId].Location[0], self.matrix[startCellId].Location[1]))
        return cells


    def FindAvalableCell(self, cell):
        avalable_cell = None
        if cell.Position[0] == 0 and cell.Position[6] == 0:
            if cell.Pair:
                avalable_cell = self.matrix[cell.Id - 14]
            else:
                avalable_cell = self.matrix[cell.Id - 13]
            if avalable_cell.End:
                avalable_cell.Parent = cell
                self.find = True
                return
            if avalable_cell.Walkable:
                if not avalable_cell.InOpenList and not avalable_cell.InClosedList:
                    avalable_cell.Parent = cell
                    avalable_cell.InOpenList = True
                    self.openList.append(avalable_cell)
                    self.FixeCell(avalable_cell, cell)
        if cell.Position[2] == 0 and cell.Position[6] == 0:
            if cell.Pair:
                avalable_cell = self.matrix[cell.Id + 14]
            else:
                avalable_cell = self.matrix[cell.Id + 15]
            if avalable_cell.End:
                avalable_cell.Parent = cell
                self.find = True
                return
            if avalable_cell.Walkable:
                if not avalable_cell.InOpenList and not avalable_cell.InClosedList:
                    avalable_cell.Parent = cell
                    avalable_cell.InOpenList = True
                    self.openList.append(avalable_cell)
                    self.FixeCell(avalable_cell, cell)
        if cell.Position[0] == 0 and cell.Position[4] == 0:
            if cell.Pair:
                avalable_cell = self.matrix[cell.Id - 15]
            else:
                avalable_cell = self.matrix[cell.Id - 14]
            if avalable_cell.End:
                avalable_cell.Parent = cell
                self.find = True
                return
            if avalable_cell.Walkable:
                if not avalable_cell.InOpenList and not avalable_cell.InClosedList:
                    avalable_cell.Parent = cell
                    avalable_cell.InOpenList = True
                    self.openList.append(avalable_cell)
                    self.FixeCell(avalable_cell, cell)
        if cell.Position[2] == 0 and cell.Position[4] == 0:
            if cell.Pair:
                avalable_cell = self.matrix[cell.Id + 13]
            else:
                avalable_cell = self.matrix[cell.Id + 14]
            if avalable_cell.End:
                avalable_cell.Parent = cell
                self.find = True
                return
            if avalable_cell.Walkable:
                if not avalable_cell.InOpenList and not avalable_cell.InClosedList:
                    avalable_cell.Parent = cell
                    avalable_cell.InOpenList = True
                    self.openList.append(avalable_cell)
                    self.FixeCell(avalable_cell, cell)
            
        # Droite
        if cell.Position[6] == 0 and cell.Position[7] == 0 and self.useDiagonals:
            avalableCell = self.matrix[cell.Id + 1]
            if avalableCell.End:
                avalableCell.Parent = cell
                find = True
                return
            if avalableCell.Walkable:
                if not avalableCell.InOpenList and not avalableCell.InClosedList:
                    avalableCell.Parent = cell
                    avalableCell.InOpenList = True
                    self.openList.append(avalableCell)
                    self.FixeCell(avalableCell, cell)

        # Gauche
        if cell.Position[4] == 0 and cell.Position[5] == 0 and self.useDiagonals:
            avalableCell = self.matrix[cell.Id - 1]
            if avalableCell.End:
                avalableCell.Parent = cell
                find = True
                return
            if avalableCell.Walkable:
                if not avalableCell.InOpenList and not avalableCell.InClosedList:
                    avalableCell.Parent = cell
                    avalableCell.InOpenList = True
                    self.openList.append(avalableCell)
                    self.FixeCell(avalableCell, cell)

        # Haut
        if cell.Position[0] == 0 and cell.Position[1] == 0 and self.useDiagonals:
            avalableCell = self.matrix[cell.Id - 28]
            if avalableCell.End:
                avalableCell.Parent = cell
                find = True
                return
            if avalableCell.Walkable:
                if not avalableCell.InOpenList and not avalableCell.InClosedList:
                    avalableCell.Parent = cell
                    avalableCell.InOpenList = True
                    self.openList.append(avalableCell)
                    self.FixeCell(avalableCell, cell)

        # Bas
        if cell.Position[2] == 0 and cell.Position[3] == 0 and self.useDiagonals:
            avalableCell = self.matrix[cell.Id + 28]
            if avalableCell.End:
                avalableCell.Parent = cell
                find = True
                return
            if avalableCell.Walkable:
                if not avalableCell.InOpenList and not avalableCell.InClosedList:
                    avalableCell.Parent = cell
                    avalableCell.InOpenList = True
                    self.openList.append(avalableCell)
                    self.FixeCell(avalableCell, cell)

        self.SortOpenList()

    
    def SortOpenList(self):
        ok = False
        while not ok:
            ok = True
            temp = None
            for i in range(len(self.openList) - 1):
                if self.openList[i].F > self.openList[i + 1].F and PathingUtils.DistanceToPoint(self.openList[i].Location, self.destinationCell.Location) < PathingUtils.DistanceToPoint(self.openList[i + 1].Location, self.destinationCell.Location):
                    temp = self.openList[i]
                    self.openList[i] = self.openList[i + 1]
                    self.openList[i + 1] = temp
                    ok = False

    def FixeCell(self, cellInspected, currentCell):
        MovementCost = self.GetFixedMouvementCost(cellInspected, currentCell)
        cellInspected.G = int(MovementCost)
        cellInspected.H = int(self.GetFixedHeuristic(cellInspected, currentCell).real)
        cellInspected.F = cellInspected.G + cellInspected.H

    def GetFixedMouvementCost(self, cellInspected, currentCell):
        poid = self.PointWeight(cellInspected.Location)
        return cellInspected.G + (10 if cellInspected.Location[1] == currentCell.Location[1] or cellInspected.Location[0] == currentCell.Location[0] else 15) * poid

    def GetFixedHeuristic(self, cellInspected, currentCell):
        _loc8_ = cellInspected.Location[0] + cellInspected.Location[1] == self.destinationCell.Location[0] + self.destinationCell.Location[1]
        _loc9_ = cellInspected.Location[0] + cellInspected.Location[1] == self.startCell.Location[0] + self.startCell.Location[1]
        _loc10_ = cellInspected.Location[0] - cellInspected.Location[1] == self.destinationCell.Location[0] - self.destinationCell.Location[1]
        _loc11_ = cellInspected.Location[0] - cellInspected.Location[1] == self.startCell.Location[0] - self.startCell.Location[1]

        Heuristic = 10 * cmath.sqrt((self.destinationCell.Location[0] - cellInspected.Location[0]) * (self.destinationCell.Location[1] - cellInspected.Location[1]) + (self.destinationCell.Location[0] - cellInspected.Location[0]) * (self.destinationCell.Location[0] - cellInspected.Location[0]))

        if cellInspected.Location[0] == self.destinationCell.Location[0] or cellInspected.Location[1] == self.destinationCell.Location[1]:
            Heuristic = Heuristic - 3
        if (_loc8_) or (_loc10_) or cellInspected.Location[0] + cellInspected.Location[1] == currentCell.Location[0] + currentCell.Location[1] or cellInspected.Location[0] - cellInspected.Location[1] == currentCell.Location[0] - currentCell.Location[1]:
            Heuristic = Heuristic - 2
        if cellInspected.Location[0] == self.startCell.Location[0] or cellInspected.Location[1] == self.startCell.Location[1]:
            Heuristic = Heuristic - 3
        if (_loc9_) or (_loc11_):
            Heuristic = Heuristic - 2
        return Heuristic

    def PointWeight(self, point):
        result = 1
        cellId = PathingUtils.CoordToCellId(point[0], point[1])
        speed = self.currentMap['cells'][cellId]['speed']
        if speed >= 0:
            result = result + (5 - speed)
        else:
            result = result + (11 + abs(speed))
        return result
    






 

def openJsonMap(mapId):
    i = 0
    dp = 0
    while dp < 6:
        while i < 10:
            try:
                file = open("C:/Users/33630/Desktop/mitm/mitm_d2/sources/data/maps/maps" + str(dp) + ".d2p/" + str(i) + "/" + str(mapId) + ".json")
                data = json.load(file)
                return data
                break
            except IOError:
                pass
            i = i + 1
        dp = dp + 1
        i = 0

  


# result = openJsonMap(88084750)
# a = Pathfinder()
# a.SetMap(result, True)

# path = a.GetPath(412, 235)
# compressed = a.GetCompressedPath(412, 235)
# print(compressed)

# for p in path:
# 	print(p.x, p.y)
# 	for m in a.matrix:
# 		location = a.matrix[m].Location
# 		if location[0] == p.x and location[1] == p.y:
# 			print(a.matrix[m])
