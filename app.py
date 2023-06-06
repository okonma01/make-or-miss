from flask import Flask
from flask import render_template
import eventlet
from flask_socketio import SocketIO

# added ../ to import from parent directory
from game.index import Game
from game.game_util import display_game_clock
from game.test_mp import test_mp
from player.overall import overall
from player.position import Position
from util.team_util import save_team, load_team
from util.helpers import height_in_feet

app = Flask(__name__)
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode='eventlet')


def get_player_stats(team):  # team is a TeamGameSim object
    player_stats = []
    for player in team._lineup:
        player_dict = {
            'name': player._name,
            'pts': player._stat.pts,
            'reb': player._stat.orb + player._stat.drb,
            'ast': player._stat.ast
        }
        player_stats.append(player_dict)
    return player_stats


def get_player_ratings(team):  # team is a TeamGameSim object
    player_ratings = []
    lineup_ratings = []
    bench_ratings = []
    for player in team._lineup:
        player_dict = {
            'name': player._name,
            'archetype': player._archetype,
            'hgt': height_in_feet(player._height_in_inches),
            'spd': player.rating('spd'),
            'stre': player.rating('stre'),
            'ins': player.rating('ins'),
            'mid': player.rating('mid'),
            'tp': player.rating('tp'),
            'oiq': player.rating('oiq'),
            'shot_usage': player.rating('shot_usage'),
            'foul_drawing': player.rating('drawing_foul'),
            'defense_perimeter': player.rating('defense_perimeter'),
            'defense_inside': player.rating('defense_inside'),
        }
        lineup_ratings.append(player_dict)
    for player in team._bench:
        player_dict = {
            'name': player._name,
            'archetype': player._archetype,
            'hgt': height_in_feet(player._height_in_inches),
            'spd': player.rating('spd'),
            'stre': player.rating('stre'),
            'ins': player.rating('ins'),
            'mid': player.rating('mid'),
            'tp': player.rating('tp'),
            'oiq': player.rating('oiq'),
            'shot_usage': player.rating('shot_usage'),
            'foul_drawing': player.rating('drawing_foul'),
            'defense_perimeter': player.rating('defense_perimeter'),
            'defense_inside': player.rating('defense_inside'),
        }
        bench_ratings.append(player_dict)
    return [lineup_ratings, bench_ratings]


def get_mp_stats(team):     # team is a TeamGameSim object
    lineup_stats = []
    bench_stats = []
    for player in team._lineup:
        # pos_val = Position[player._pos].value
        player_dict = {
            'name': player._name,
            'pos': player._pos,
            'ovr': player.ovr(player._pos.value),
            'mp': player.stat('mp'),
            'stam': player.rating('stam'),
            'halfcourt_usage': player.rating('halfcourt_usage'),
            'fastbreak_usage': player.rating('fastbreak_usage'),
            'shot_usage': player.rating('shot_usage'),
            'defense_inside': player.rating('defense_inside'),
            'defense_perimeter': player.rating('defense_perimeter'),
            # 'reb': player._stat.orb + player._stat.drb,
            # 'ast': player._stat.ast
        }
        lineup_stats.append(player_dict)
    for player in team._bench:
        # pos_val = Position.player._pos.value
        player_dict = {
            'name': player._name,
            'pos': player._pos,
            'ovr': player.ovr(player._pos.value),
            'mp': player.stat('mp'),
            'stam': player.rating('stam'),
            'halfcourt_usage': player.rating('halfcourt_usage'),
            'fastbreak_usage': player.rating('fastbreak_usage'),
            'shot_usage': player.rating('shot_usage'),
            'defense_inside': player.rating('defense_inside'),
            'defense_perimeter': player.rating('defense_perimeter'),
            # 'reb': player._stat.orb + player._stat.drb,
            # 'ast': player._stat.ast
        }
        bench_stats.append(player_dict)

    return [lineup_stats, bench_stats]


@app.route('/')
def simulate():
    team1 = load_team('Los Brooks')
    team2 = load_team('Los Lamboys')

    # simulate a basketball game here
    g = Game()
    g.teams = [team1, team2]
    g.restart_game()
    team1_player_stats = get_player_stats(team1)
    team2_player_stats = get_player_stats(team2)

    # generate the game data to send to the client
    game_data = {
        'team1_name': team1._name,
        'team1_score': team1._stat.pts,
        'team1_players': team1_player_stats,
        'team2_name': team2._name,
        'team2_score': team2._stat.pts,
        'team2_players': team2_player_stats,
        'time_remaining': g.game_clock
    }

    return render_template('exhibition.html',
                           team1_name=team1._name,
                           team1_score=team1._stat.pts,
                           team1_players=team1_player_stats,
                           team2_name=team2._name,
                           team2_score=team2._stat.pts,
                           team2_players=team2_player_stats,
                           time_remaining=display_game_clock(g.game_clock))


@app.route('/team/<team_name>')
def team_view(team_name):
    team = load_team('Los ' + team_name.title())
    player_ratings = get_player_ratings(team)
    return render_template('team_view.html', team=team, lineup_ratings=player_ratings[0], bench_ratings=player_ratings[1])

@app.route('/ratings/<team_name>')
def ratings(team_name):
    team = load_team('Los ' + team_name.title())
    return render_template('roster_ratings.html', team=team, height=height_in_feet, ovr=overall)



@app.route('/test_mp/<no>')
def test_mp_view(no):
    team = t2 if no == '2' else t1
    player_stats = get_mp_stats(team)
    return render_template('test_mp.html', team=team, lineup_stats=player_stats[0], bench_stats=player_stats[1])

# t1 = load_team('Los Edmondsons')
# t2 = load_team('Los Gonzalezs')
# g = Game()
# g.teams = [t1, t2]
# g.restart_game()
# test_mp(g, 41)

if __name__ == '__main__':
    app.run(debug=True)
