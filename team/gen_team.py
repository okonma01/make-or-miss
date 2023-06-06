import names

from player.gen_player import gen_player
from team.index import TeamGameSim


def gen_team() -> TeamGameSim:
    t = TeamGameSim()
    teamName = names.get_last_name()
    if teamName[-1] == 'z':
        pass
    if teamName[-2:] == 'ch' or teamName[-2:] == 'sh':
        teamName += 'es'
    elif teamName[-1] != 's':
        teamName += 's'
    if teamName[:2] == 'Mc':
        teamName = teamName[:2] + teamName[2:].title()
    teamName = 'Los ' + teamName
    t._name = teamName
    t._players = [gen_player(x//3 + 1) for x in range(15)]
    t.set_lineup()
    return t