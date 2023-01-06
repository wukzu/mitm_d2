

import json


def buildMountInfos(mount, place = 's'):
    return {
        'id': int(mount['id']),
        'level': mount['level'],
        'love': mount['love'],
        'maturity': mount['maturity'],
        'maturityForAdult': mount['maturityForAdult'],
        'stamina': mount['stamina'],
        'serenity': mount['serenity'],
        'sex': mount['sex'],
        'place': place
    }

class MountDecoder:

    def getMounts(data):
        print("todo")

        stabledMounts = data['stabledMountsDescription']
        paddockedMounts = []
        try:
            paddockedMounts = data['paddockedMountsDescription']
        except KeyError:
            paddockedMounts = []

        mounts = []

        for mount in stabledMounts:
            mounts.append(buildMountInfos(mount, 's'))
            
        for mount in paddockedMounts:
            mounts.append(buildMountInfos(mount, 'p'))
        
        return {
            'mounts': mounts
        }

    def getMountBoostChanged(data):
        mountId = int(data['rideId'])

        boostList = data['boostToUpdateList']
        finalBoostList = []

        for boost in boostList:
            finalBoostList.append({
                'type': boost['type'],
                'value': boost['value']
            })
        
        return {
            'mountId': mountId,
            'boostList': finalBoostList
        }
    
    def getMountsAddedPaddock(data):
        mountsAdded = []

        for mount in data['mountDescription']:
            mountsAdded.append(buildMountInfos(mount, 'p'))
        
        return {
            'mountsAdded': mountsAdded
        }
    

    def getMountsAddedStable(data):
        mountsAdded = []

        for mount in data['mountDescription']:
            mountsAdded.append(buildMountInfos(mount, 's'))
        
        return {
            'mountsAdded': mountsAdded
        }
    
            
