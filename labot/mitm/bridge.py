"""
Classes to take decisions for transmitting the packets

The classes inheriting from BridgeHandler must
implement `handle`.

The classes inheriting from MsgBridgeHandler must
implement `handle_message`.
"""
import threading

import select
from abc import ABC, abstractmethod
from collections import deque
import os
import logging
import time

from ..data import Buffer, Msg, Dumper
from .. import protocol

import json

logger = logging.getLogger("labot")
# TODO: use the logger


def from_client(origin):
    return origin.getpeername()[0] == "127.0.0.1"


def direction(origin):
    if from_client(origin):
        return "Client->Server"
    else:
        return "Server->Client"

def dictToString(data):
    return json.dumps(data)

def getMonsters(data):
    MonsterGroups = []
    for x in data['actors']:
        if x['__type__'] == 'GameRolePlayGroupMonsterInformations':
            groupId = x['contextualId']
            cellId = x['disposition']['cellId']
            monsters = []
            for m in x['staticInfos']['underlings']:
                monsters.append({
                    'id': m['genericId'],
                    'level': m['level']
                })
            info = x['staticInfos']['mainCreatureLightInfos']
            monsters.append({
                'id': info['genericId'],
                'level': info['level']
            })
            
            MonsterGroups.append({
                'groupId': int(groupId),
                'cellId': int(cellId),
                'monsters': monsters
            })

    return MonsterGroups

def getPlayerCellId(data, Bridge):
    for entity in data['actors']:
        if entity['__type__'] == "GameRolePlayCharacterInformations" and int(entity['contextualId']) == Bridge.actorId:
            return int(entity['disposition']['cellId'])
            break

def getPlayerCharacteristic(data, characteristicId):
    for characteristic in data['stats']['characteristics']:
        if characteristic['characteristicId'] == characteristicId:
            return int(characteristic['base']) + int(characteristic['additional']) + int(characteristic['objectsAndMountBonus'])
            break

def getCharacteristicType(characteristicId):
    if characteristicId == 1:
        return 'PA'
    elif characteristicId == 23:
        return 'PM'
    elif characteristicId == 11:
        return 'PDV'
    else:
        return "NONE"


def handleMessage(Bridge, name, data):
    #print ("---- Handle message Bridge :", str(name), data)
    if Bridge.waiting:
        if name == Bridge.waitingName:
            Bridge.qForm.put(("callback", name))
            Bridge.waiting = False
            Bridge.waitingName = ""

    else:
        if name == 'MapComplementaryInformationsDataInHavenBagMessage':
            zaapElementId = 0
            zaapSkillInstanceUid = 0

            for element in data['interactiveElements']:
                if element['elementTypeId'] == 16:  # Zaap
                    zaapElementId = element['elementId']
                    zaapSkillInstanceUid = element['enabledSkills'][0]['skillInstanceUid']
                    break
            
            Bridge.qForm.put(("mapHavenBagInformations", dictToString({
                'zaap': {
                    'elementId': zaapElementId,
                    'skillInstanceUid': zaapSkillInstanceUid
                }
            })))

        if name == 'ZaapDestinationsMessage':
            Bridge.qForm.put(("ZaapDestinationsMessage", ""))
        
        if name == 'TeleportDestinationsMessage':
            Bridge.qForm.put(("TeleportDestinationsMessage", ""))

        if name == "ExchangeStartOkMountWithOutPaddockMessage":
            Bridge.qForm.put(("stableOpened", ""))



        if name == 'MapComplementaryInformationsDataMessage':
            
            if not Bridge.initialized:
                print("Put Initialized")
                Bridge.qForm.put(("Initialized", ""))
                Bridge.initialized = True
            
            zaapElementId = 0
            zaapSkillInstanceUid = 0

            for element in data['interactiveElements']:
                if element['elementTypeId'] == 16:  # Zaap
                    zaapElementId = element['elementId']
                    zaapSkillInstanceUid = element['enabledSkills'][0]['skillInstanceUid']
                    break

            mapInfos = dictToString({
                'mapId': int(data['mapId']),
                'subAreaId': int(data['subAreaId']),
                'monsters': getMonsters(data),
                'fightStartCells': data['fightStartPositions']['positionsForChallengers'],
                'zaap': {
                    'elementId': zaapElementId,
                    'skillInstanceUid': zaapSkillInstanceUid
                }
            })
            Bridge.qForm.put(("mapInformations", mapInfos))
            try:
                Bridge.qForm.put(('playerUpdateCellId', dictToString({
                    'cellId': getPlayerCellId(data, Bridge)
                })))
            except KeyError:
                pass

        if name == 'CharacterSelectedSuccessMessage':
            Bridge.actorId = int(data['infos']['id'])
            Bridge.qForm.put(("playerInformations", dictToString({
                'id': data['infos']['id'], 
                'name': data['infos']['name'], 
                'level': data['infos']['level']
            })))

        if name == "GameMapMovementMessage" and int(data['actorId']) == Bridge.actorId:
            Bridge.startMovement = True
            Bridge.movementCellId = int(data['keyMovements'][-1])
            Bridge.qForm.put(("PlayerMovementStart", ""))

        
        if name == "GameMapMovementConfirmMessage" and Bridge.startMovement:
            Bridge.confirmMovement = True
        
        
        if name == "GameMapMovementMessage":
            Bridge.qForm.put(("updateActorPosition", dictToString({
                'actorId': int(data['actorId']),
                'cellId': int(data['keyMovements'][-1])
            })))
            if Bridge.inFight == True:
                Bridge.fightStartMoving = True
                try:
                    Bridge.qForm.put(('playerUpdateCellId', dictToString({
                        'cellId': data['cellId']
                    })))
                except Exception as e:
                    print("--- Error 1 :", e)
        if name == "GameContextRemoveElementMessage":
            Bridge.qForm.put(("removeElement", dictToString(
                {
                    'id': int(data['id'])
                }
            )))
            
        
        if Bridge.fightStarted:
            if name == 'GameFightShowFighterMessage':
                if data['informations']['__type__'] == 'GameFightCharacterInformations' and int(data['informations']['contextualId']) == Bridge.actorId:
                    Bridge.fight['playerCellId'] = int(data['informations']['disposition']['cellId'])
                
                if data['informations']['__type__'] == 'GameFightMonsterInformations':
                    Bridge.fight['monstersCellId'].append({
                        'id': int(data['informations']['contextualId']),
                        'cellId': int(data['informations']['disposition']['cellId'])
                    })

        if name == "CharacterStatsListMessage":
            Bridge.qForm.put(("playerUpdateCharacteristics", dictToString({
                'PA': getPlayerCharacteristic(data, 1),
                'PM': getPlayerCharacteristic(data, 23),
                'PDV':getPlayerCharacteristic(data, 11)
            })))
        
        
        
        if name == "GameEntitiesDispositionMessage":
            for disposition in data['dispositions']:
                if int(disposition['id']) == Bridge.actorId:
                    try:
                        Bridge.qForm.put(('playerUpdateCellId', dictToString({
                            'cellId': int(disposition.get('cellId', 0))
                        })))
                    except Exception as e:
                        print("--- Error 2 :", e)
                    
        if name == "RefreshCharacterStatsMessage":
            if int(data['fighterId']) == Bridge.actorId:

                characteristicsToUpdate = []
                for characteristic in data['stats']['characteristics']['characteristics']:
                    characteristicsToUpdate.append({
                        'type': getCharacteristicType(int(characteristic['characteristicId'])),
                        'value': (int(characteristic.get('base', 0)) + int(characteristic.get('additional', 0)) + int(characteristic.get('objectsAndMountBonus', 0))) - int(characteristic.get('used', 0))
                    })
                Bridge.qForm.put(('playerUpdateCharacteristicsList', dictToString({
                    'characteristics': characteristicsToUpdate
                })))

                print("-------      SETTING playerStatMessage to TRUE |   CASTED SPELL",Bridge.spellCasted )
                Bridge.playerStatMessage = True
                
        
        if name == "GameFightJoinMessage":
            Bridge.inFight = True
            Bridge.fightStarted = True
        
        if name == "GameFightEndMessage":
            Bridge.inFight = False
            Bridge.qForm.put(('fightEnded', ""))
        
        if name == "GameActionFightDeathMessage":
            print("FIGHT DEATH MESSAGE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< - ID :", data['targetId'])
            Bridge.qForm.put(('fightDeathMonster', dictToString({
                'id': int(data['targetId'])
            })))

        if name == "GameActionFightPointsVariationMessage" and Bridge.inFight == True:
            if int(data['targetId']) == Bridge.actorId:
                if Bridge.startMovement and int(data['actionId']) == 129: #PM
                    Bridge.qForm.put(('playerUpdateCellId', dictToString({
                        'cellId': Bridge.movementCellId
                    })))
                    #Bridge.qForm.put(('fightDeplacementFinished', dictToString({})))
                    Bridge.startMovement = False


                if int(data['actionId']) == 129:
                    Bridge.qForm.put(("playerUpdateLossCharacteristic", dictToString({
                        'type': "PM",
                        'delta': int(data['delta']) 
                    })))
                    if Bridge.fightStartMoving:
                        Bridge.fightStartMoving = False
                        Bridge.playerStatMessage = False
                        Bridge.qForm.put(("allActionsFinished", dictToString({})))
                    
                elif int(data['actionId']) == 102:
                    Bridge.qForm.put(("playerUpdateLossCharacteristic", dictToString({
                        'type': "PA",
                        'delta': int(data['delta']) 
                    })))
                    

        if name == "BasicNoOperationMessage":

            if Bridge.startMovement and Bridge.confirmMovement:
                Bridge.qForm.put(('playerUpdateCellId', dictToString({
                    'cellId': Bridge.movementCellId
                })))
                Bridge.startMovement = False
                Bridge.confirmMovement = False

            #--------------------------------------
            if Bridge.inFight:
                if Bridge.fightStarted:
                    Bridge.fightStarted = False
                    Bridge.qForm.put(("fightUpdateMonsterCells", dictToString(Bridge.fight)))
                    Bridge.qForm.put(("fightStarted", dictToString({})))
                    Bridge.resetFightObj()
                

        if name == "GameActionFightSlideMessage":
            if data['targetId'] == Bridge.actorId:
                Bridge.qForm.put(("fightPlayerSlide", dictToString({
                    'cellId': int(data['endCellId'])
                })))
            else:
                Bridge.qForm.put(("fightMonsterSlide", dictToString({
                    'id': int(data['targetId']),
                    'cellId': int(data['endCellId'])
                })))
        if name == "GameFightTurnStartMessage":
            if int(data['id']) == Bridge.actorId:
                Bridge.qForm.put(("fightTurnStart", dictToString({})))
                Bridge.playerStatMessage = False
                Bridge.spellCasted = False

        # if name == "GameActionFightCastRequestMessage":
        #     print('-------- GameActionFightCastRequestMessage Bridge.spellCasted')
        #     Bridge.spellCasted = True
        
        if name == "BasicNoOperationMessage" and Bridge.inFight:
            print("() BasicNoOperationMessage: spellCasted :", Bridge.spellCasted)
            if Bridge.spellCasted == True and Bridge.playerStatMessage == True:
                print("() sending allActionsFinished")
                Bridge.qForm.put(("allActionsFinished", dictToString({})))
                Bridge.playerStatMessage = False
                Bridge.spellCasted = False
        #     if Bridge.spellCasted == True:
        #         Bridge.qForm.put(("allActionsFinished", dictToString({})))
        #         Bridge.spellCasted = False
            
        #     if Bridge.fightStartMoving:
        #         Bridge.fightStartMoving = False
        #         Bridge.qForm.put(("allActionsFinished", dictToString({})))

        



        # GameFightTurnStartMessage

        #  GameActionFightLifePointsLostMessage {'__type__': 'GameActionFightLifePointsLostMessage', 'actionId': 96, 'sourceId': 115831800030.0, 'targetId': -1.0, 'loss': 20, 'permanentDamages': 2, 'elementId': 3}

                    


            






            



class BridgeHandler(ABC):
    """Abstract class for bridging policies.
    You just have to subclass and fill the handle method.
    
    It implements the proxy_callback that will be called
    when a client tries to connect to the server.
    proxy_callback will call `handle` on every packet.

    To modify the behavior, you have to create subclasses pf
    BridgeHandler.
    """

    def __init__(self, coJeu, coSer):
        self.coJeu = coJeu
        self.coSer = coSer
        self.other = {coJeu: coSer, coSer: coJeu}
        self.conns = [coJeu, coSer]

    @abstractmethod
    def handle(self, data, origin):
        pass

    @classmethod
    def proxy_callback(cls, coJeu, coSer):
        """Callback that can be called by the proxy

        It creates an instance of the class and
        calls `handle` on every packet

        coJeu: socket to the game
        coSer: socket to the server
        """
        bridge_handler = cls(coJeu, coSer)
        bridge_handler.loop()

    def loop(self):
        conns = self.conns
        active = True
        print("loop")
        try:
            while active:
                rlist, wlist, xlist = select.select(conns, [], conns)
                if xlist or not rlist:
                    break
                for r in rlist:
                    data = r.recv(8192)
                    if not data:
                        active = False
                        break
                    self.handle(data, origin=r)
        finally:
            for c in conns:
                c.close()


class DummyBridgeHandler(BridgeHandler):
    """Implements a dummy policy
    that forwards all packets"""

    def handle(self, data, origin):
        self.other[origin].sendall(data)


class PrintingBridgeHandler(DummyBridgeHandler):
    """
    Implements a dummy policy that
    forwards and prints all packets
    """

    def handle(self, data, origin):
        super().handle(data, origin)
        print(direction(origin), data.hex())


class MsgBridgeHandler(DummyBridgeHandler, ABC):
    """
    Advanced policy to work with the parsed messages
    instead of the raw packets like BridgeHandler.
    
    This class implements a generic `handle` that calls 
    `handle_message` which acts on the parsed messages
    and that should be implemented by the subclasses.
    """

    def __init__(self, coJeu, coSer):
        super().__init__(coJeu, coSer)
        self.buf = {coJeu: Buffer(), coSer: Buffer()}

    def handle(self, data, origin):

        super().handle(data, origin)
        self.buf[origin] += data
        from_client = origin == self.coJeu
        # print(direction(origin), self.buf[origin].data)
        msg = Msg.fromRaw(self.buf[origin], from_client)
        while msg is not None:
            msgType = protocol.msg_from_id[msg.id]
            parsedMsg = protocol.read(msgType, msg.data)

            assert msg.data.remaining() == 0, (
                "All content of %s have not been read into %s:\n %s"
                % (msgType, parsedMsg, msg.data)
            )
            print("message ---")
            print(parsedMsg)
            self.handle_message(parsedMsg, origin)
            msg = Msg.fromRaw(self.buf[origin], from_client)

    @abstractmethod
    def handle_message(self, msg, origin):
        pass


class PrintingMsgBridgeHandler(MsgBridgeHandler):
    def handle_message(self, msg, origin):
        print(direction(origin))
        print(msg)
        print()
        print()


class InjectorBridgeHandler(BridgeHandler):
    """Forwards all packets and allows to inject
    packets
    """

    def __init__(self, coJeu, coSer, db_size=100, dumper=None, qForm=None, qSocket=None):
        super().__init__(coJeu, coSer)
        self.buf = {coJeu: Buffer(), coSer: Buffer()}
        self.injected_to_client = 0
        self.injected_to_server = 0
        self.counter = 0
        self.db = deque([], maxlen=db_size)
        self.dumper = dumper
        self.qForm = qForm
        self.qSocket = qSocket
        self.waiting = False
        self.actorId = 1
        self.fightStartMoving = False

        self.movementCellId = 0
        self.startMovement = False
        self.waitingName = ""

        self.confirmMovement = False

        self.fightStarted = False
        self.fightPreparing = False
        self.fight = {
            "playerCellId": 0,
            "monstersCellId": []
        }

        self.spellCasted = False

        self.inFight = False
        self.zaap = {'elementId': 0, 'skillInstanceUid': 0}

        self.playerStatMessage = False
        self.logActivated = False
        self.parsedLogActivated = False

        self.callbackMessage = None

        self.initialized = False
        self.blackList = ['EmotePlayMessage', 'AchievementListMessage', 'ChatServerMessage', 'PrismsListMessage', 'FollowedQuestsMessage', 'QuestListMessage', 'AnomalySubareaInformationResponseMessage', 'ChatServerWithObjectMessage', 'GuildGetInformationsMessage', 'GameContextRefreshEntityLookMessage', 'SetCharacterRestrictionsMessage', 'GameRolePlayShowActorMessage']
        self.whitelist = ['GameFightPlacementPositionRequestMessage', 'GameFightTurnFinishMessage']
        self.socketON = True
        self.lock = threading.Lock()
        self.packetThread = threading.Thread(target=self.queueHandle, args=())
        self.packetThread.start()

    def resetFightObj(self):
        self.fight = {
            "playerCellId": 0,
            "monstersCellId": []
        }
    
    
    def queueHandle(self):
        self.socketON = True
        while self.socketON:
            time.sleep(50/1000)
            if not self.qSocket.empty():
                #self.socketON = False
                action, infos = self.qSocket.get()

                print("------- MESSAGE : " + str(action)  + " - data: " + str(infos))
                if action == "sendMessage":
                    self.send_socket(infos)


    def send_to_client(self, data):
        if isinstance(data, Msg):
            data = data.bytes()
        self.injected_to_client += 1
        self.coJeu.sendall(data)

    def send_to_server(self, data):
        if isinstance(data, Msg):
            data.count = self.counter + 1
            data = data.bytes()
        self.injected_to_server += 1
        with self.lock:
            self.coSer.sendall(data)

    

    def send_socket(self, infos):

        data = {}
        if infos != "":
            data = json.loads(infos)
        #self.packetThread.join()
        messageName = data['messageName']
        extraData = data['data']

        print("() Method send_socket()", messageName, extraData)
        msg = Msg.from_json(
            {"__type__": messageName, **extraData}
        )
        try:
            self.send_to_server(msg)
            if messageName == "GameActionFightCastRequestMessage":
                self.spellCasted = True
        except:
            print("FAILED : on reesssait ")
            self.qSocket.put(("sendMessage", infos))

    def set_fight_ready(self):
        msg = Msg.from_json(
            {"__type__": "GameFightReadyMessage", "isReady": True}
        )
        try:
            self.send_to_server(msg)
        except:
            print("FAILED : on reesssait ")
            self.qSocket.put(("fightSetReady", ""))

    def handle(self, data, origin):
        self.buf[origin] += data
        from_client = origin == self.coJeu

        msg = Msg.fromRaw(self.buf[origin], from_client)

        while msg is not None:
            msgType = protocol.msg_from_id[msg.id]
            parsedMsg = protocol.read(msgType, msg.data)

            # print(">>>>> waiting callback :", self.callbackMessage)
            # if self.callbackMessage != None:
            #     if protocol.msg_from_id[msg.id]["name"] == self.callbackMessage:
            #         self.qForm.put(('callback', ''))

            assert msg.data.remaining() in [0, 48], (
                "All content of %s have not been read into %s:\n %s"
                % (msgType, parsedMsg, msg.data)
            )

            # if protocol.msg_from_id[msg.id]["name"] not in self.blackList:
            #     if from_client:
            #         logger.info(
            #             ("-- SENT - [%(count)i] %(name)s (%(size)i Bytes)"),
            #             dict(
            #                 count=msg.count,
            #                 name=protocol.msg_from_id[msg.id]["name"],
            #                 size=len(msg.data),
            #             ),
            #         )
            #     else:
            #         logger.info(
            #             ("RECV - %(name)s (%(size)i Bytes)"),
            #             dict(name=protocol.msg_from_id[msg.id]["name"], size=len(msg.data)),
            #         )
                
            #     print(parsedMsg)
            #     print()

            handleMessage(self, protocol.msg_from_id[msg.id]["name"], parsedMsg)

            if from_client:
                msg.count += self.injected_to_server - self.injected_to_client
                self.counter = msg.count
            else:
                self.counter += 1
            self.db.append(msg)
            if self.dumper is not None:
                self.dumper.dump(msg)
            self.other[origin].sendall(msg.bytes())

            self.handle_message(parsedMsg, origin)
            msg = Msg.fromRaw(self.buf[origin], from_client)

            time.sleep(0.005)

    def handle_message(self, m, o):
        pass
