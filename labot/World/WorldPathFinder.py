
import sys, json
from Worldgraph import Worldgraph

from Mapdata import Mapdata
from AStar import AStar

class WorldPathFinder:
    
    worldgraph = None
    fromm = None
    to = None
    dest = None
    linkedZone = None

    @staticmethod
    def setData(path):

        wg_input = open(path, "rb")
        #wg_input = "test"
        WorldPathFinder.worldgraph = Worldgraph(wg_input)
        print("---")
        print(WorldPathFinder.worldgraph)


    def getTransitionSkillCell(path):
        for p in path:
            t = p.getTransitions()
            for transition in t:
                return { "skill": transition.getSkillId(), "cell": transition.getCell() }

    def findPath(destinationMapId, actualMapId, actualCellId):

        actualLinkedZoneRP = Mapdata.getCellLinkedZone(actualMapId, actualCellId)

        if actualLinkedZoneRP == None or actualLinkedZoneRP == -1:
            print("Il y a eu une erreur linkedZoneRP")
            return -1
        
        WorldPathFinder.fromm = WorldPathFinder.worldgraph.getVertex(actualMapId, actualLinkedZoneRP)

        if WorldPathFinder.fromm == None or WorldPathFinder.fromm == -1:
            print("Il y a eu une erreur getVertex")
            return -1
        
        WorldPathFinder.to = destinationMapId

        WorldPathFinder.linkedZone = 1

        path = WorldPathFinder.Next()
        return path


        

    def Next():
        path = AStar.search(WorldPathFinder.worldgraph, WorldPathFinder.fromm, WorldPathFinder.worldgraph.getVertex(WorldPathFinder.to,WorldPathFinder.linkedZone))
        

        if(path != None or path != -1):
            return path
        else:
            WorldPathFinder.linkedZone = WorldPathFinder.linkedZone + 1
            WorldPathFinder.Next()




    def getWorldgraph():
        return WorldPathFinder.worldgraph


