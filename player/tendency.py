from dataclasses import dataclass


@dataclass
class Tendency():
    ins_tend: int = 0
    mid_tend: int = 0
    tp_tend: int = 0