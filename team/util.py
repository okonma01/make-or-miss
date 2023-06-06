from typing import List
from player.index import PlayerGameSim, pos_dict
from player.position import Position

def sort_team(players: List[PlayerGameSim], depth: int) -> List[PlayerGameSim]:
    sorted_list = []
    for i in range(1, 6):
        player_set = set(players) - set(sorted_list)
        sorted_list.append(get_best_at_position(i, player_set))
    
    for i in range(1, depth-4):
        player_set = set(players) - set(sorted_list)
        sorted_list.append(get_best_at_position(i, player_set))

    return sorted_list

def get_pos_depths(pos: Position, l: List[PlayerGameSim] = list()) -> int:
        if l == []:
            return 0
        depth = 0
        for player in l:
            if player._pos in pos_dict[pos.value]:
                depth += 1
        return depth

def get_best_at_position(i: int, pool: List, sub: bool = False) -> PlayerGameSim:
    if len(pool) == 0:
        return None
        
    # first filter out injured players
    pool = [p for p in pool if not p._injured]

    # sub = True (for subs) or False (for starters)
    if sub:
        pool = [p for p in pool if p.stat('bench_time') > 0]
    best = sorted(pool, key= lambda p: p.ovr(i), reverse=True)[0]
    if best.ovr(i) == -1:
        return None
    return best
