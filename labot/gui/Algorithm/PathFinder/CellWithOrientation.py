class CellWithOrientation:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y
        self.orientation = 0
        self.compressed_value = 0
    
    def set_orientation(self, next_cell: "CellWithOrientation"):
        if next_cell.x == self.x:
            if next_cell.y == self.y + 1:
                self.orientation = 7
            elif next_cell.y == self.y - 1:
                self.orientation = 3
        elif next_cell.y == self.y:
            if next_cell.x == self.x + 1:
                self.orientation = 1
            elif next_cell.x == self.x - 1:
                self.orientation = 5
        else:
            if next_cell.x == self.x + 1 and next_cell.y == self.y + 1:
                self.orientation = 0
            elif next_cell.x == self.x + 1 and next_cell.y == self.y - 1:
                self.orientation = 2
            elif next_cell.x == self.x - 1 and next_cell.y == self.y - 1:
                self.orientation = 4
            elif next_cell.x == self.x - 1 and next_cell.y == self.y + 1:
                self.orientation = 6
    
    def set_orientation(self, orientation: int):
        self.orientation = orientation
    
    def get_compressed_value(self):
        self.compressed_value = (self.orientation & 7) << 12 | self.id & 4095
