class Cell:
    def __init__(self, changeMap: bool, walkable: bool, los: bool, column: int, line: int, id: int, location: tuple):
        self.ChangeMap = changeMap
        self.Walkable = walkable
        self.Parent = None
        self.Los = los
        self.Start = False
        self.InClosedList = False
        self.InOpenList = False
        self.End = False
        self.Id = id
        self.Pair = line % 2 == 0
        self.G = 0
        self.Location = location
        self.GetBorder(column, line)

    def GetBorder(self, column: int, line: int):
        self.Position = bytearray(8)
        if line == 0:
            self.Position[0] = 1
        if line == 1:
            self.Position[1] = 1
        if line == 39:
            self.Position[2] = 1
        if line == 38:
            self.Position[3] = 1
        if column == 0 and self.Pair:
            self.Position[4] = 1
        if column == 0 and not self.Pair:
            self.Position[5] = 1
        if column == 13 and not self.Pair:
            self.Position[6] = 1
        if column == 13 and self.Pair:
            self.Position[7] = 1

    def SetH(self, end_cell):
        self.H = int(10 * (abs(end_cell.Location[0] - self.Location[0]) + abs(end_cell.Location[1] - self.Location[1])))

    def __str__(self):
        return f"Id : {self.Id} Location : ({self.Location[0]} ; {self.Location[1]})"
