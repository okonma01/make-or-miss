from game.gen_game import gen_game
from game.index import Game
from team.gen_team import gen_team
from util.team_util import save_team, load_team
from game.stat_util import box_score
from game.test_mp import test_mp

# from team.gen_team import gen_team
# from random import randint

# TO-DO: 
# saving game plays
# substitutions
# overall

# d = {x: 0 for x in range(5, 16)}
# teams = list()
# for i in range(100):
#     t = gen_team()
#     d[len(t._lineup)] += 1
#     teams.append(t)
# print(d)

if __name__ == '__main__':
    # t1 = load_team('Los Brooks')
    # t2 = load_team('Los Lamboys')
    t1 = gen_team()
    t2 = gen_team()
    # g = Game()
    # g.teams = [t1, t2]
    # g.restart_game()
    # test_mp(g, 82)

    # for p in t1._players:
    #     p._rating.update_composite()
    # for p in t2._players:
    #     p._rating.update_composite()
    save_team(t1)
    save_team(t2)
    # g.play_game()
    pass


# for i in range(10):
#     g = gen_game()
#     g.play_game()
#     print(g.get_score())