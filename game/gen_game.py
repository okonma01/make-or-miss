from game.index import Game
from team.gen_team import gen_team

def gen_game() -> Game:
    t1 = gen_team()
    t2 = gen_team()
    g = Game()
    g.teams = [t1, t2]
    return g