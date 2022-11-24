


class Node(object):

    def __init__(self, vertex, mapp, cost=None, heuristic=None, parent=None):

        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.map = mapp
        self.vertex = vertex

    def getVertex(self):
        return self.vertex

    def getCost(self):
        return self.cost

    def getHeuristic(self):
        return self.heuristic

    def getMap(self):
        return self.map

    def getParent(self):
        return self.parent