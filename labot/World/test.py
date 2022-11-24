


from WorldPathFinder import WorldPathFinder
WorldPathFinder.setData("C:/Users/llegay/Documents/world-graph.binary")
path = WorldPathFinder.findPath(191104004, 188745222, 308)
print("--------- path :", path)
lastTransition = {"TransitionMapId":0, "skill" : 0, "cellId" : 0, "id" : 0}
for p in path:
    t = p.getTransitions()
    print(t)
    for transition in t:
        direction = transition.getDirection()
        cell = transition.getCell()
        transitionMapId = transition.getTransitionMapId()
        skill = transition.getSkillId()
        ID = transition.getId()

        if(direction == 2):
            if(cell == 545 or cell == 559):
                cell = 558
            
        

        if(lastTransition['TransitionMapId'] != transitionMapId):
            if skill == -1:



                if(direction == 2):
                    print("move top")
                
                elif(direction == 6):
                    print("move bottom")
                    
                elif(direction == 4):
                    print("move left")
                    
                elif(direction == 0):
                    print("move right")
            
            else:

                print("use ", cell)

            
            # direction bas : y 490 2
            # direction haut : y 1 6
            #direction gauche : x 1 4 
            #direction droite : y 695 0

            

            
            
            
        else:
            print("même transition  :", transition.toString()) 


        lastTransition = {"TransitionMapId":transitionMapId}
           