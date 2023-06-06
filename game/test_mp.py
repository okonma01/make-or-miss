
# create Game object, but simulate play_game() to test minutes played

# at start of method: 
# 1 - ensure mp and bench_time is 0 for all players
# 2 - start main game loop
# MAIN GAME LOOP:
# while self.state != 'game_over':
#     match self.state:
#         case 'tip_off':
#             game_engine.tip_off(self)
#         case 'inbound':
#             # check for subs (after n possessions or minutes)
#             game_engine.inbound(self)
#         case 'end_of_quarter':
#             game_engine.end_of_quarter(self)
#         case 'make_assist':
#             game_engine.make_assist(self)
#         case 'take_shot':
#             game_engine.take_shot(self)
#         case 'rebound':
#             game_engine.rebound(self)
#         case 'free_throw':
#             # check for subs
#             game_engine.free_throw(self)
#         case _:
#             pass
# game_engine.game_over(self)
# game_engine.set_winner(self)

# 3 - the only time update_mp() is called is in run_clock(); the only time run_clock() is called is in inbound() and free_throw()

from game.index import Game
import game.test_engine as test_engine


def test_mp(g: Game, no_of_games: int = 1) -> None:
    if no_of_games < 1:
        return
    for i in range(no_of_games):
        # g = Game()
        while g.state != 'game_over':
            match g.state:
                case 'tip_off':
                    test_engine.tip_off(g)
                case 'inbound':
                    # check for subs (after n possessions or minutes)
                    test_engine.inbound(g)
                case 'end_of_quarter':
                    test_engine.end_of_quarter(g)
                case 'make_assist':
                    test_engine.make_assist(g)
                case 'take_shot':
                    test_engine.take_shot(g)
                case 'rebound':
                    test_engine.rebound(g)
                case 'free_throw':
                    # check for subs
                    test_engine.free_throw(g)
                case _:
                    pass
        test_engine.game_over(g)
        test_engine.set_winner(g)
        test_engine.restart(g)
    test_engine.round_mp(g, no_of_games)