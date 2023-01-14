
import json

class Socket:
    
    def EnterHavenBag(playerId):
        return ("sendMessage", json.dumps({
            'messageName': 'EnterHavenBagRequestMessage',
            'data': {
                'havenBagOwner': playerId
            }
        }))

    def useHavenbagZaap(zaap):
        return ("sendMessage", json.dumps({
            'messageName': 'InteractiveUseRequestMessage',
            'data': {
                'elemId': zaap['elementId'],
                'skillInstanceUid': zaap['skillInstanceUid']
            }
        }))
    
    def teleportBrakmar():
        return ("sendMessage", json.dumps({
            'messageName': 'TeleportRequestMessage',
            'data': {
                'sourceType': 3, 
                'destinationType': 0, 
                'mapId': 212861955.0
            }
        }))

    def teleportAnimals():
        return ("sendMessage", json.dumps({
            'messageName': 'TeleportRequestMessage',
            'data': {
                'sourceType': 1, 
                'destinationType': 1, 
                'mapId': 212862469.0
            }
        }))

    def useSpell(spellId, cellId):
        return ("sendMessage", json.dumps({
            'messageName': 'GameActionFightCastRequestMessage',
            'data': {
                'spellId': spellId,
                'cellId': cellId
            }
        }))
    
    def setFightReady():
        return ("sendMessage", json.dumps({
            'messageName': 'GameFightReadyMessage',
            'data': {
                'isReady': True
            }
        }))
    
    def fightPassTurn(): 
        return ("sendMessage", json.dumps({
            'messageName': 'GameFightTurnFinishMessage',
            'data': {
                'isAfk': False
            }
        }))
    
    def rideMount(mountId):
        return ("sendMessage", json.dumps({
            'messageName': 'ExchangeHandleMountsMessage',
            'data': {
                'actionType': 2,
                'ridesId': [mountId]
            }
        }))
    
    def rideMountOnPlayer():
        return ("sendMessage", json.dumps({
            'messageName': 'MountToggleRidingRequestMessage',
            'data': {}
        }))
    
    def mountSetXpRatio(ratio): 
        return ("sendMessage", json.dumps({
            'messageName': 'MountSetXpRatioRequestMessage',
            'data': {
                'xpRatio': 90
            }
        }))
    
    def mountMovePaddockToStable(mountsId): 
        return ("sendMessage", json.dumps({
            'messageName': 'ExchangeHandleMountsMessage',
            'data': {
                'actionType': 7,
                'ridesId': mountsId
            }
        }))
    
    def mountMoveStableToPaddock(mountsId): 
        return ("sendMessage", json.dumps({
            'messageName': 'ExchangeHandleMountsMessage',
            'data': {
                'actionType': 6,
                'ridesId': mountsId
            }
        }))

    def moveToCellId(path, mapId):
        return ("sendMessage", json.dumps({
            'messageName': 'GameMapMovementRequestMessage',
            'data': {
                'keyMovements': path,
                'mapId': mapId
            }
        }))
    
    def attackMonster(monsterId):
        return ("sendMessage", json.dumps({
            'messageName': 'GameRolePlayAttackMonsterRequestMessage',
            'data': {
                'monsterGroupId': monsterId
            }
        }))
        
    
    def offLogs():
        return ("offLogs", "")
    
    def onLogs():
        return ("onLogs", "")

    print("----------- end callback")


