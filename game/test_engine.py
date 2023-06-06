import random
from dataclasses import dataclass
from game.game_state import GameState
from game.game_util import record_stat, reset_game, round_mp, swap_teams, reset_variables, time_for_sub, do_subs, clock_over, run_clock, scores_tied, reset_clock


# def record_player_stat(g, t: int, p: int, s: str, amt: int = 1) -> None:
#     g.teams[t]._players[p]._stat.__dict__[s] += amt


# def record_team_stat(g, t: int, s: str, amt: int = 1) -> None:
#     g.teams[t]._stat.__dict__[s] += amt


def tip_off(g) -> None:
    # jump ball - (for now, pick a random player) - DONE
    # set g.o and g.d (teams) - DONE
    # set quarter_no = 1, game_clock to 12:00 - DONE
    # set game_state to HALF_COURT - DONE
    # to-do:
    # get teams best jump ball players - DONE

    # set winner of tip off to random player
    winner_of_tip_off = random.choice([0, 1])
    if winner_of_tip_off == 0:
        g.o = 0
        g.d = 1
    else:
        g.o = 1
        g.d = 0
    if g.quarter_no <= 4:
        g.quarter_no = 1
    g.game_clock = 720
    g.game_state = GameState.half_court
    g.to_make_assist()


def inbound(g) -> None:
    # check for substitutions
    # swap teams
    swap_teams(g)
    reset_variables(g)
    if time_for_sub(g):
        do_subs(g, g.o)
        do_subs(g, g.d)
    g.game_state = GameState.half_court
    g.to_make_assist()


def make_assist(g) -> None:
    if clock_over(g):
        g.to_end_of_quarter()
        return None
    # set assist man (for now, pick a random player)
    # ratios = [g.teams[g.o]._players[i] for i in range(5)]
    # record_stat(g, 'make_assist', amt=1)

    g.assist_man = random.choice([0, 1, 2, 3, 4])
    if random.random() < 0.08:    # turnover
        # set steal man (for now, pick a random player)
        run_clock(g, turnover=True)
        if clock_over(g):
            g.to_end_of_quarter()
            return None
        g.steal_man = random.choice([0, 1, 2, 3, 4])
        record_stat(g, 'turnover')
        g.game_state = GameState.transition
        swap_teams(g)
        g.to_make_assist()
    else:
        g.to_take_shot()


def take_shot(g) -> None:
    # set shooter (usage depends on game state; for now pick a random player)
    # record stats (fga)
    run_clock(g)
    g.shot_taker = random.choice([0, 1, 2, 3, 4])
    shot_type = random.choice(['fga_threepoint', 'fga_midrange', 'fga_inside'])
    shot_made = random.random() < 0.47
    foul_committed = random.random() < 0.14
    record_stat(g, 'take_shot', shot_type=shot_type)
    g.fts = 3 if shot_type == 'fga_threepoint' else 2
    if shot_made:
        record_stat(g, 'shot_made', shot_type=shot_type, amt=g.fts)
        if foul_committed:
            g.to_free_throw()
        else:
            g.to_inbound()
    else:
        if foul_committed:
            g.to_free_throw()
        else:
            g.to_rebound()


def rebound(g) -> None:
    # if defensive rebound, set game_state to transition and swap teams
    # if offensive rebound, go to 'make_assist' state
    if clock_over(g):
        g.to_end_of_quarter()
        return None
    x = random.random()
    if x < 0.15:            # offensive rebound
        # set board_man (for now pick a random player)
        g.board_man = random.choice([0, 1, 2, 3, 4])
        record_stat(g, 'orb')
        reset_variables(g)
        # record_stat(g, 'make_assist', amt=-1)
    else:
        # set board_man (for now pick a random player)
        g.board_man = random.choice([0, 1, 2, 3, 4])
        record_stat(g, 'drb')
        g.game_state = GameState.transition
        swap_teams(g)
    g.to_make_assist()


def free_throw(g) -> None:
    # free throw mechanism here
    if time_for_sub(g):
        do_subs(g, g.o)
        do_subs(g, g.d)
    for i in range(g.fts):
        record_stat(g, 'ft')
        x = random.random()
        if x < 0.75:
            record_stat(g, 'shot_made', 'ft', amt=1)
            record_stat(g, 'ft_made')
        if i == g.fts-1 and x < 0.75:
            g.last_ft_made = True
    if g.last_ft_made:
        g.to_inbound()
    else:                               # miss
        g.to_rebound()


def end_of_quarter(g) -> None:
    if g.quarter_no == 4:            # end of regulation
        if scores_tied(g):
            # go to overtime
            g.to_inbound()
        else:
            g.to_game_over()
    else:                               # we are not at q4 yet
        g.quarter_no += 1
        reset_clock(g)
        g.to_inbound()


def game_over(g) -> None:
    # for clean up
    pass
    # round_mp(g, g.o)
    # round_mp(g, g.d)


def set_winner(g) -> None:
    # set game winner and loser
    if g.teams[g.o]._stat.pts > g.teams[g.d]._stat.pts:
        g.winner = g.teams[g.o]
    else:
        g.winner = g.teams[g.d]


def round_mp(g, t: int) -> None:
    for t in range(2):
        for p in g.teams[t]._lineup:
            p._stat.mp = round(p._stat.mp / 60, 1)
        for p in g.teams[t]._bench:
            p._stat.mp = round(p._stat.mp / 60, 1)


# call game_util restart function
def restart(g) -> None:
    for t in g.teams:
        t.clear_stat()
        for p in t._players:
            for s in p._stat.__dict__:
                if s == 'mp':
                    continue
                if s == 'energy':
                    p._stat.__dict__[s] = 100
                else:
                    p._stat.__dict__[s] = 0
    t.set_lineup()
    g.quarter_no = 1
    reset_clock(g)
    reset_variables(g)
    g.o, g.d = 0, 1
    g.winner = None
    g.game_state = GameState.half_court
    g.pos_per_sub = 6


@dataclass
class GameEngine():
    end_clock: int = 0
