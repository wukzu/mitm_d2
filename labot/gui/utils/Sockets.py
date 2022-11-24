
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
    
    