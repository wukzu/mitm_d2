class Vertex(object):

    def __init__(self, mapId, zoneId, vertexUid):
        self._mapId = mapId
        self._zoneId = zoneId
        self._uid = vertexUid
    
    def getMapId(self):
        return self._mapId

    def getZoneId(self):
        return self._zoneId
    
    def getUID(self):
        return self._uid

    
