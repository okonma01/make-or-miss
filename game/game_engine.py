import random
from dataclasses import dataclass
from game.game_state import GameState
from game.game_util import pick_player, record_stat, get_assist_man, get_steal_man, get_shot_taker, get_board_man, reset_game, round_mp, swap_teams, reset_variables, time_for_sub, do_subs, clock_over, turnover, run_clock, do_foul, do_shot, scores_tied, reset_clock
from game.game_util import ensure_logger
# from game.event import GameLogger
# from game.index import Game


def tip_off(g) -> None:
    # jump ball - (for now, pick a random player) - DONE
    # set g.o and g.d (teams) - DONE
    # set quarter_no = 1, game_clock to 12:00 - DONE
    # set game_state to HALF_COURT - DONE
    # to-do:
    # get teams best jump ball players - DONE
    t1_players = [p.rating('jump_ball') for p in g.teams[0]._lineup]
    p1 = t1_players.index(max(t1_players))
    t2_players = [p.rating('jump_ball') for p in g.teams[1]._lineup]
    p2 = t2_players.index(max(t2_players))

    ratios = [p1, p2]
    winner_of_tip_off = pick_player(ratios, 2)
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

    # Add logger initialization and event logging
    ensure_logger(g)
    winner_player = g.teams[g.o]._lineup[p1 if g.o == 0 else p2]
    g.logger.log_event(
        event_type="tip_off",
        player_id=winner_player._id,
    )

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

    # set assist man - DONE
    g.assist_man = get_assist_man(g)
    if turnover(g):    # TODO transition or fast break - right now it is random
        # set steal man - DONE
        run_clock(g, turnover=True)
        if clock_over(g):
            g.to_end_of_quarter()
            return None

        g.steal_man = get_steal_man(g)
        record_stat(g, 'turnover')

        # Log turnover event
        ensure_logger(g)
        assist_player = g.teams[g.o]._lineup[g.assist_man]
        steal_player = g.teams[g.d]._lineup[g.steal_man]
        steal_details = {"steal_player_id": steal_player._id}

        g.logger.log_event(
            event_type="turnover",
            player_id=assist_player._id,
            details=steal_details
        )

        g.game_state = GameState.transition
        swap_teams(g)
        g.to_make_assist()
    else:
        g.to_take_shot()


def take_shot(g) -> None:
    # pick shooter - DONE
    # record stats (fga)
    run_clock(g)
    g.shot_taker = get_shot_taker(g)
    shot_type = random.choice(['fga_threepoint', 'fga_midrange', 'fga_inside'])
    shot_made = do_shot()
    foul_committed = do_foul()
    record_stat(g, 'take_shot', shot_type=shot_type)
    # g.fts = 3 if shot_type == 'fga_threepoint' else 2
    if shot_made:
        if foul_committed: # and-1
            g.fts = 1
        else: # shot made, no foul
            g.fts = 0
    else:
        if foul_committed:
            g.fts = 3 if shot_type == 'fga_threepoint' else 2
        else:
            g.fts = 0

    # Prepare to log shot event
    ensure_logger(g)
    shot_taker = g.teams[g.o]._lineup[g.shot_taker]
    points = 3 if shot_type == 'fga_threepoint' else 2

    # Build details dictionary
    shot_details = {
        "shot_type": shot_type,
        "points": points,
        "shooting_foul": foul_committed
    }

    # Add assist information if applicable
    if g.assist_man >= 0 and g.assist_man != g.shot_taker:
        assist_player = g.teams[g.o]._lineup[g.assist_man]
        shot_details["assist_player_id"] = assist_player._id

    # Add defender information
    defender_index = g.shot_taker  # Matching index in defensive lineup
    if defender_index < len(g.teams[g.d]._lineup):
        defender = g.teams[g.d]._lineup[defender_index]
        shot_details["defender_id"] = defender._id

    if shot_made:
        record_stat(g, 'shot_made', shot_type=shot_type, amt=points)
        g.logger.log_event(
            event_type="shot_made",
            player_id=shot_taker._id,
            details=shot_details
        )

        if foul_committed:
            g.to_free_throw()
        else:
            g.to_inbound()
    else:
        g.logger.log_event(
            event_type="shot_missed",
            player_id=shot_taker._id,
            details=shot_details
        )

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
    ensure_logger(g)

    if x < 0.15:  # offensive rebound
        # set board_man - DONE
        g.board_man = get_board_man(g, g.o)
        record_stat(g, 'orb')

        # Log offensive rebound
        board_player = g.teams[g.o]._lineup[g.board_man]
        g.logger.log_event(
            event_type="rebound",
            player_id=board_player._id,
            details={"rebound_type": "offensive"}
        )

        reset_variables(g)
    else:  # defensive rebound
        # set board_man - DONE
        g.board_man = get_board_man(g, g.d)
        record_stat(g, 'drb')

        # get board_player before swapping teams, as it will be the player from the defensive team
        board_player = g.teams[g.d]._lineup[g.board_man]

        g.game_state = GameState.transition
        swap_teams(g)

        # Log defensive rebound
        # NOTE: I swapped teams before logging here, to ensure team_id=self.game.o from event.py is the rebounder's team
        g.logger.log_event(
            event_type="rebound",
            player_id=board_player._id,
            details={"rebound_type": "defensive"}
        )

    g.to_make_assist()


def free_throw(g) -> None:
    # free throw mechanism here
    if time_for_sub(g):
        do_subs(g, g.o)
        do_subs(g, g.d)

    ensure_logger(g)
    shot_taker = g.teams[g.o]._lineup[g.shot_taker]

    g.last_ft_made = False
    for i in range(g.fts):
        record_stat(g, 'ft')
        x = random.random()
        ft_made = x < 0.75

        # Log free throw event
        g.logger.log_event(
            event_type="free_throw",
            player_id=shot_taker._id,
            details={
                "made": ft_made,
                "free_throw_num": i + 1,
                "total_free_throws": g.fts
            }
        )

        if ft_made:
            record_stat(g, 'shot_made', 'ft', amt=1)
            record_stat(g, 'ft_made')
            if i == g.fts-1:
                g.last_ft_made = True

    if g.last_ft_made:
        g.to_inbound()
    else:                               # miss
        g.to_rebound()


def end_of_quarter(g) -> None:
    ensure_logger(g)

    # Log end of quarter event
    g.logger.log_event(
        event_type="quarter_end",
        player_id=None,  # No specific player
        details={
            "quarter": g.quarter_no,
            "home_score": g.teams[0]._stat.pts,
            "away_score": g.teams[1]._stat.pts
        }
    )

    # Create quarterly checkpoint
    g.logger.create_checkpoint(checkpoint_type="quarter")

    # Existing end_of_quarter logic
    if g.quarter_no == 4:  # end of regulation
        if scores_tied(g):
            g.to_inbound()   # go to overtime
        else:
            g.to_game_over()
    else:    # we are not at q4 yet
        g.quarter_no += 1
        reset_clock(g)
        g.to_inbound()


def game_over(g) -> None:
    ensure_logger(g)
    # Log game over event
    g.logger.log_event(
        event_type="game_over",
        player_id=None,  # No specific player
        details={
            "home_score": g.teams[0]._stat.pts,
            "away_score": g.teams[1]._stat.pts
        }
        # player_states needs mp stat in seconds, so round_mp() comes after
    )
    # for clean up
    round_mp(g, g.o)
    round_mp(g, g.d)

    # Save the game log to a file
    g.logger.save_to_file()


def set_winner(g) -> None:
    # set game winner and loser
    if g.teams[g.o]._stat.pts > g.teams[g.d]._stat.pts:
        g.winner = g.teams[g.o]
    else:
        g.winner = g.teams[g.d]

# call game_util restart function


def restart(g) -> None:
    reset_game(g)


@dataclass
class GameEngine():
    end_clock: int = 0
