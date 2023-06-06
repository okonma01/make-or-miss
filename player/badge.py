from dataclasses import dataclass

from player.position import Position


@dataclass
class Badge():
    acrobat: bool = False
    catch_and_shoot: bool = False
    clamps: bool = False
    clutch_shooter: bool = False
    deadeye: bool = False
    dimer: bool = False
    ice_in_veins: bool = False
    post_lockdown: bool = False
    rebound_chaser: bool = False
    # rim_protector: bool = False
    space_creator: bool = False
    # unpluckable: bool = False


def gen_badge(pos: Position) -> Badge:
    b = Badge()
    badge_dict = dict()
    badge_dict['acrobat'] =         [20, 25, 15, 0, 0]
    badge_dict['catch_and_shoot'] = [15, 25, 20, 0, 0]
    badge_dict['clamps'] =          [0, 0, 0, 0, 0]
    badge_dict['clutch_shooter'] =  [10, 10, 10, 10, 10]
    badge_dict['deadeye'] =         [0, 0, 0, 0, 0]
    badge_dict['dimer'] =           [20, 5, 0, 0, 0]
    badge_dict['ice_in_veins'] =    [15, 15, 10, 0, 0]
    badge_dict['post_lockdown'] =   [0, 0, 0, 20, 20]
    badge_dict['rebound_chaser'] =  [0, 0, 0, 0, 0]
    badge_dict['space_creator'] =   [0, 0, 0, 0, 0]
    # for k in b.__dict__.keys():
