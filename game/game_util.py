import random
from typing import List

# from game.game_engine import ensure_logger
from game.game_state import GameState
from player.overall import fatigue_adj_ovr
from team.util import get_best_at_position
from game.event import GameLogger

# Add this helper function at the top of the file


def ensure_logger(g) -> None:
    """Initialize logger if it doesn't exist yet"""
    if not hasattr(g, 'logger') or g.logger is None:
        g.logger = GameLogger(g)


def clock_over(g) -> bool:
    return g.game_clock == 0
    # return g.game_clock == GameEngine.end_clock


def display_game_clock(secs) -> str:
    mins = secs // 60
    secs = secs % 60
    if secs < 10:
        return str(mins) + ':0' + str(secs)
    return str(mins) + ':' + str(secs)


def do_foul() -> bool:
    res = random.random()
    return res < 0.14


def do_shot() -> bool:
    res = random.random()
    return res < 0.47


def do_subs(g, t: int) -> bool:
    did_subs = False
    # sub_dict = {pos: ovr} or {1: 63, 2: 65, 3: 44, 4: 56, 5: 61}
    sub_dict = {
        i+1: fatigue_adj_ovr(g.teams[t]._lineup[i], i+1) for i in range(5)}
    # sub_queue = [3, 4, 5, 1, 2]
    sub_queue = sorted(sub_dict.keys(), key=lambda k: sub_dict[k])

    player_set = set(g.teams[t]._bench)

    # Make sure the logger exists
    ensure_logger(g)

    # sub player at pos 3 (SF) out first
    for p in sub_queue:
        # do not sub if player is free throw man
        if t == g.o and p == g.shot_taker:
            continue
        sub_in = get_best_at_position(p, player_set, sub=True)
        sub_out = g.teams[t]._lineup[p-1]
        if sub_in and fatigue_adj_ovr(sub_in, p) > fatigue_adj_ovr(sub_out, p):
            # Log the substitution before actually swapping players
            g.logger.log_event(
                event_type="substitution",
                player_id=sub_out._id,  # Player coming in
                details={
                    "player_in_id": sub_in._id,
                    "player_out_id": sub_out._id,
                    "position": p,
                    "team_id": t
                }
            )

            # Now perform the actual substitution
            swap_players(g, t, sub_in, sub_out)
            index = g.teams[t]._lineup.index(sub_in)
            reset_player_stat(g, t, index, 'bench_time')
            player_set.remove(sub_in)
            # player_set.add(sub_out)
            did_subs = True

    return did_subs


def fatigue(g, seconds: int, stam: int) -> float:
    # fatigue is calculated per second
    # afterwards, this calculated value is subtracted from a player's energy
    # stam rating   1 sec   300 secs (6 mins)   720 secs(12 mins)
    # 50            0.0833  30                  60
    # 100           0.0556  20                  40
    fat = seconds * ((1/9) - (1/1800)*stam)
    fat = round(fat, 4)
    return -fat


def get_assist_man(g) -> int:
    ratios = list()
    if g.game_state == GameState.half_court:
        ratios = [p.rating('halfcourt_usage') for p in g.teams[g.o]._lineup]
    else:
        ratios = [p.rating('fastbreak_usage') for p in g.teams[g.o]._lineup]
    assist_man = pick_player(ratios, 4)
    return assist_man


def get_board_man(g, t) -> int:
    ratios = [p.rating('rebounding') for p in g.teams[t]._lineup]
    board_man = pick_player(ratios, 4)
    return board_man


def get_shot_taker(g) -> int:
    ratios = [p.rating('shot_usage') for p in g.teams[g.o]._lineup]
    shot_taker = pick_player(ratios, 8)
    return shot_taker


def get_steal_man(g) -> int:
    ratios = [p.rating('stealing') for p in g.teams[g.d]._lineup]
    steal_man = pick_player(ratios, 4)
    return steal_man


def pick_player(ratios: List[int], pow: int = 1) -> int:
    ratios = [r**pow for r in ratios]
    ratio_sum = sum(ratios)
    if ratio_sum == 0:
        return random.choice([0, 1, 2, 3, 4])

    rand_val = random.random() * ratio_sum
    running_sum = 0

    for i in range(len(ratios)):
        running_sum += ratios[i]
        if rand_val < running_sum:
            return i

    return 0


def record_bench_stat(g, t: int, p: int, s: str, amt: int = 1) -> None:
    g.teams[t]._bench[p]._stat.__dict__[s] += amt


def record_player_stat(g, t: int, p: int, s: str, amt: int = 1) -> None:
    g.teams[t]._lineup[p]._stat.__dict__[s] += amt


def record_stat(g, s: str, shot_type: str = str(), amt: int = 0) -> None:
    match s:
        case 'make_assist':
            record_team_stat(g, g.o, 'pos', amt)
            # record_team_stat(g, g.o, 'opp_pos')
            # record_team_stat(g, g.d, 'pos')
            record_team_stat(g, g.d, 'opp_pos', amt)
        case 'turnover':
            record_player_stat(g, g.o, g.assist_man, 'tov')
            record_player_stat(g, g.d, g.steal_man, 'stl')
            record_team_stat(g, g.o, 'tov')
            record_team_stat(g, g.o, 'opp_stl')
            record_team_stat(g, g.d, 'stl')
            record_team_stat(g, g.d, 'opp_tov')
        case 'take_shot':
            record_player_stat(g, g.o, g.shot_taker, shot_type)
            record_player_stat(g, g.o, g.shot_taker, 'fga')
            record_team_stat(g, g.o, 'fga')
            record_team_stat(g, g.d, 'opp_fga')
            if shot_type == 'fga_threepoint':
                record_team_stat(g, g.o, 'tpa')
                record_team_stat(g, g.d, 'opp_tpa')
            else:
                record_team_stat(g, g.o, 'twopa')
                record_team_stat(g, g.d, 'opp_twopa')
        case 'shot_made':
            record_team_stat(g, g.o, 'pts', amt)
            record_team_stat(g, g.d, 'opp_pts', amt)
            if shot_type != 'ft':
                record_team_stat(g, g.o, 'fg')
                record_team_stat(g, g.d, 'opp_fg')
            if shot_type == 'fga_threepoint':
                record_team_stat(g, g.o, 'tp')
                record_team_stat(g, g.d, 'opp_tp')
            elif shot_type in ['fga_midrange', 'fga_inside']:
                record_team_stat(g, g.o, 'twop')
                record_team_stat(g, g.d, 'opp_twop')

            record_player_stat(g, g.o, g.shot_taker, 'pts', amt)

            if shot_type != 'ft':
                record_player_stat(g, g.o, g.shot_taker, 'fg')
                record_player_stat(g, g.o, g.shot_taker,
                                   shot_type[:2]+shot_type[3:])
            if g.shot_taker != g.assist_man and shot_type != 'ft':
                record_player_stat(g, g.o, g.assist_man, 'ast')
                record_team_stat(g, g.o, 'ast')
                record_team_stat(g, g.d, 'opp_ast')
        case 'orb':
            record_player_stat(g, g.o, g.board_man, 'orb')
            record_team_stat(g, g.o, 'orb')
            record_team_stat(g, g.d, 'opp_orb')
        case 'drb':
            record_player_stat(g, g.d, g.board_man, 'drb')
            record_team_stat(g, g.o, 'drb')
            record_team_stat(g, g.d, 'opp_drb')
        case 'ft':
            record_player_stat(g, g.o, g.shot_taker, 'fta')
            record_team_stat(g, g.o, 'fta')
            record_team_stat(g, g.d, 'opp_fta')
        case 'ft_made':
            record_player_stat(g, g.o, g.shot_taker, 'ft')
            record_team_stat(g, g.o, 'ft')
            record_team_stat(g, g.d, 'opp_ft')
        case 'mp':
            for i in range(5):
                record_player_stat(g, g.o, i, 'mp', amt)
                record_player_stat(g, g.d, i, 'mp', amt)

            # update bench_time for players on bench
            for i in range(len(g.teams[g.o]._bench)):
                record_bench_stat(g, g.o, i, 'bench_time', amt)

            for i in range(len(g.teams[g.d]._bench)):
                record_bench_stat(g, g.d, i, 'bench_time', amt)
        case 'energy':
            secs = amt
            # tire out on-court players
            for i in range(5):
                record_player_stat(g, g.o, i, 'energy', fatigue(
                    g, secs, g.teams[g.o]._lineup[i].rating('stam')))
                if g.teams[g.o]._lineup[i]._stat.__dict__['energy'] < 0:
                    g.teams[g.o]._lineup[i]._stat.__dict__['energy'] = 0

                record_player_stat(g, g.d, i, 'energy', fatigue(
                    g, secs, g.teams[g.d]._lineup[i].rating('stam')))
                if g.teams[g.d]._lineup[i]._stat.__dict__['energy'] < 0:
                    g.teams[g.d]._lineup[i]._stat.__dict__['energy'] = 0

            # recover players on bench
            secs = round(secs*0.094, 4)
            for i in range(len(g.teams[g.o]._bench)):
                record_bench_stat(g, g.o, i, 'energy', secs)
                if g.teams[g.o]._bench[i]._stat.__dict__['energy'] > 100:
                    g.teams[g.o]._bench[i]._stat.__dict__['energy'] = 100

            for i in range(len(g.teams[g.d]._bench)):
                record_bench_stat(g, g.d, i, 'energy', secs)
                if g.teams[g.d]._bench[i]._stat.__dict__['energy'] > 100:
                    g.teams[g.d]._bench[i]._stat.__dict__['energy'] = 100
        case _:
            pass
    return


def record_team_stat(g, t: int, s: str, amt: int = 1) -> None:
    g.teams[t]._stat.__dict__[s] += amt


def reset_bench_stat(g, t: int, p: int, s: str) -> None:
    if s == 'energy':
        g.teams[t]._bench[p]._stat.__dict__[s] = 100
    else:
        g.teams[t]._bench[p]._stat.__dict__[s] = 0


def reset_clock(g) -> None:
    if g.quarter_no > 4:    # overtime
        g.game_clock = 300
    else:
        g.game_clock = 720


def reset_player_stat(g, t: int, p: int, s: str) -> None:
    if s == 'energy':
        g.teams[t]._lineup[p]._stat.__dict__[s] = 100
    else:
        g.teams[t]._lineup[p]._stat.__dict__[s] = 0


def reset_variables(g) -> None:
    g.assist_man, g.shot_taker = -1, -1
    g.board_man, g.steal_man = -1, -1
    g.fts = 0
    g.last_ft_made = False


def reset_game(g) -> None:
    for t in g.teams:
        t.clear_stat()
        for p in t._players:
            p.clear_stat()
        t.set_lineup()
    g.quarter_no = 1
    reset_clock(g)
    reset_variables(g)
    g.o, g.d = 0, 1
    g.winner = None
    g.game_state = GameState.half_court
    g.pos_per_sub = 6


def round_mp(g, t: int) -> None:
    for p in g.teams[t]._lineup:
        p._stat.mp = p._stat.mp // 60
    for p in g.teams[t]._bench:
        p._stat.mp = p._stat.mp // 60


def run_clock(g, turnover: bool = False) -> None:
    # TO-DO:
    # 1. add minutes to players currently on the court - DONE
    # 2. tire on-court players out; recover players on bench - DONE (check record_stat 'energy')

    # Store the current game clock time before updating
    previous_time = g.game_clock
    previous_minute = previous_time // 60

    # Existing run_clock logic to determine seconds elapsed
    if turnover:
        seconds = random.randint(8, 14)
    else:
        if g.game_state == GameState.transition:
            seconds = random.randint(8, 16)
        else:
            seconds = random.randint(16, 24)

    # Update clock
    new_time = max(0, g.game_clock - seconds)
    new_minute = new_time // 60

    # Check if we've crossed a minute boundary
    if new_minute < previous_minute:
        # Make sure the logger exists
        ensure_logger(g)
        # Create a minute-based checkpoint
        g.logger.create_checkpoint(checkpoint_type="minute")

    # Update the game clock
    g.game_clock = new_time

    # Update players' minutes and fatigue
    update_mp(g, seconds)
    update_energy(g, seconds)


def scores_tied(g) -> bool:
    return g.teams[0]._stat.pts == g.teams[1]._stat.pts


def swap_players(g, t, sub_in, sub_out) -> None:
    in_idx = g.teams[t]._bench.index(sub_in)
    out_idx = g.teams[t]._lineup.index(sub_out)
    g.teams[t]._bench[in_idx] = sub_out
    g.teams[t]._lineup[out_idx] = sub_in


def swap_teams(g) -> None:
    if g.o == 0:
        g.o = 1
        g.d = 0
    else:
        g.o = 0
        g.d = 1


def time_for_sub(g) -> bool:
    if g.pos_per_sub <= 0:
        g.pos_per_sub = 6
        return True
    g.pos_per_sub -= 1
    return False


def turnover(g) -> bool:
    if random.random() < 0.08:
        return True
    else:
        return False


def update_energy(g, seconds: int) -> None:
    record_stat(g, 'energy', amt=seconds)


def update_mp(g, seconds: int) -> None:
    record_stat(g, 'mp', amt=seconds)
