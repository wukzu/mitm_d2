

from Mapdata import Mapdata

from Node import Node

class AStar:

    def search(worldGraph, fromm, to):

        print("helo")
        if(fromm == to):
            print("search: fromm == to")
            return -1

        #self.initForbiddenSubareaList()

        AStar.worldGraph = worldGraph
        AStar.to = to

        AStar.dest = Mapdata.getData(to.getMapId())
        AStar.closedDic = dict()
        AStar.openList = []
        AStar.openDic = dict()

        AStar.iterations = -1 # A revoir
        AStar.openList.append(Node(fromm,Mapdata.getData(fromm.getMapId()))) # A tester 
        pathh = AStar.compute()
        return pathh

    def buildResultPath(worldGraph, node):

        result = []
        actualNode = node

        while actualNode.getParent() != None: # Vérifier si c'est bien None renvoyé si 
            result.append(worldGraph.getEdge(actualNode.getParent().getVertex(), actualNode.getVertex()))
            actualNode = actualNode.getParent()

        result.reverse()
        return result

    def orderNodes(a, b=None): # A vérifier
        aHeuristic = a.getHeuristic()
        if(b != None):
            bHeuristic = b.getHeuristic()

        if(b != None):
            if(aHeuristic == bHeuristic):
                return 0
            elif(aHeuristic > bHeuristic):
                return 1
            elif(aHeuristic < bHeuristic):
                return -1
        else:
            return 0

        # or just, return aHeuristic - bHeuristic. The compare function does not have to return -1 or 1, but merely a negative or positive number (or zero). 

    def hasValidTransition(edge):
        return True # A FAIRE

    def hasValidDestinationSubarea(edge):
        fromMapId = edge.getFromm().getMapId()
        fromSubareaId = Mapdata.getData(fromMapId)['subAreaId']
        toMapId = edge.getTo().getMapId()
        toSubareaId = Mapdata.getData(toMapId)['subAreaId']
        if fromSubareaId == toSubareaId:
            return True
        return True

    def compute():
        current = None
        edges = None
        oldLength = 0
        cost = 0
        edge = None
        existing = None
        mapp = None
        manhattanDistance = 0
        node = None


        while len(AStar.openList) > 0:

            AStar.iterations += 1



            if AStar.iterations > 50000:
                print("Trop d'itération, max atteint")
                return -1
            #print("currentccc:", current)
            current = AStar.openList.pop(0)
            #print("currentddd:", current)
            if current.getVertex() in AStar.openDic:
                del AStar.openDic[current.getVertex()]

            if current.getVertex() == AStar.to:
                print("goal reached in ", AStar.iterations, " itérations")
                res = AStar.buildResultPath(AStar.worldGraph, current)
                return res

            edges = AStar.worldGraph.getOutgoingEdgesFromVertex(current.getVertex())
            oldLength = len(AStar.openList)
            #print("currentttt : ", current)
            if current.getCost() != None:
                cost = current.getCost() + 1
            else:
                cost = 1

            if edges != None:
                for edge in edges:

                    if(AStar.hasValidTransition(edge)):

                        if(AStar.hasValidDestinationSubarea(edge)):
                            existing = AStar.closedDic.get(edge.getTo()) # à créer getTo

                            if(existing != None):
                                existing_cond = 0
                                if existing.getCost() != None:
                                    existing_cond = existing.getCost()

                            if( not ( existing != None and cost >= existing_cond ) ): #A revoir
                                existing = AStar.openDic.get(edge.getTo())  # à créer getTo
                                
                                if(existing != None):
                                    existing_cond = 0
                                    if existing.getCost() != None:
                                        existing_cond = existing.getCost()

                                if( not (existing != None and cost >= existing_cond)): #A revoir
                                    mapp = Mapdata.getData(edge.getTo().getMapId()) 



                                    if(mapp == None): #Gérer dans la classe map, si on ne trouve rien, renvoyer None ou -1 #Et également gérer un mapOutdoor / indoor
                                        print("La map ne semble pas exister !")
                                        return -1

                                    

                                    else:
                                        manhattanDistance = abs(mapp['posX'] - AStar.dest['posX']) + abs(mapp['posY'] - AStar.dest['posY'])
                                        salt = 0
                                        """
                                        if(current.getMap().isOutdoor() and not mapp.isOutdoor()):
                                            salt = 0
                                        else:
                                            salt = 0
                                        """
                                        node = Node(edge.getTo(), mapp, cost=cost, heuristic=cost + 1 * manhattanDistance, parent=current)
                                        AStar.openList.append(node)
                                        AStar.openDic[node.getVertex()] = node
                
            AStar.closedDic[current.getVertex()] = current

            if(oldLength < len(AStar.openList)):
                AStar.openList.sort(key=AStar.orderNodes)

            

                                