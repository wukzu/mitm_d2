

import json
import Variables as Variables

from FileReader import FileReader


class Mapdata:
   
    def getData(mapId):
       
        # Lire le fichier JSON dlm correspondant à la mapId
       
        posX = None
        posY = None
        result = [p for p in Variables.mapCoordinatesAll if str(p["mapId"]) == str(mapId)]
        posX = result[0]['posX'] 
        posY = result[0]['posY'] 
        
        subAreaId = result[0]["subAreaId"]
        outdoor = result[0]["outdoor"]

        result = {'posX':posX, 'posY':posY, 'subAreaId':subAreaId, 'outdoor':outdoor}
       
        return result
   
    def getCellLinkedZone(mapId, cellId):
       
        #cellId = 457
        #Récupère l'objet de la cellId dans lel fichier mapId.dlm.json correspondant
       
        cellLikedZone = None
        moveZone = None
        try:
            data = FileReader.openJsonMap(int(mapId))

            print("mapId :", mapId, cellId)
            
            cellData = data.get('cells')[cellId]
            cellLikedZone = cellData.get('_linkedZone')
            moveZone = cellData.get('moveZone')

                    
        except IndexError:
            print("erreur d'index")
            return None
        except FileNotFoundError:
            print("erreur FileNotFoundError")
            return -1

        if cellLikedZone != None:
            return (cellLikedZone & 240) >> 4
        
        return (moveZone & 240) >> 4
       
     
 