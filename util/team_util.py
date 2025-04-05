import csv
import json
import os
from typing import List, Optional
from pathlib import Path

from team.index import TeamGameSim
from player.index import PlayerGameSim
from player.position import Position
from player.rating import Rating
from util.helpers import height_rating
import pickle

path = '/Users/daniel/Documents/Python/mom/app/'


def save_team(t: TeamGameSim) -> None:
    fp = path + 'db/teams/' + t._name + '.pickle'
    # if not os.path.exists(fp):
    #     os.makedirs(fp)
    pickle_out = open(fp, 'wb')
    pickle.dump(t, pickle_out)
    pickle_out.close()
    print('Save successful: File path: ' + fp)
    return


def load_team(name: str) -> TeamGameSim:
    fp = path + 'db/teams/' + str(name) + '.pickle'
    if os.path.exists(fp):
        pickle_in = open(fp, 'rb')
        print('Loaded successfully!')
        return pickle.load(pickle_in)
    else:
        print('Load failed: No saved team named ' + str(name))
        return

    # Update the main.py file to use JSON files


def load_team(team_name, format="json"):
    """
    Load a team by name, supporting both JSON and CSV formats

    Args:
        team_name: Name of the team file (without extension)
        format: "json" or "csv"

    Returns:
        TeamGameSim: The loaded team
    """
    teams_dir = os.path.join('data', 'teams')

    if format == "json":
        file_path = os.path.join(teams_dir, f"{team_name}.json")
        return load_team_from_json(file_path)
    else:  # CSV format
        file_path = os.path.join(teams_dir, f"{team_name}.csv")
        return load_team_from_csv(file_path)


def load_team_from_csv(csv_path: str, team_name: Optional[str] = None) -> TeamGameSim:
    """
    Load team data from a CSV file and create a TeamGameSim object.

    Args:
        csv_path: Path to the CSV file
        team_name: Optional name for the team (defaults to filename without extension)

    Returns:
        TeamGameSim object populated with players from the CSV
    """
    # Use filename as team name if not provided
    if team_name is None:
        team_name = Path(csv_path).stem

    # Create the team
    team = TeamGameSim()
    team._name = team_name

    # Read the CSV file
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Create a new player
            player = PlayerGameSim()

            # Set basic attributes
            player._id = str(row['player_id'])
            player._jersey_no = int(row['no'])
            player._name = row['name']

            # Set position based on csv value
            pos_str = row['pos']
            if pos_str == 'G':
                player._pos = Position.G
            elif pos_str == 'GF':
                player._pos = Position.GF
            elif pos_str == 'F':
                player._pos = Position.F
            elif pos_str == 'FC':
                player._pos = Position.FC
            elif pos_str == 'C':
                player._pos = Position.C

            # Set height
            player_height = row['height']
            # convert from feet-inches to inches
            feet, inches = player_height.split('-')
            player._height_in_inches = int(feet) * 12 + int(inches)

            # Set player attributes
            rating = Rating()
            rating.hgt = height_rating(player._height_in_inches)
            rating.stre = int(row['stre'])
            rating.stam = int(row['stam'])
            rating.spd = int(row['spd'])
            rating.jmp = int(row['jmp'])
            rating.ins = int(row['ins'])
            rating.mid = int(row['mid'])
            rating.tp = int(row['tp'])
            rating.ft = int(row['ft'])
            rating.pss = int(row['pss'])
            rating.hndl = int(row['hndl'])
            rating.reb = int(row['reb'])
            rating.oiq = int(row['oiq'])
            rating.diq = int(row['diq'])
            rating.dur = int(row['dur'])
            rating.update_composite()
            player._rating = rating

            # Initialize game-specific attributes
            player._stat.energy = 100  # Players start with full energy
            player.clear_stat()   # Clear any default stats

            # Add the player to the team
            team._players.append(player)

    # Set lineup based on positions and ratings
    team.set_lineup()

    return team


def save_teams_from_csv_directory(directory_path: str, output_directory: str = None) -> List[str]:
    """
    Convert all CSV files in a directory to team pickle files.

    Args:
        directory_path: Path to directory containing CSV files
        output_directory: Optional directory to save pickle files (defaults to db/teams/)

    Returns:
        List of team names that were processed
    """
    if output_directory is None:
        output_directory = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'db', 'teams')

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    team_names = []

    # Process each CSV file
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            team_name = Path(filename).stem

            # Load team from CSV
            team = load_team_from_csv(file_path, team_name)
            team_names.append(team_name)

            # Save as pickle
            pickle_path = os.path.join(output_directory, f"{team_name}.pickle")
            with open(pickle_path, 'wb') as f:
                pickle.dump(team, f)

            print(f"Converted {filename} to {team_name}.pickle")

    return team_names


def load_team_from_json(json_file_path):
    """
    Load a team from a JSON file with the dictionary structure

    Args:
        json_file_path: Path to the JSON file

    Returns:
        TeamGameSim: A loaded team
    """
    # Create the team
    team = TeamGameSim()

    # Load the JSON data
    with open(json_file_path, 'r') as f:
        team_data = json.load(f)

    # Set team properties
    team._name = team_data.get("team_name", "")
    team._abbreviation = team_data.get("abbreviation", "")
    team._id = team_data.get("team_id", "")
    team._season = team_data.get("season", "")
    team._coach = team_data.get("coach", "")
    team._record = team_data.get("record", "")
    team._arena = team_data.get("arena", "")

    # Get the players dictionary
    players_dict = team_data.get("players", {})

    # Create player objects for each player
    for player_id, player_data in players_dict.items():
        # Create a new player
        player = PlayerGameSim()

        # Set player ID
        player._id = player_id

        # Set basic attributes
        player._jersey_no = player_data.get("no", 0)
        player._name = player_data.get("name", "")

        # Set position
        pos_str = player_data.get("pos", "")
        if pos_str == "G":
            player._pos = Position.G
        elif pos_str == "GF":
            player._pos = Position.GF
        elif pos_str == "F":
            player._pos = Position.F
        elif pos_str == "FC":
            player._pos = Position.FC
        elif pos_str == "C":
            player._pos = Position.C

        # Set height
        if "height_inches" in player_data:
            player._height_in_inches = player_data["height_inches"]
        elif "height" in player_data:
            player_height = player_data["height"]
            try:
                feet, inches = player_height.split('-')
                player._height_in_inches = int(feet) * 12 + int(inches)
            except (ValueError, AttributeError):
                player._height_in_inches = 75  # Default height

        # Set player ratings
        rating = Rating()
        rating.hgt = height_rating(player._height_in_inches)

        # Set all ratings
        for attr in ['stre', 'stam', 'spd', 'jmp', 'ins', 'mid', 'tp', 'ft',
                     'pss', 'hndl', 'reb', 'oiq', 'diq', 'dur']:
            if attr in player_data:
                setattr(rating, attr, int(player_data[attr]))

        rating.update_composite()
        player._rating = rating

        # Initialize game-specific attributes
        player._stat.energy = 100
        player.clear_stat()

        # Add the player to the team
        team._players.append(player)

    # Set lineup based on positions and ratings
    team.set_lineup()

    return team
