
from Transition import Transition


class Edge(object):

    def __init__(self, fromm, to):
        self._fromm = fromm
        self._to = to
        self._transitions = [] #Type transition

    def getFromm(self):
        return self._fromm
        
    def getTo(self):
        return self._to

    def getTransitions(self):
        return self._transitions

    def addTransition(self, dir, typee, skill, criterion, transitionMapId, cell, idd):
        self._transitions.append(Transition(dir, typee, skill, criterion, transitionMapId, cell, idd))

    
