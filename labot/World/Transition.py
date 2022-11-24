


class Transition:

    def __init__(self, typee, direction, skillId, criterion, transitionMapId, cell, idd):
        self._typee = typee
        self._direction = direction
        self._skillId = skillId
        self._criterion = criterion
        self._transitionMapId = transitionMapId
        self._cell = cell
        self._id = idd

    def getType(self):
        return self._typee
        
    def getDirection(self):
        return self._direction
        
    def getSkillId(self):
        return self._skillId
        
    def getCriterion(self):
        return self._criterion
        
    def getTransitionMapId(self):
        return self._transitionMapId
        
    def getCell(self):
        return self._cell
        
    def getId(self):
        return self._id

    def toString(self):
        return "type:", self.getType(), ", direction:", self.getDirection(), ", skill:", self.getSkillId(), ", Criterion:", self.getCriterion(), ", TransitionMapId:", self.getTransitionMapId(), ", Cell:", self.getCell(), ", id:", self.getId()


