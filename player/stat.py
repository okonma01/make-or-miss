from dataclasses import dataclass
from datetime import timedelta

@dataclass
class PlayerStat():
    ast: int = 0
    bench_time: int = 0
    blk: int = 0
    court_time: int = 0
    drb: int = 0
    energy: int = 100
    fg: int = 0
    fg_inside: int = 0
    fg_midrange: int = 0
    fg_threepoint: int = 0
    fga: int = 0
    fga_inside: int = 0
    fga_midrange: int = 0
    fga_threepoint: int = 0
    ft: int = 0
    fta: int = 0
    g: int = 0
    gs: int = 0
    mp: float = 0
    orb: int = 0
    pf: int = 0
    # pos: int = 0
    pts: int = 0
    stl: int = 0
    tov: int = 0
