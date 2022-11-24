

import zlib, tempfile, io
from Utils._binarystream import _BinaryStream
from collections import OrderedDict

from Vertex import Vertex
from Edge import Edge
from Node import Node
from Transition import Transition

class Worldgraph:
    def __init__(self, data):
        
        fromm = None
        dest = None
        edge = None
        transitionCount = 0

        self._vertexUid = 0

        self._verticles = dict()
        self._edges = dict()
        self._outgoingEdges = dict()

        raw = _BinaryStream(data, True)
        edgeCount = raw.read_int32()

        print("edgeCount:", edgeCount)

        for i in range(0,edgeCount):
            
            frommapid = raw.read_double()
            fromzone = raw.read_int32()

            fromm = self.addVertex(int(frommapid), fromzone)
            
            tomapid = raw.read_double()
            tozone = raw.read_int32()
            
            dest = self.addVertex(int(tomapid), tozone)

            edge = self.addEdge(fromm,dest)

            transitionCount = raw.read_int32()



            #print("from mapid:", frommapid, ", fromZone:", fromzone, ", toMapID:", tomapid, ", toZone:", tozone)
            #print("transition count:", transitionCount)
            
            for y in range(0,transitionCount):
                _dir = raw.read_char()
                _type = raw.read_char()
                _skill = raw.read_int32()
                _text = str(raw.read_string_bytes(raw.read_int32()))
                _transitionMapID = raw.read_double()
                _cell = raw.read_int32()
                _id = raw.read_double()
                edge.addTransition(_type, _dir, _skill, _text, _transitionMapID, _cell, _id )
                #print("-- dir:", _dir,", type:", _type,", skill:", _skill,", criterion:", _text,", transitionMapID:", _transitionMapID, " cell:", _cell, ", id:",_id)

    def addVertex(self, mapId, zone):

        if(self._verticles.get(mapId) == None):
            self._verticles[mapId] = dict()
        
        vertex = self._verticles.get(mapId).get(zone)

        if(vertex == None):
            vertex = Vertex(mapId, zone, self._vertexUid)
            self._vertexUid = self._vertexUid + 1
            self._verticles[mapId][zone] = vertex
        
        return vertex

    def getVertex(self, mapId, mapRpZone):
        if(self._verticles.get(mapId) == None):
            return None
        
        if(self._verticles.get(mapId).get(mapRpZone) == None):
            return None
        
        return self._verticles.get(mapId).get(mapRpZone)

    def getOutgoingEdgesFromVertex(self, fromm):
        if(self._outgoingEdges.get(fromm.getUID()) == None):
            return None
        
        return self._outgoingEdges.get(fromm.getUID())

    def getEdge(self, fromm, dest):
        if self._edges.get(fromm.getUID()) == None:
            return None

        if self._edges.get(fromm.getUID()).get(dest.getUID()) == None:
            return None
        
        return self._edges.get(fromm.getUID()).get(dest.getUID())

    def getEdges(self):
        return self._edges

    
    def addEdge(self, fromm, dest):
        edge = self.getEdge(fromm, dest)
        if(edge != None):
            return edge
        
        if not self.doesVertexExist(fromm) or not self.doesVertexExist(dest):
            return None
        
        edge = Edge(fromm, dest)

        if(self._edges.get(fromm.getUID()) == None):
            self._edges[fromm.getUID()] = dict()
        
        self._edges[fromm.getUID()][dest.getUID()] = edge

        outgoing = self._outgoingEdges.get(fromm.getUID())

        if(outgoing == None):
            outgoing = []
            self._outgoingEdges[fromm.getUID()] = outgoing
        
        self._outgoingEdges[fromm.getUID()].append(edge)
        #outgoing.append(edge)

        return edge


    def doesVertexExist(self, v):
        
        if(self._verticles.get(v.getMapId()).get(v.getZoneId()) != None):
            return True
        else:
            return False



    def getVerticles(self):
        return self._verticles
    





