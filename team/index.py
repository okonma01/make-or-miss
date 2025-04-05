from typing import List
from player.position import Position
from player.overall import fatigue_adj_ovr, overall
from player.index import PlayerGameSim, pos_dict
from team.stat import TeamStat
from team.util import get_best_at_position, get_pos_depths
from util.helpers import generate_id

# changed team stat mp to float type - DONE
# commented out pos and opp_pos in team stat - DONE

# change team stat mp back to int type (for seconds) - DONE
# remove trb from team stat.py
# add asta to team stat.py

class TeamGameSim():
    count = 0
    depth_dict = {Position.G:  3,  # g + gf
                  Position.GF: 3,  # g + gf
                  Position.F:  4,  # gf + f
                  Position.FC: 3,  # f + fc
                  Position.C:  3}  # fc + c

    def __init__(self) -> None:
        self._id: str = generate_id(self)
        TeamGameSim.count += 1
        self._name: str = str()
        self._abbreviation: str = str()
        self._season: str = str()
        self._coach: str = str()
        self._record: str = str()
        self._arena: str = str()
        self._players: List[PlayerGameSim] = list()
        self._lineup: List[PlayerGameSim] = list()
        self._bench: List[PlayerGameSim] = list()
        self._stat: TeamStat = TeamStat()

    def clear_stat(self) -> None:
        for s in self._stat.__dict__:
            self._stat.__dict__[s] = 0

    def set_lineup(self) -> None:
        sorted_list = []
        player_set = set()
        for i in range(1, 6):
            player_set = set(self._players) - set(sorted_list)
            sorted_list.append(get_best_at_position(i, player_set))

        depths = {pos: 0 for pos in Position}
        for pos in Position:
            depths[pos] = get_pos_depths(pos, sorted_list)
            while depths[pos] < TeamGameSim.depth_dict[pos]:
                player_set = set(self._players) - set(sorted_list)
                nth_man = get_best_at_position(pos.value, player_set)
                if (nth_man):
                    sorted_list.append(nth_man)
                    depths[pos] += 1
                else:
                    break

        self._lineup = sorted_list[:5]
        self._bench = sorted_list[5:]

    def print_roster(self, x: int = 0, fatigue: bool = False) -> List:
        if fatigue:
            if x == 0:
                return [p._pos.name + ' ' + str(fatigue_adj_ovr(p, p._pos.value)) for p in self._lineup]
            else:
                return [p._pos.name + ' ' + str(fatigue_adj_ovr(p, p._pos.value)) for p in self._bench]
        else:
            if x == 0:
                return [p._pos.name + ' ' + str(overall(p, p._pos)) for p in self._lineup]
            else:
                return [p._pos.name + ' ' + str(overall(p, p._pos)) for p in self._bench]
