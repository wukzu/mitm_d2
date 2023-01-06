


import json

class FileReader:
    def openJsonMap(mapId):
        i = 0
        dp = 0
        while dp < 7:
            while i < 10:
                try:
                    print("trying " +str(dp) + " - " + str(i))
                    file = open("C:/Users/33630/Desktop/mitm/mitm_d2/sources/data/maps/maps" + str(dp) + ".d2p/" + str(i) + "/" + str(mapId) + ".json")
                    data = json.load(file)
                    return data
                    break
                except IOError:
                    pass
                i = i + 1
            dp = dp + 1
            i = 0

  

