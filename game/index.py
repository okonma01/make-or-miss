from typing import List
from transitions import Machine
from datetime import timedelta
from team.index import TeamGameSim
from game.game_state import GameState
import game.game_engine as game_engine
from game.event import GameLogger
from util.helpers import generate_id
from game.game_util import ensure_logger

# changed game_clock attribute of Game class to int type (seconds)
# changed game_engine.reset_clock() to set game_clock to 720 (12 minutes)
# changed game_engine.run_clock() to reduce game_clock by seconds (not timedelta)

# changed get_best_at_position() to filter out injured players
# changed get_best_at_position() during subs using bench_time stat
# updated update_mp(): it now updates bench_time for players on the bench
# cleared bench_time stat for players subbing in
# got teams' tallest players on jump ball
# prevented injured players from subbing in
# prevented free throw shooters from subbing out

# to-do (game_engine):
# 2. composite ratings - almost DONE
# 3. right now, g.assist_man (DONE) and g.shot_taker are random players - fix this
# 4. turnovers are also random - fix this


class Game(object):

    states = ['tip_off', 'inbound', 'end_of_quarter', 'game_over',
              'make_assist', 'take_shot', 'rebound', 'free_throw']

    def __init__(self):
        self._id: str = generate_id(self)
        self.logger: None         # initialize logger after teams are set
        self.machine: Machine = Machine(
            model=self, states=Game.states, initial='tip_off')
        self.game_clock: int = 720
        self.quarter_no: int = 1
        self.teams: List[TeamGameSim] = list()
        self.assist_man: int = -1
        self.shot_taker: int = -1
        self.board_man: int = -1
        self.steal_man: int = -1
        self.last_ft_made: bool = False
        self.fts: int = 0
        self.o: int = 0
        self.d: int = 1
        self.winner: TeamGameSim = None
        self.game_state: GameState = GameState.half_court
        self.pos_per_sub = 6

    def play_game(self) -> None:
        # This ensures the logger is initialized before the game starts
        # even if we don't call tip_off directly
        ensure_logger(self)
        while self.state != 'game_over':
            match self.state:
                case 'tip_off':
                    game_engine.tip_off(self)
                case 'inbound':
                    # check for subs (after n possessions or minutes)
                    game_engine.inbound(self)
                case 'end_of_quarter':
                    game_engine.end_of_quarter(self)
                case 'make_assist':
                    game_engine.make_assist(self)
                case 'take_shot':
                    game_engine.take_shot(self)
                case 'rebound':
                    game_engine.rebound(self)
                case 'free_throw':
                    # check for subs
                    game_engine.free_throw(self)
                case _:
                    pass
        game_engine.game_over(self)
        game_engine.set_winner(self)

    def restart_game(self) -> None:
        game_engine.restart(self)

    def get_score(self) -> str:
        res = self.teams[0]._name + ' ' + str(self.teams[0]._stat.pts)
        res += ' - '
        res += str(self.teams[1]._stat.pts) + ' ' + self.teams[1]._name
        return res
