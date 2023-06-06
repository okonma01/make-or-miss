from dataclasses import dataclass

@dataclass
class TeamStat():
    g: int = 0
    mp: float = 0
    fg: int = 0
    fga: int = 0
    tp: int = 0
    tpa: int = 0
    twop: int = 0
    twopa: int = 0
    ft: int = 0
    fta: int = 0
    orb: int = 0
    drb: int = 0
    trb: int = 0
    ast: int = 0
    stl: int = 0
    blk: int = 0
    tov: int = 0
    pf: int = 0
    # pos: int = 0
    pts: int = 0
    opp_g: int = 0
    opp_mp: float = 0
    opp_fg: int = 0
    opp_fga: int = 0
    opp_tp: int = 0
    opp_tpa: int = 0
    opp_twop: int = 0
    opp_twopa: int = 0
    opp_ft: int = 0
    opp_fta: int = 0
    opp_orb: int = 0
    opp_drb: int = 0
    opp_trb: int = 0
    opp_ast: int = 0
    opp_stl: int = 0
    opp_blk: int = 0
    opp_tov: int = 0
    opp_pf: int = 0
    # opp_pos: int = 0
    opp_pts: int = 0