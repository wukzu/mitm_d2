
from ..utils.Sockets import Socket
import time

class Mount:
    def __init__(self, gui):
        self.Gui = gui
        self.mountsToLevelUp = []

    def socketHandler(self, action, data):
        print("DATA FROM MOUNT SOCKET HANDLER :", data)

        if action == "mountsToLevelUp":
            self.mountsToLevelUp = data['mounts']
            print("--------- data :", data)
            print('--------- zdvkubzcvkubzevzv', self.mountsToLevelUp)


    def routeToUpMount(self):
        print("----- routeToUpMount() ")
        if len(self.mountsToLevelUp) == 0:
            return "aucune DD à monter"
        
        mountToUp = self.mountsToLevelUp[0]
        mountToUpId = int(mountToUp['id'])
        print("----- mountToUp ", mountToUp)
        print("----- mount chosen :", mountToUpId)

        ### TODO  nourir monture
        ### TODO  nourir monture
        ### TODO  nourir monture

        self.Gui.qSocket.put(Socket.rideMount(mountToUpId))
        
        self.Gui.waitCallback("ExchangeMountsStableRemoveMessage")
        print("<<< mount riding")
        time.sleep(1000/1000)

        self.Gui.Window.clickCellIdWithDeltaX(41, 24) # Clique sur la croix
        print("<<< croix cliqué")
        time.sleep(1300/1000)

        self.Gui.qSocket.put(Socket.mountSetXpRatio(90))
        self.Gui.waitCallback("MountXpRatioMessage")
        print("<<< mount xp ratio setted")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(Socket.rideMountOnPlayer())
        self.Gui.waitCallback("MountRidingMessage")
        print("<<< mount riding on player")
        time.sleep(1000/1000)
        
        
        self.Gui.qSocket.put(Socket.EnterHavenBag(self.Gui.Player.id))
        self.Gui.waitCallback("mapHavenBagInformations")
        time.sleep(1000/1000)

        self.Gui.qSocket.put(Socket.useHavenbagZaap(self.Gui.Map.zaap))
        self.Gui.waitCallback('ZaapDestinationsMessage')
        time.sleep(1000/1000)

        print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")


        # TODO 
        # Aller zaap up dd
        # boucle de combat avec changement de map jusqu'au niveau 5
        






        