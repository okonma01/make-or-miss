import csv
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
        output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'teams')
    
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
