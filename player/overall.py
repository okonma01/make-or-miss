# from dataclasses import dataclass
# from player.index import PlayerGameSim
from math import inf
from player.position import Position
from util.helpers import weights


weight_dict = dict()
weight_dict['G'] = weight_dict['g'] = [['spd', 'pss', 'mid', 'ins', 'diq', 'jmp', 'reb', 'ft', 'hndl', 'tp'],
                                       weights(n=10, sum=100, delta=0.9)]

weight_dict['GF'] = weight_dict['gf'] = [['pss', 'spd', 'ins', 'mid', 'tp', 'diq', 'oiq', 'reb', 'jmp', 'ft'],
                                         weights(n=10, sum=100, delta=0.7)]

weight_dict['F'] = weight_dict['f'] = [['hgt', 'mid', 'diq', 'jmp', 'ins', 'spd', 'oiq', 'tp'],
                                       [30] + weights(n=7, sum=70, delta=1.3)]

weight_dict['FC'] = weight_dict['fc'] = [['hgt', 'reb', 'ins', 'jmp', 'stre', 'diq', 'oiq', 'stam'],
                                         [38] + weights(n=7, sum=62, delta=0.7)]

weight_dict['C'] = weight_dict['c'] = [['hgt', 'diq', 'reb', 'ins', 'jmp', 'stre'],
                                         [26] + weights(n=5, sum=74, delta=1.1)]

def overall(p, pos: Position) -> int:
    ovr = 0
    pos = pos.name
    for i in range(len(weight_dict[pos][0])):
        attr = weight_dict[pos][0][i]
        wgt  = weight_dict[pos][1][i] / 100
        ovr += round(p.rating(attr)*wgt, 4)
    return int(round(ovr, 0))

def fatigue_adj_ovr(p, pos: int) -> int:
    if not p:
        return inf
    ovr = p.ovr(pos)
    if ovr == -1:
        return -1
    return int((p.stat('energy')/100) * ovr)