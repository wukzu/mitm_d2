
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
        self.isMaturity = False

        self.staminaObjectUID = 0

        self.loveAndStamina = False


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
    
    def toggleMaturity(self):
        
        if self.isMaturity == True:
            self.isMaturity = False
            self.Gui.btnMountMaturity['text'] = 'Start maturité'
        else:
            self.isMaturity = True
            self.Gui.btnMountMaturity['text'] = 'Stop maturité'
            self.getMountsToMaturity()
        

    
    def getMountsToLevelUp(self, mounts):
        for mount in mounts:
            if mount['place'] == 's' and mount['level'] < 5 and mount['love'] >= 7500 and mount['maturity'] == mount['maturityForAdult'] and mount['stamina'] >= 7500:
                self.mountsToLevelUp.append(mount['id'])

    def getMountsToSlap(self):
        timeToWait = random.randint(50, 600)
        self.Gui.waitTime(timeToWait)
        for mount in self.stabledMounts:
            if (self.paddockedMounts) == 10:
                break
            if (mount['boostLimiter'] < mount['boostMax'] and ((mount['stamina'] < 7500 and
                ((mount['love'] > 7500 and ((mount['sex'] == True and mount['serenity'] >= -1000) or (mount['sex'] == False and mount['serenity'] >= 0))) or
                ((mount['love'] < 7500 and (mount['sex'] == True and mount['serenity'] < -500 and mount['serenity'] > -1000))) or 
                ((mount['love'] < 7500 and (mount['sex'] == False and mount['serenity'] > 0 and mount['serenity'] < 500))))) or 
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] >= 1999) or (mount['sex'] == True and mount['serenity'] >= 999))))):
                
                print("->>> mount to slap :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))

                timeToWait = random.randint(300, 2000)
                self.Gui.waitTime(timeToWait)
                break

    def getMountsToCaress(self):
        timeToWait = random.randint(50, 600)
        self.Gui.waitTime(timeToWait)
        print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))
        for mount in self.stabledMounts:
            if len(self.paddockedMounts) == 10:
                break
            if (mount['boostLimiter'] < mount['boostMax'] and ((mount['love'] < 7500 and
                ((mount['stamina'] > 7500 and ((mount['sex'] == True and mount['serenity'] < 0) or (mount['sex'] == False and mount['serenity'] < 1000))) or
                ((mount['stamina'] < 7500 and (mount['sex'] == False and mount['serenity'] > 500 and mount['serenity'] < 1000))) or 
                ((mount['stamina'] < 7500 and (mount['sex'] == True and mount['serenity'] > -500 and mount['serenity'] < 0))))) or
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] <= -999) or (mount['sex'] == True and mount['serenity'] <= -1999))))):
                
                print("->>> mount to caress :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(300, 2000)
                self.Gui.waitTime(timeToWait)
                break
        
        print("<----> ended mounts to paddock")

    def getMountsToStamina(self):
        timeToWait = random.randint(50, 600)
        self.Gui.waitTime(timeToWait)
        print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))

        for mount in self.stabledMounts:
            if len(self.paddockedMounts) == 10:
                break
        
            if (mount['boostLimiter'] < mount['boostMax'] and (mount['stamina'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] < 0) or (mount['sex'] == True and mount['serenity'] < -1000)))):

                print("->>> mount to stamina :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(300, 2000)
                self.Gui.waitTime(timeToWait)
                break
        
        print("<----> ended mounts to paddock")

    def getMountsToLove(self):
        timeToWait = random.randint(50, 600)
        self.Gui.waitTime(timeToWait)
        hasMountLeft = False

        for mount in self.stabledMounts:
            print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))
            if len(self.paddockedMounts) >= 10:
                break
        
            if (mount['boostLimiter'] < mount['boostMax'] and (mount['love'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] > 1000) or (mount['sex'] == True and mount['serenity'] > 0)))):

                hasMountLeft = True

                print("->>> mount to love :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(300, 2000)
                self.Gui.waitTime(timeToWait)
                break
        
        if not hasMountLeft and len(self.paddockedMounts) < 10 and self.loveAndStamina:
            self.isLove = False
            self.placeObjects()
        print("<----> ended mounts to paddock")
    
    
    def getMountsToMaturity(self):
        timeToWait = random.randint(50, 600)
        self.Gui.waitTime(timeToWait)
        for mount in self.stabledMounts:
            print("getMountsToCaress -------------------------- >>>>>>>>>> length paddock :", len(self.paddockedMounts))
            if len(self.paddockedMounts) >= 10:
                break
        
            if (mount['boostLimiter'] < mount['boostMax'] and (mount['love'] > 7500 and mount['stamina'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and
                (((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999)))))):

                print("->>> mount to maturity :", mount)
                self.Gui.qSocket.put(Socket.mountMoveStableToPaddock([mount['id']]))
                
                timeToWait = random.randint(300, 2000)
                self.Gui.waitTime(timeToWait)
                break


    def getMountsInfo(self):
        print("---------------- MOUNT INFOS") 
        needCaressing = 0
        needSlapping = 0
        needLove = 0
        needStamina = 0
        needMaturity = 0

        for mount in self.stabledMounts:
            if ((mount['stamina'] < 7500 and
                ((mount['love'] > 7500 and ((mount['sex'] == True and mount['serenity'] >= -1000) or (mount['sex'] == False and mount['serenity'] >= 0))) or
                ((mount['love'] < 7500 and (mount['sex'] == True and mount['serenity'] < -500 and mount['serenity'] > -1000))) or 
                ((mount['love'] < 7500 and (mount['sex'] == False and mount['serenity'] > 0 and mount['serenity'] < 500))))) or 
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > 1999) or (mount['sex'] == True and mount['serenity'] > 999)))):
                needSlapping = needSlapping + 1
            
            if ((mount['love'] < 7500 and
                ((mount['stamina'] > 7500 and ((mount['sex'] == True and mount['serenity'] < 0) or (mount['sex'] == False and mount['serenity'] < 1000))) or
                ((mount['stamina'] < 7500 and (mount['sex'] == False and mount['serenity'] > 500 and mount['serenity'] < 1000))) or 
                ((mount['stamina'] < 7500 and (mount['sex'] == True and mount['serenity'] > -500 and mount['serenity'] < 0))))) or
                (mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] < -999) or (mount['sex'] == True and mount['serenity'] < -1999)))):
                needCaressing = needCaressing + 1
            
            if (mount['stamina'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] < 0) or (mount['sex'] == True and mount['serenity'] < -1000))):
                needStamina = needStamina + 1

            if (mount['love'] < 7500 and
                ((mount['sex'] == False and mount['serenity'] > 1000) or (mount['sex'] == True and mount['serenity'] > 0))):
                needLove = needLove + 1
            
            if (mount['love'] > 7500 and mount['stamina'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and
                (((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999))))):
                needMaturity = needMaturity + 1
        
        final = "Love : " + str(needLove) + ' - Stamina : ' + str(needStamina) + " - Slapping : " + str(needSlapping) + " - Caressing : " + str(needCaressing) + " - Maturity : " + str(needMaturity)
        
        print("---------------- final :", final) 
        try:
            self.Gui.lDDInfos.config(text = final)
        except:
            pass




    def socketHandler(self, action, data):

        if action == "staminaUID":
            self.staminaObjectUID = data['objectUID']
        
        if action == "allMounts":
            self.mounts = data['mounts']
            self.getMountsToLevelUp(data['mounts'])

            self.stabledMounts = [x for x in data['mounts'] if x['place'] == 's']
            self.paddockedMounts = [x for x in data['mounts'] if x['place'] == 'p']

            self.getMountsInfo()

        if action == "mountsAddedPaddock":
            for newMount in data['mountsAdded']:
                self.paddockedMounts.append(newMount)
                mountId = newMount['id']

                self.stabledMounts = [
                    item for item in self.stabledMounts if item.get('id') != mountId
                ]
            
            if self.isSlapping:
                self.getMountsToSlap()
            elif self.isCaressing:
                self.getMountsToCaress()
            elif self.isLove:
                self.getMountsToLove()
            elif self.isStamina:
                self.getMountsToStamina()
            elif self.isMaturity:
                self.getMountsToMaturity()
            
        
        if action == "mountsAddedStable":
            for newMount in data['mountsAdded']:
                self.stabledMounts.append(newMount)

                mountId = newMount['id']
                self.paddockedMounts = [
                    item for item in self.paddockedMounts if item.get('id') != mountId
                ]

            if self.isSlapping:
                self.getMountsToSlap()
            elif self.isCaressing:
                self.getMountsToCaress()
            elif self.isLove:
                self.getMountsToLove()
            elif self.isStamina:
                self.getMountsToStamina()
            elif self.isMaturity:
                self.getMountsToMaturity()

        if action == "mountBoostUpdated":
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> mount updated')
            print("data :", data)

            
            for mount in self.paddockedMounts:
                if mount['id'] == data['mountId']:

                    for boost in data['boostList']:
                        if boost['type'] == 6:
                            mount['boostLimiter'] = boost['value']
                        if boost['type'] == 2:
                            mount['serenity'] = boost['value']
                        elif boost['type'] == 3:
                            mount['stamina'] = boost['value']
                        elif boost['type'] == 4:
                            mount['love'] = boost['value']
                        elif boost['type'] == 5:
                            mount['maturity'] = boost['value']

                    self.mountPaddockActionHandler(mount)

    def mountPaddockActionHandler(self, mount):
        print("   -> mountPaddockActionHandler :", mount)
        if mount['boostLimiter'] >= mount['boostMax']:
            self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))

        elif self.isSlapping:
            if (((mount['stamina'] < 7500) and ((mount['serenity'] < 0 and mount['sex'] == False) or (mount['serenity'] <= -1000 and mount['sex'] == True))) or 
                ((mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999)))))):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))

        elif self.isCaressing:
            if (((mount['love'] < 7500) and ((mount['serenity'] > 1000 and mount['sex'] == False) or (mount['serenity'] > 0 and mount['sex'] == True))) or 
                ((mount['stamina'] > 7500 and mount['love'] > 7500 and mount['maturity'] < mount['maturityForAdult'] and 
                ((mount['sex'] == False and mount['serenity'] > -999 and mount['serenity'] < 1999) or
                ((mount['sex'] == True and mount['serenity'] > -1999 and mount['serenity'] < 999)))))):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
        
        elif self.isStamina:
            if (mount['stamina'] > 7500):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
        
        elif self.isLove:
            if (mount['love'] > 7500):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))
            
        elif self.isMaturity:
            if (mount['maturity'] >= mount['maturityForAdult']):
                print('>> moving to stable')
                self.Gui.qSocket.put(Socket.mountMovePaddockToStable([mount['id']]))

    def waitRandomTime(self):
        timeToWait = random.randint(300, 1500)
        self.Gui.waitTime(timeToWait)

        
    def placeObjects(self):
        self.Gui.Window.clickCellIdWithDeltaX(41, 24) # Clique sur la croix
        timeToWait = random.randint(2000, 5000)
        self.Gui.waitTime(timeToWait)
        #wait

        self.Gui.qSocket.put(Socket.removeObject(342))
        self.Gui.waitCallback("GameDataPaddockObjectRemoveMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.removeObject(356))
        self.Gui.waitCallback("GameDataPaddockObjectRemoveMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.removeObject(315))
        self.Gui.waitCallback("GameDataPaddockObjectRemoveMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.removeObject(329))
        self.Gui.waitCallback("GameDataPaddockObjectRemoveMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.removeObject(357))
        self.Gui.waitCallback("GameDataPaddockObjectRemoveMessage")
        self.waitRandomTime()

        self.Gui.qSocket.put(Socket.useObject(self.staminaObjectUID, 342))
        self.Gui.waitCallback("GameDataPaddockObjectAddMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.useObject(self.staminaObjectUID, 356))
        self.Gui.waitCallback("GameDataPaddockObjectAddMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.useObject(self.staminaObjectUID, 315))
        self.Gui.waitCallback("GameDataPaddockObjectAddMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.useObject(self.staminaObjectUID, 329))
        self.Gui.waitCallback("GameDataPaddockObjectAddMessage")
        self.waitRandomTime()
        self.Gui.qSocket.put(Socket.useObject(self.staminaObjectUID, 357))
        self.Gui.waitCallback("GameDataPaddockObjectAddMessage")
        self.waitRandomTime()

        self.Gui.qSocket.put(Socket.openMountBrakmar())
        self.Gui.waitCallback("allMounts")

        timeToWait = random.randint(1000, 4000)
        self.Gui.waitTime(timeToWait)
        print("---------------- DONE")
        #self.isStamina = True
        #self.getMountsToStamina()


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
        






        