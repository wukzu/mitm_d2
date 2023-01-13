class CellWithOrientation:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y
        self.Orientation = 0
        self.CompressedValue = 0
    
    def SetOrientation(self, next_cell: "CellWithOrientation"):
        if next_cell.x == self.x:
            if next_cell.y == self.y + 1:
                self.Orientation = 7
            elif next_cell.y == self.y - 1:
                self.Orientation = 3
        elif next_cell.y == self.y:
            if next_cell.x == self.x + 1:
                self.Orientation = 1
            elif next_cell.x == self.x - 1:
                self.Orientation = 5
        else:
            if next_cell.x == self.x + 1 and next_cell.y == self.y + 1:
                self.Orientation = 0
            elif next_cell.x == self.x + 1 and next_cell.y == self.y - 1:
                self.Orientation = 2
            elif next_cell.x == self.x - 1 and next_cell.y == self.y - 1:
                self.Orientation = 4
            elif next_cell.x == self.x - 1 and next_cell.y == self.y + 1:
                self.Orientation = 6
    
    def SetOrientationInt(self, orientation: int):
        self.Orientation = orientation
    
    def GetCompressedValue(self):
        self.CompressedValue = (self.Orientation & 7) << 12 | self.id & 4095
