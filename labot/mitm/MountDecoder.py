


class MountDecoder:

    def getMountsToLevelUp(data):
        print("todo")

        mountsToLevelUp = []

        allMounts = data['stabledMountsDescription']

        for mount in allMounts:
            level = mount['level']
            love = mount['love']
            maturity = mount['maturity']
            maturityForAdult = mount['maturityForAdult']
            stamina = mount['stamina']

            if level < 5 and love >= 7500 and maturity == maturityForAdult and stamina >= 7500:
                mountsToLevelUp.append({
                    'id': mount['id']
                })
        
        return mountsToLevelUp
