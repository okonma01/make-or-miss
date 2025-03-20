from util.team_util import load_team_from_csv
from game.index import Game
import os


def run_simulation_and_save_events(home_team_name, away_team_name):
    """
    Load teams from CSV, run a game simulation, and save events to a JSON file

    Args:
        home_team_csv: Path to home team CSV file
        away_team_csv: Path to away team CSV file
        output_json_path: Path to save the JSON output
    """

    # Build paths to team files
    teams_dir = os.path.join('data', 'teams')
    home_team_csv = os.path.join(teams_dir, f"{home_team_name}.csv")
    away_team_csv = os.path.join(teams_dir, f"{away_team_name}.csv")

    # Load teams
    home_team = load_team_from_csv(home_team_csv)
    away_team = load_team_from_csv(away_team_csv)

    # Create and run game
    game = Game()
    game.teams = [home_team, away_team]
    game.play_game()

    # Get event log and save to JSON
    event_log = game.logger.event_log

    # Save event log to JSON file
    event_log.to_json()

    return game


# Run the simulation
g = run_simulation_and_save_events('celtics.csv', 'nuggets.csv')
