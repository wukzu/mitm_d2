import json

import threading

# dicta = {
#   "__type__": "MapComplementaryInformationsDataMessage",
#   "subAreaId": 30,
#   "mapId": 120061956.0,
#   "houses": [],
#   "actors": [
#     {
#       "__type__": "GameRolePlayCharacterInformations",
#       "contextualId": 115831800030.0,
#       "disposition": {
#         "__type__": "EntityDispositionInformations",
#         "cellId": 20,
#         "direction": 2
#       },
#       "look": {
#         "__type__": "EntityLook",
#         "bonesId": 1,
#         "skins": [
#           91,
#           2149,
#           3021,
#           3357,
#           3841,
#           970
#         ],
#         "indexedColors": [
#           33538919,
#           33554432,
#           50866292,
#           67108864,
#           83886080
#         ],
#         "scales": [
#           135
#         ],
#         "subentities": []
#       },
#       "name": "Lorienta",
#       "humanoidInfo": {
#         "__type__": "HumanInformations",
#         "restrictions": {
#           "__type__": "ActorRestrictionsInformations",
#           "cantBeAggressed": False,
#           "cantBeChallenged": False,
#           "cantTrade": False,
#           "cantBeAttackedByMutant": False,
#           "cantRun": False,
#           "forceSlowWalk": False,
#           "cantMinimize": False,
#           "cantMove": False,
#           "cantAggress": False,
#           "cantChallenge": False,
#           "cantExchange": False,
#           "cantAttack": True,
#           "cantChat": False,
#           "cantBeMerchant": False,
#           "cantUseObject": False,
#           "cantUseTaxCollector": False,
#           "cantUseInteractive": False,
#           "cantSpeakToNPC": False,
#           "cantChangeZone": False,
#           "cantAttackMonster": False
#         },
#         "sex": True,
#         "options": [
#           {
#             "__type__": "HumanOptionTitle",
#             "titleId": 79,
#             "titleParam": ""
#           },
#           {
#             "__type__": "HumanOptionOrnament",
#             "ornamentId": 99,
#             "level": 184,
#             "leagueId": 65535,
#             "ladderPosition": -1
#           },
#           {
#             "__type__": "HumanOptionSpeedMultiplier",
#             "speedMultiplier": 1
#           }
#         ]
#       },
#       "accountId": 39286155,
#       "alignmentInfos": {
#         "__type__": "ActorAlignmentInformations",
#         "alignmentSide": 0,
#         "alignmentValue": 0,
#         "alignmentGrade": 0,
#         "characterPower": 115831800214.0
#       }
#     },
#     {
#       "__type__": "GameRolePlayGroupMonsterInformations",
#       "contextualId": -20005.0,
#       "disposition": {
#         "__type__": "EntityDispositionInformations",
#         "cellId": 410,
#         "direction": 1
#       },
#       "look": {
#         "__type__": "EntityLook",
#         "bonesId": 567,
#         "skins": [],
#         "indexedColors": [],
#         "scales": [],
#         "subentities": []
#       },
#       "keyRingBonus": False,
#       "hasHardcoreDrop": False,
#       "hasAVARewardToken": False,
#       "staticInfos": {
#         "__type__": "GroupMonsterStaticInformations",
#         "mainCreatureLightInfos": {
#           "__type__": "MonsterInGroupLightInformations",
#           "genericId": 134,
#           "grade": 4,
#           "level": 28
#         },
#         "underlings": []
#       },
#       "lootShare": -1,
#       "alignmentSide": -1
#     },
#     {
#       "__type__": "GameRolePlayGroupMonsterInformations",
#       "contextualId": -20007.0,
#       "disposition": {
#         "__type__": "EntityDispositionInformations",
#         "cellId": 256,
#         "direction": 5
#       },
#       "look": {
#         "__type__": "EntityLook",
#         "bonesId": 647,
#         "skins": [],
#         "indexedColors": [],
#         "scales": [],
#         "subentities": []
#       },
#       "keyRingBonus": False,
#       "hasHardcoreDrop": False,
#       "hasAVARewardToken": False,
#       "staticInfos": {
#         "__type__": "GroupMonsterStaticInformations",
#         "mainCreatureLightInfos": {
#           "__type__": "MonsterInGroupLightInformations",
#           "genericId": 793,
#           "grade": 2,
#           "level": 24
#         },
#         "underlings": [
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 793,
#             "grade": 3,
#             "level": 26,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 647,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 148,
#             "grade": 4,
#             "level": 28,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 570,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 149,
#             "grade": 1,
#             "level": 22,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 568,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 134,
#             "grade": 2,
#             "level": 24,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 567,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 149,
#             "grade": 2,
#             "level": 24,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 568,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 149,
#             "grade": 3,
#             "level": 26,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 568,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [],
#               "subentities": []
#             }
#           },
#           {
#             "__type__": "MonsterInGroupInformations",
#             "genericId": 101,
#             "grade": 1,
#             "level": 22,
#             "look": {
#               "__type__": "EntityLook",
#               "bonesId": 563,
#               "skins": [],
#               "indexedColors": [],
#               "scales": [
#                 105
#               ],
#               "subentities": []
#             }
#           }
#         ]
#       },
#       "lootShare": -1,
#       "alignmentSide": -1
#     }
#   ],
#   "interactiveElements": [
#     {
#       "__type__": "InteractiveElementWithAgeBonus",
#       "elementId": 495693,
#       "elementTypeId": 254,
#       "enabledSkills": [
#         {
#           "__type__": "InteractiveElementSkill",
#           "skillId": 68,
#           "skillInstanceUid": 146399379
#         }
#       ],
#       "disabledSkills": [],
#       "onCurrentMap": True,
#       "ageBonus": 0
#     },
#     {
#       "__type__": "InteractiveElementWithAgeBonus",
#       "elementId": 483723,
#       "elementTypeId": 33,
#       "enabledSkills": [],
#       "disabledSkills": [
#         {
#           "__type__": "InteractiveElementSkill",
#           "skillId": 39,
#           "skillInstanceUid": 146399381
#         }
#       ],
#       "onCurrentMap": True,
#       "ageBonus": 2
#     },
#     {
#       "__type__": "InteractiveElement",
#       "elementId": 483722,
#       "elementTypeId": 31,
#       "enabledSkills": [],
#       "disabledSkills": [
#         {
#           "__type__": "InteractiveElementSkill",
#           "skillId": 37,
#           "skillInstanceUid": 146399380
#         }
#       ],
#       "onCurrentMap": True
#     },
#     {
#       "__type__": "InteractiveElementWithAgeBonus",
#       "elementId": 483680,
#       "elementTypeId": 67,
#       "enabledSkills": [
#         {
#           "__type__": "InteractiveElementSkill",
#           "skillId": 71,
#           "skillInstanceUid": 146399760
#         }
#       ],
#       "disabledSkills": [],
#       "onCurrentMap": False,
#       "ageBonus": 12
#     },
#     {
#       "__type__": "InteractiveElement",
#       "elementId": 483898,
#       "elementTypeId": -1,
#       "enabledSkills": [
#         {
#           "__type__": "InteractiveElementSkill",
#           "skillId": 198,
#           "skillInstanceUid": 146400303
#         }
#       ],
#       "disabledSkills": [],
#       "onCurrentMap": False
#     }
#   ],
#   "statedElements": [
#     {
#       "__type__": "StatedElement",
#       "elementId": 495693,
#       "elementCellId": 230,
#       "elementState": 0,
#       "onCurrentMap": True
#     },
#     {
#       "__type__": "StatedElement",
#       "elementId": 483723,
#       "elementCellId": 529,
#       "elementState": 0,
#       "onCurrentMap": True
#     },
#     {
#       "__type__": "StatedElement",
#       "elementId": 483722,
#       "elementCellId": 491,
#       "elementState": 1,
#       "onCurrentMap": True
#     },
#     {
#       "__type__": "StatedElement",
#       "elementId": 483680,
#       "elementCellId": 82,
#       "elementState": 0,
#       "onCurrentMap": False
#     }
#   ],
#   "obstacles": [],
#   "fights": [],
#   "hasAggressiveMonsters": True,
#   "fightStartPositions": {
#     "__type__": "FightStartingPositions",
#     "positionsForChallengers": [
#       87,
#       100,
#       101,
#       116,
#       127,
#       130,
#       141,
#       144,
#       155,
#       170,
#       171,
#       184
#     ],
#     "positionsForDefenders": [
#       360,
#       374,
#       375,
#       388,
#       414,
#       428,
#       429,
#       442,
#       468,
#       482,
#       483,
#       496
#     ]
#   }
# }

# # print(a)
# # print(type(a))

# # i = json.dumps(a)

# # print(i)
# # print(type(i))


# # my_dict = json.loads(i) 

# data = {'__type__': 'GameMapMovementMessage', 'keyMovements': [383, 343], 'forcedDirection': 1, 'actorId': -20005.0}

# MonsterGroups = []

# for x in dicta['actors']:
#     if x['__type__'] == 'GameRolePlayGroupMonsterInformations':
#         groupId = x['contextualId']
#         cellId = x['disposition']['cellId']
#         monsters = []
#         for m in x['staticInfos']['underlings']:
#             monsters.append({
#                 'id': m['genericId'],
#                 'level': m['level']
#             })
#         info = x['staticInfos']['mainCreatureLightInfos']
#         monsters.append({
#             'id': info['genericId'],
#             'level': info['level']
#         })
        
#         MonsterGroups.append({
#             'groupId': int(groupId),
#             'cellId': int(cellId),
#             'monsters': monsters
#         })


# newList = [x for x in MonsterGroups if x['groupId'] != -20005]

# for elem in MonsterGroups:
#     if elem['groupId'] == -20007:
#         elem['cellId'] = 999

# print(MonsterGroups)
# print('-------')
# print(newList)

import time

class Test():
  def __init__(self):
    self.packetThread = threading.Thread(target=self.test, args=())
    self.packetThread.start()

  def stop(self):
    self.packetThread.join()
    print("OK")
    self.packetThread = threading.Thread(target=self.test, args=())
    self.packetThread.start()
  def test(self):
    a = True
    count = 0
    while a:
      print("hello")
      time.sleep(1)
      count += 1
      if count == 3:
        threading.Thread(target=self.stop).start()
        break
      
      if count == 6:
        threading.Thread(target=self.stop).start()
        break
        a = False
      if count == 10:
        a = False


test = Test()

print("main ")
