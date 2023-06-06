from dataclasses import dataclass
from player.composite_rating import CompositeRating


@dataclass
class Rating():
    hgt: int = 0
    stre: int = 0
    stam: int = 0
    spd: int = 0
    jmp: int = 0
    ins: int = 0
    mid: int = 0
    tp: int = 0
    ft: int = 0
    pss: int = 0
    hndl: int = 0
    # stl: int = 0
    # blk: int = 0
    reb: int = 0
    oiq: int = 0
    diq: int = 0
    dur: int = 0

    def __init__(self) -> None:
        self.composite: CompositeRating = CompositeRating()

    def get(self, attr: str) -> int:
        return self.__dict__[attr]

    def update_composite(self) -> None:
        self.composite = CompositeRating()
        self.composite.compose(self)


raw_rating = Rating()
raw_rating.stre = 37
raw_rating.stam = 57
raw_rating.spd = 40
raw_rating.jmp = 40
raw_rating.ins = 27
raw_rating.mid = 32
raw_rating.tp = 32
raw_rating.ft = 32
raw_rating.pss = 37
raw_rating.hndl = 37
raw_rating.reb = 37
raw_rating.oiq = 32
raw_rating.diq = 32
raw_rating.dur = 70


@dataclass
class TypeFactor():
    factors = dict()
    factors['G'] = {'spd':  1.05,
                    'ft':   1.1,
                    'hndl': 1.05,
                    'oiq':  1.05}

    factors['GF'] = {'ft':   1.05,
                     'mid':  1.05,
                     'hndl': 1.05,
                     'oiq':  1.05}

    factors['F'] = {'jmp':  1.05,
                    'diq':   1.05}

    factors['FC'] = {'reb':  1.05,
                     'diq':  1.05}

    factors['C'] = {'stre': 1.05,
                    'ins':  1.05,
                    'ft':   0.95,
                    'reb':  1.05,
                    'diq':  1.05}


def get_ratings(r: Rating) -> str:
    result = ''
    for i in range(1):
        result = '\nATHLETICISM:\n'
        result += 'Strength: ' + str(r.stre) + '\n'
        result += 'Stamina: ' + str(r.stam) + '\n'
        result += 'Speed: ' + str(r.spd) + '\n'
        result += 'Jumping: ' + str(r.jmp) + '\n'
        result += 'Durability: ' + str(r.dur) + '\n'
        result += '\nOFFENSE:\n'
        result += 'Inside shot: ' + str(r.ins) + '\n'
        result += 'Mid range: ' + str(r.mid) + '\n'
        result += 'Three point: ' + str(r.tp) + '\n'
        result += 'Free throw: ' + str(r.ft) + '\n'
        result += 'Passing: ' + str(r.pss) + '\n'
        result += 'Ball handle: ' + str(r.hndl) + '\n'
        result += '\nDEFENSE:\n'
        result += 'Rebound: ' + str(r.reb) + '\n'
        # result += 'Block: ' + str(r.blk) + '\n'
        result += '\nIQ:' + '\n'
        result += 'Offensive IQ: ' + str(r.oiq) + '\n'
        result += 'Defensive IQ: ' + str(r.diq) + '\n'
    return result

# now, we will use a different method to generate ratings
# we will still have gauss, but we will have different "raw_rating" based on different archetypes
# our archetypes:
#   - shooting specialist
#   - 3 and D wing
#   - pass first playmaker
#   - slasher
#   - perimeter defender
#   - rebounding specialist
#   - rolling big
#   - playmaking big
#   - stretch big
#   - rim protector

# we will have a different raw_rating for each archetype


def gen_raw_rating(archetype: str) -> Rating:
    raw_rating = Rating()
    # stamina for all archetypes is 75
    # durability for all archetypes is 70
    raw_rating.stam = 75
    raw_rating.dur = 70
    if archetype == 'shooting specialist':
        raw_rating.spd = 65
        raw_rating.stre = 40
        raw_rating.jmp = 55
        raw_rating.ins = 60
        raw_rating.mid = 75
        raw_rating.tp = 80
        raw_rating.ft = 80
        raw_rating.pss = 55
        raw_rating.hndl = 60
        raw_rating.reb = 50
        raw_rating.oiq = 55
        raw_rating.diq = 40
    elif archetype == '3 and D wing':
        raw_rating.spd = 75
        raw_rating.stre = 55
        raw_rating.jmp = 65
        raw_rating.ins = 50
        raw_rating.mid = 45
        raw_rating.tp = 70
        raw_rating.ft = 60
        raw_rating.pss = 50
        raw_rating.hndl = 55
        raw_rating.reb = 65
        raw_rating.oiq = 60
        raw_rating.diq = 75
    elif archetype == 'pass first playmaker':
        raw_rating.spd = 65
        raw_rating.stre = 45
        raw_rating.jmp = 50
        raw_rating.ins = 55
        raw_rating.mid = 55
        raw_rating.tp = 50
        raw_rating.ft = 70
        raw_rating.pss = 80
        raw_rating.hndl = 75
        raw_rating.reb = 40
        raw_rating.oiq = 75
        raw_rating.diq = 45
    elif archetype == 'slasher':
        raw_rating.spd = 80
        raw_rating.stre = 40
        raw_rating.jmp = 75
        raw_rating.ins = 75
        raw_rating.mid = 60
        raw_rating.tp = 50
        raw_rating.ft = 65
        raw_rating.pss = 55
        raw_rating.hndl = 70
        raw_rating.reb = 40
        raw_rating.oiq = 60
        raw_rating.diq = 40
    elif archetype == 'perimeter defender':
        raw_rating.spd = 75
        raw_rating.stre = 65
        raw_rating.jmp = 65
        raw_rating.ins = 55
        raw_rating.mid = 45
        raw_rating.tp = 45
        raw_rating.ft = 60
        raw_rating.pss = 50
        raw_rating.hndl = 55
        raw_rating.reb = 65
        raw_rating.oiq = 45
        raw_rating.diq = 80
    elif archetype == 'rebounding specialist':
        raw_rating.spd = 60
        raw_rating.stre = 65
        raw_rating.jmp = 75
        raw_rating.ins = 55
        raw_rating.mid = 45
        raw_rating.tp = 45
        raw_rating.ft = 60
        raw_rating.pss = 45
        raw_rating.hndl = 50
        raw_rating.reb = 85
        raw_rating.oiq = 45
        raw_rating.diq = 70
    elif archetype == 'rolling big':
        raw_rating.spd = 50
        raw_rating.stre = 75
        raw_rating.jmp = 65
        raw_rating.ins = 75
        raw_rating.mid = 55
        raw_rating.tp = 40
        raw_rating.ft = 45
        raw_rating.pss = 40
        raw_rating.hndl = 40
        raw_rating.reb = 75
        raw_rating.oiq = 70
        raw_rating.diq = 55
    elif archetype == 'playmaking big':
        raw_rating.spd = 55
        raw_rating.stre = 60
        raw_rating.jmp = 55
        raw_rating.ins = 55
        raw_rating.mid = 55
        raw_rating.tp = 45
        raw_rating.ft = 60
        raw_rating.pss = 75
        raw_rating.hndl = 65
        raw_rating.reb = 60
        raw_rating.oiq = 75
        raw_rating.diq = 55
    elif archetype == 'stretch big':
        raw_rating.spd = 50
        raw_rating.stre = 60
        raw_rating.jmp = 55
        raw_rating.ins = 55
        raw_rating.mid = 65
        raw_rating.tp = 75
        raw_rating.ft = 70
        raw_rating.pss = 50
        raw_rating.hndl = 50
        raw_rating.reb = 60
        raw_rating.oiq = 60
        raw_rating.diq = 55
    elif archetype == 'rim protector':
        raw_rating.spd = 50
        raw_rating.stre = 80
        raw_rating.jmp = 70
        raw_rating.ins = 55
        raw_rating.mid = 50
        raw_rating.tp = 40
        raw_rating.ft = 45
        raw_rating.pss = 40
        raw_rating.hndl = 40
        raw_rating.reb = 75
        raw_rating.oiq = 50
        raw_rating.diq = 80
    else:
        raise Exception('Unknown archetype')
    return raw_rating
