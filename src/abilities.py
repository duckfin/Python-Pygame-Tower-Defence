from localdefs import *

abilitypricedict = {'Regen I':50,
                    'Regen II':100,
                    'Interest I':50,
                    'Interest II':100,
                    'Interest III':200}

def getAbility(type):
    if type=='Regen I':
        player.addHpt(0.25)
    elif type=='Regen II':
        player.addHpt(0.25)
    elif type=='Interest I':
        player.addInterest(0.05)
    elif type=='Interest II':
        player.addInterest(0.05)
    elif type=='Interest III':
        player.addInterest(0.05)
    else:
        return
    player.abilities.append(type)