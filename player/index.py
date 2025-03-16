# from .badge import Badge
from player.overall import overall
from player.position import Position
from player.rating import Rating, get_ratings
from player.stat import PlayerStat
# from .tendency import Tendency
from util.helpers import height_in_feet, generate_id

# changed player's court_time and bench_time to int type
# changed player's gp to g
# commented out player's pos
# ovr method in does not actually use pos parameter - it only uses self._pos

pos_dict = {1: [Position.G],
            2: [Position.G, Position.GF],
            3: [Position.GF, Position.F],
            4: [Position.F, Position.FC, Position.C],
            5: [Position.FC, Position.C]}


class PlayerGameSim():
    count = 0
    def __init__(self) -> None:
        # global count
        self._id = generate_id(self)
        PlayerGameSim.count += 1
        self._name = str()
        self._jersey_no = int()
        self._height_in_inches = int()
        self._archetype = str()
        self._pos = Position.G
        self._stat = PlayerStat()
        self._rating = Rating()
        # self._badges = Badge()
        # self._tendency = Tendency()
        self._injured = bool(None)

    def get_info(self) -> None:
        print('PLAYER NAME: ', self._name, '\n')
        print('PLAYER HEIGHT: ', height_in_feet(self._height_in_inches), '\n')
        print('PLAYER POSITION: ', self._pos, '\n')
        print('PLAYER RATINGS: ', get_ratings(self._rating), '\n')
        print('PLAYER OVR: coming soon...')

    def rating(self, attr) -> int:
        if attr in self._rating.composite.__dict__:
            return self._rating.composite.__dict__[attr]
        if attr not in self._rating.__dict__:
            return -1
        return self._rating.__dict__[attr]

    def clear_stat(self) -> None:
        for s in self._stat.__dict__:
            if s == 'energy':
                self._stat.__dict__[s] = 100
            else:
                self._stat.__dict__[s] = 0

    def stat(self, s):
        if s not in self._stat.__dict__:
            return -1
        return self._stat.__dict__[s]

    def ovr(self, pos: int = None) -> int:
        if pos is None:
            pos = self._pos.value
        if self._pos not in pos_dict[pos]:
            return -1
        return overall(self, self._pos)
