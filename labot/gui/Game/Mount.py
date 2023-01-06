
from ..utils.Sockets import Socket
import time
import random

class Mount:
    def __init__(self, gui):
        self.Gui = gui

        self.isSlapping = False
        self.isCaressing = False
        self.isStamina = False
        self.isLove = False


        self.mounts = []
        self.mountsToLevelUp = []
        self.stabledMounts = []
        self.paddockedMounts = []

    def toggleSlapping(self):
        if self.isSlapping == True:
            self.isSlapping = False
            self.Gui.btnMountlapping['text'] = 'Start baffeurs'
        else:
            self.isSlapping = True
            self.Gui.btnMountlapping['text'] = 'Stop baffeurs'
            self.getMountsToSlap()
        
    def toggleStamina(self):
        if self.isStamina == True:
            self.isStamina = False
            self.Gui.btnMountStamina['text'] = 'Start foudroyeurs'
        else:
            self.isStamina = True
            self.Gui.btnMountStamina['text'] = 'Stop foudroyeurs'
            self.getMountsToStamina()
    
    
    def toggleLove(self):
        if self.isLove == True:
            self.isLove = False
            self.Gui.btnMountLove['text'] = 'Start dragofesses'
        else:
            self.isLove = True
            self.Gui.btnMountLove['text'] = 'Stop dragofesses'
            self.getMountsToLove()

    def toggleCaressing(self):
        if self.isCaressing == True:
            self.isCaressing = False
            self.Gui.btnMountCaressing['text'] = 'Start caresseurs'
        else:
            self.isCaressing = True
            self.Gui.btnMountCaressing['text'] = 'Stop caresseurs'
            self.getMountsToCaress()
        
        print("<><> slapping :", self.isSlapping)
    
    def getMountsToLevelUp(self, mounts):
        for mount in mounts:
            if mount['place'] == 's' and mount['level'] < 5 and mount['love'] >= 7500 and mount['maturity'] == mount['maturityForAdult'] and mount['stamina'] >= 7500:
                self.mountsToLevelUp.append(mount['id'])

    def getMountsToSlap(self):
        timeToWait = random.randint(500, 3000)
        self.Gui.waitTime(timeToWait)
        for mount in self.stabledMounts:
            if (self.paddockedMounts) == 10:
                break
            if ((mount['stamina'] < 7500 and
                ((mount['love'] > 7500 and ((mount['sex'] == True and mount['serenity'] >= -1000) or (mount['sex'] == False and mount['serenity'] >= 0))) or
                ((mount['love'] < 7500 and (mount['sex'] == True and mount['serenity'] < -500 and mount['serenity'] > -1000))) or 
                ((mount['love'] < 7500 and (mount['sex'] == False and mount['serenity'] > 0 and mount['serenity'] < 500))))) or 
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] >= 1999) or (mount['sex'] == True and mount['serenity'] >= 999)))):
                
                print("->>> mount to slap :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))

                timeToWait = random.randint(1000, 5000)
                self.Gui.waitTime(timeToWait)

    def getMountsToCaress(self):
        timeToWait = random.randint(500, 3000)
        self.Gui.waitTime(timeToWait)
        print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))
        for mount in self.stabledMounts:
            if len(self.paddockedMounts) == 10:
                break
            if ((mount['love'] < 7500 and
                ((mount['stamina'] > 7500 and ((mount['sex'] == True and mount['serenity'] < 0) or (mount['sex'] == False and mount['serenity'] < 1000))) or
                ((mount['stamina'] < 7500 and (mount['sex'] == False and mount['serenity'] > 500 and mount['serenity'] < 1000))) or 
                ((mount['stamina'] < 7500 and (mount['sex'] == True and mount['serenity'] > -500 and mount['serenity'] < 0))))) or
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] <= -999) or (mount['sex'] == True and mount['serenity'] <= -1999)))):
                
                print("->>> mount to caress :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(1000, 5000)
                self.Gui.waitTime(timeToWait)
        
        print("<----> ended mounts to paddock")

    def getMountsToStamina(self):
        timeToWait = random.randint(500, 3000)
        self.Gui.waitTime(timeToWait)
        print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))

        for mount in self.stabledMounts:
            if len(self.paddockedMounts) == 10:
                break
        
            if (mount['stamina'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] < 0) or (mount['sex'] == True and mount['serenity'] < -1000))):

                print("->>> mount to stamina :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(1000, 5000)
                self.Gui.waitTime(timeToWait)
        
        print("<----> ended mounts to paddock")

    def getMountsToLove(self):
        timeToWait = random.randint(500, 3000)
        self.Gui.waitTime(timeToWait)

        for mount in self.stabledMounts:
            print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))
            if len(self.paddockedMounts) >= 10:
                break
        
            if (mount['love'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] > 1000) or (mount['sex'] == True and mount['serenity'] > 0))):

                print("->>> mount to love :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(1000, 5000)
                self.Gui.waitTime(timeToWait)
        
        print("<----> ended mounts to paddock")

    def getMountsInfo(self):
        print("---------------- MOUNT INFOS") 
        needCaressing = 0
        needSlapping = 0
        needLove = 0
        needStamina = 0

        for mount in self.stabledMounts:
            if ((mount['stamina'] < 7500 and
                ((mount['love'] > 7500 and ((mount['sex'] == True and mount['serenity'] >= -1000) or (mount['sex'] == False and mount['serenity'] >= 0))) or
                ((mount['love'] < 7500 and (mount['sex'] == True and mount['serenity'] < -500 and mount['serenity'] > -1000))) or 
                ((mount['love'] < 7500 and (mount['sex'] == False and mount['serenity'] > 0 and mount['serenity'] < 500))))) or 
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > 1999) or (mount['sex'] == True and mount['serenity'] > 999)))):
                needSlapping = needSlapping + 1
                print("need to SLAP :", mount)
            
            if ((mount['love'] < 7500 and
                ((mount['stamina'] > 7500 and ((mount['sex'] == True and mount['serenity'] < 0) or (mount['sex'] == False and mount['serenity'] < 1000))) or
                ((mount['stamina'] < 7500 and (mount['sex'] == False and mount['serenity'] > 500 and mount['serenity'] < 1000))) or 
                ((mount['stamina'] < 7500 and (mount['sex'] == True and mount['serenity'] > -500 and mount['serenity'] < 0))))) or
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] < -999) or (mount['sex'] == True and mount['serenity'] < -1999)))):
                needCaressing = needCaressing + 1
                print("need to CARESS :", mount)
            
            if (mount['stamina'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] < 0) or (mount['sex'] == True and mount['serenity'] < -1000))):
                needStamina = needStamina + 1
                print("need to STAMINA :", mount)

            if (mount['love'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] > 1000) or (mount['sex'] == True and mount['serenity'] > 0))):
                needLove = needLove + 1
                print("need to LOVE :", mount)
        
        final = "Love : " + str(needLove) + ' - Stamina : ' + str(needStamina) + " - Slapping : " + str(needSlapping) + " - Caressing : " + str(needCaressing)
        
        print("---------------- final :", final) 
        self.Gui.lDDInfos.config(text = final)




    def socketHandler(self, action, data):
        
        if action == "allMounts":
            self.mounts = data['mounts']
            self.getMountsToLevelUp(data['mounts'])

            self.stabledMounts = [x for x in data['mounts'] if x['place'] == 's']
            self.paddockedMounts = [x for x in data['mounts'] if x['place'] == 'p']

            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")
            print("--------------------")

            self.getMountsInfo()

        if action == "mountsAddedPaddock":
            for newMount in data['mountsAdded']:
                self.paddockedMounts.append(newMount)
            
        if action == "mountsRemovePaddock":
            for removedMount in data['mountsRemoved']:
                self.paddockedMounts = [
                    item for item in self.paddockedMounts if item.get('id') != removedMount
                ]
        
        if action == "mountsAddedStable":
            for newMount in data['mountsAdded']:
                self.stabledMounts.append(newMount)

        if action == "mountsRemoveStable":
            for removedMount in data['mountsRemoved']:
                self.stabledMounts = [
                    item for item in self.stabledMounts if item.get('id') != removedMount
                ]
        
        print("--- mounts stabble :", len(self.stabledMounts), " | mounts paddocked : ", len(self.paddockedMounts))

        if action == "mountBoostUpdated":
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> mount updated')
            print("data :", data)

            
            for mount in self.paddockedMounts:
                if mount['id'] == data['mountId']:

                    for boost in data['boostList']:
                        if boost['type'] == 2:
                            mount['serenity'] = boost['value']
                        elif boost['type'] == 3:
                            mount['stamina'] = boost['value']
                        elif boost['type'] == 4:
                            mount['love'] = boost['value']

                    self.mountPaddockActionHandler(mount)

    def mountPaddockActionHandler(self, mount):
        print("   -> mountPaddockActionHandler :", mount)
        if self.isSlapping:
            if (((mount['stamina'] < 7500) and ((mount['serenity'] < 0 and mount['sex'] == False) or (mount['serenity'] <= -1000 and mount['sex'] == True))) or 
                ((mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999)))))):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
                self.getMountsToCaress()

        elif self.isCaressing:
            if (((mount['love'] < 7500) and ((mount['serenity'] > 1000 and mount['sex'] == False) or (mount['serenity'] > 0 and mount['sex'] == True))) or 
                ((mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999)))))):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
                self.getMountsToCaress()
        
        elif self.isStamina:
            if (mount['stamina'] > 7500):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
                self.getMountsToStamina()
        
        elif self.isLove:
            if (mount['love'] > 7500):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
                self.getMountsToLove()
        
                


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
        
        self.Gui.waitCallback("mountsRemoveStable")
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
        






        