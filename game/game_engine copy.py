from dataclasses import dataclass
from datetime import timedelta
from .game_state import GameState
# import index
import random

from .game_util import pick_player


def scores_tied(g: index.Game) -> bool:
    return g.teams[0].stat.pts == g.teams[1].stat.pts


def reset_clock(g: Game) -> None:
    if g.quarter_no > 4:
        g.game_clock = timedelta(minutes=5, seconds=0)
    else:
        g.game_clock = timedelta(minutes=12, seconds=0)


def run_clock(g: Game) -> None:
    # TO-DO:
    # 1. add minutes to players currently on the court
    # 2. tire on-court players out; recover players on bench
    if g.game_state == GameState.transition:
        delta = random.randint(4, 10)
    else:
        delta = random.randint(10, 18)
    new_clock = timedelta(seconds=delta)
    if (g.game_clock - new_clock).days == -1:
        g.game_clock = timedelta(0)
    else:
        g.game_clock = g.game_clock - new_clock


def clock_over(g: Game) -> bool:
    return g.game_clock == GameEngine.end_clock


def reset_variables(g: Game) -> None:
    g.assist_man, g.shot_taker = 0, 0
    g.board_man, g.steal_man = 0, 0
    g.fts = 0
    g.last_ft_made = False


def record_player_stat(g: Game, t: int, p: int, s: str, amt: int = 1) -> None:
    g.teams[t]._players[p]._stat.__dict__[s] += amt


def record_team_stat(g: Game, t: int, s: str, amt: int = 1) -> None:
    g.teams[t]._stat.__dict__[s] += amt


def tip_off(g: Game) -> None:
    # get teams tallest players on jump ball (for now, pick a random player) - DONE
    # set g.o and g.d (teams) - DONE
    # set quarter_no = 1, game_clock to 12:00 - DONE
    # set game_state to HALF_COURT - DONE
    p1 = random.randint(0, 4)
    p2 = random.randint(0, 4)
    ratios = [g.teams[0]._players[p1]._rating.hgt,
              g.teams[1]._players[p2]._rating.hgt]
    winner_of_tip_off = pick_player(ratios)
    if winner_of_tip_off == 0:
        g.o = 0
        g.d = 1
    else:
        g.o = 1
        g.d = 0
    if g.quarter_no <= 4:
        g.quarter_no = 1
    g.game_clock = timedelta(minutes=12, seconds=0)
    g.game_state = GameState.half_court
    g.to_make_assist()


def inbound(g: Game) -> None:
    # check for substitutions
    # swap teams
    swap_teams(g)
    reset_variables(g)
    g.game_state = GameState.half_court
    g.to_make_assist()


def turnover(g: Game) -> bool:
    if random.random() < 0.2:
        return True
    else:
        return False


def swap_teams(g: Game) -> None:
    if g.o == 0:
        g.o = 1
        g.d = 0
    else:
        g.o = 0
        g.d = 1


def make_assist(g: Game) -> None:
    if clock_over(g):
        g.to_end_of_quarter()
        return None
    # set assist man (for now, pick a random player)
    # ratios = [g.teams[g.o]._players[i] for i in range(5)]
    record_team_stat(g, g.o, 'pos')
    record_team_stat(g, g.d, 'pos')
    g.assist_man = random.randint(0, 4)
    if turnover():    # transition or fast break - right now it is random
        # swap teams - DONE
        # record stats (stl + TO) - DONE
        g.steal_man = random.randint(0, 4)
        record_player_stat(g, g.o, g.assist_man, 'tov')
        record_player_stat(g, g.d, g.steal_man, 'stl')
        record_team_stat(g, g.o, 'tov')
        record_team_stat(g, g.d, 'stl')
        g.game_state = GameState.transition
        swap_teams()
        g.to_make_assist()
    else:
        g.to_take_shot()


def take_shot(g: Game) -> None:
    # set shooter (usage depends on game state; for now pick a random player)
    # record stats (fga)
    run_clock(g)
    g.shot_taker = random.randint(0, 4)
    shot_type = random.choice(['fga_threepoint', 'fga_midrange', 'fga_inside'])
    shot_made = shot_made()
    foul_committed = foul_committed()
    record_player_stat(g, g.o, g.shot_taker, shot_type)
    record_team_stat(g, g.o, 'fga')
    if shot_type == 'fga_threepoint':
        record_player_stat(g, g.o, g.shot_taker, 'tpa')
    else:
        record_player_stat(g, g.o, g.shot_taker, 'twopa')

    g.fts = 3 if shot_type == 'fga_threepoint' else 2
    if shot_made:
        record_team_stat(g, g.o, 'pts', g.fts)
        record_team_stat(g, g.o, 'fg')
        record_player_stat(g, g.o, g.shot_taker, 'pts', g.fts)
        record_player_stat(g, g.o, g.shot_taker, shot_type[:2]+shot_type[3:])
        if g.shot_taker != g.assist_man:
            record_player_stat(g, g.o, g.assist_man, 'ast')
            record_team_stat(g, g.o, 'ast')
            # record_team_stat(g, g.d, )
        if foul_committed:
            g.to_free_throw()
        else:
            g.to_inbound()
    else:
        if foul_committed:
            g.to_free_throw()
        else:
            g.to_rebound()


def shot_made() -> bool:
    res = random.random()
    return res < 0.47


def rebound(g: Game) -> None:
    # if defensive rebound, set game_state to transition and swap teams
    # if offensive rebound, go to 'make_assist' state
    if clock_over(g):
        g.to_end_of_quarter()
        return None
    x = random.random()
    if x < 0.15:            # offensive rebound
        record_team_stat(g, g.o, 'orb')
        # set board_man (for now pick a random player)
        reset_variables(g)
    else:
        record_team_stat(g, g.d, 'drb')
        # set board_man (for now pick a random player)
        g.game_state = GameState.transition
        swap_teams()
    g.to_make_assist()


def free_throw(g: Game) -> None:
    # free throw mechanism here
    for i in range(g.fts):
        record_player_stat(g, g.o, g.shot_taker, 'fta')
        record_team_stat(g, g.o, 'fta')
        x = random.random()
        if x < 0.75:
            record_player_stat(g, g.o, g.shot_taker, 'ft')
            record_team_stat(g, g.o, 'ft')
        if i == g.fts-1 and x < 0.75:
            g.last_ft_made = True
    if g.last_ft_made:
        g.to_inbound()
    else:                               # miss
        g.to_rebound()


def foul_committed() -> bool:
    res = random.random()
    return res < 0.17


def end_of_quarter(g: Game) -> None:
    if g.quarter_no == 4:            # end of regulation
        if scores_tied():
            # go to overtime
            g.to_inbound()
        else:
            g.to_game_over()
    else:                               # we are not at q4 yet
        quarter_no += 1
        reset_clock(g)
        g.to_inbound()


def set_winner(g: Game) -> None:
    # set game winner and loser
    if g.teams[g.o]._stat.pts > g.teams[g.d]._stat.pts:
        g.winner = g.teams[g.o]
    else:
        g.winner = g.teams[g.d]


@dataclass
class GameEngine():
    end_clock: timedelta = timedelta(minutes=0, seconds=0)
