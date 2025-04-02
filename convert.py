#!/usr/bin/env python3
# filepath: /Users/daniel/Documents/repos/make-or-miss/convert.py

import csv
import json
import os

TEAMS_DICT = {
    'cavaliers16': {
        'team_id': 'cavaliers16',
        'team_name': 'Cleveland Cavaliers',
        'season': '2016',
        'record': '57-25',
    },
    'warriors17': {
        'team_id': 'warriors17',
        'team_name': 'Golden State Warriors',
        'season': '2017',
        'record': '67-15',
    },
    'raptors19': {
        'team_id': 'raptors19',
        'team_name': 'Toronto Raptors',
        'season': '2019',
        'record': '58-24',
    },
    'lakers20': {
        'team_id': 'lakers20',
        'team_name': 'Los Angeles Lakers',
        'season': '2020',
        'record': '52-19',
    },
    'bucks21': {
        'team_id': 'bucks21',
        'team_name': 'Milwaukee Bucks',
        'season': '2021',
        'record': '46-26',
    },
    'nuggets23': {
        'team_id': 'nuggets23',
        'team_name': 'Denver Nuggets',
        'season': '2023',
        'record': '53-29',
    },
    'celtics24': {
        'team_id': 'celtics24',
        'team_name': 'Boston Celtics',
        'season': '2024',
        'record': '64-18',
    },
}

def convert_csv_to_json_dict(csv_file_path, json_file_path=None):
    """
    Convert a CSV file containing player data to a JSON format with players as a dictionary
    keyed by player_id
    
    Args:
        csv_file_path: Path to the input CSV file
        json_file_path: Path to save the output JSON file (optional)
                        If None, will use the same name as CSV but with .json extension
    
    Returns:
        dict: The JSON data as a Python dictionary
    """

    if 'template' in csv_file_path:
        # Skip template files
        return
    
    # Determine output path if not provided
    if json_file_path is None:
        base_name = os.path.splitext(csv_file_path)[0]
        json_file_path = f"{base_name}.json"
    
    # Read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        # Skip the first line if it's a comment
        first_line = csv_file.readline().strip()
        if first_line.startswith('//'):
            # Restart from the beginning
            csv_file.seek(0)
            # Skip the first line
            next(csv_file)
        else:
            # If it wasn't a comment, go back to the beginning
            csv_file.seek(0)
        
        # Read the CSV data
        csv_reader = csv.DictReader(csv_file)
        
        # Initialize players dictionary
        players_dict = {}
        
        # Process each player row
        for row in csv_reader:
            # Extract player_id for use as the dictionary key
            player_id = row.pop('player_id', None)
            
            if not player_id:
                # print(f"Warning: Missing player_id in row {row}. Skipping.")
                continue
                
            # Convert numeric fields to appropriate types
            for key in row:
                if key in ['no']:
                    try:
                        row[key] = int(row[key])
                    except ValueError:
                        # If conversion fails, keep as string
                        pass
                elif key in ['stre', 'stam', 'spd', 'jmp', 'ins', 'mid', 'tp', 
                            'ft', 'pss', 'hndl', 'reb', 'oiq', 'diq', 'dur']:
                    try:
                        row[key] = int(row[key])
                    except ValueError:
                        # If conversion fails, keep as string
                        pass
            
            # Parse height into inches
            if 'height' in row:
                try:
                    feet, inches = row['height'].split('-')
                    total_inches = int(feet) * 12 + int(inches)
                    row['height_in_inches'] = total_inches
                except (ValueError, AttributeError):
                    # Keep original height if parsing fails
                    pass
            
            # Add this player to the dictionary
            players_dict[player_id] = row
    
    # Extract team information from filename
    team_id = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    # Get team name (remove year suffix and capitalize)
    team_base_name = ''.join([c for c in team_id if not c.isdigit()])
    team_name = team_base_name.capitalize()
    
    # Create the final JSON structure
    json_data = {
        "team_id": team_id,
        "team_name": TEAMS_DICT[team_id]['team_name'],
        "season": TEAMS_DICT[team_id]['season'],
        "players": players_dict,
        "record": TEAMS_DICT[team_id]['record'],
    }
    
    # Write to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    
    # print(f"Successfully converted {csv_file_path} to {json_file_path} with dictionary format")
    return json_data

def process_all_csv_files(directory_path="data/teams"):
    """
    Process all CSV files in the specified directory and convert them to JSON
    
    Args:
        directory_path: Path to the directory containing CSV files
    """
    # Create directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {directory_path}")
        return
    
    # Process each CSV file
    for csv_file in csv_files:
        csv_path = os.path.join(directory_path, csv_file)
        convert_csv_to_json_dict(csv_path)

if __name__ == "__main__":
    # Check if a specific file was provided as argument
    import sys
    
    if len(sys.argv) > 1:
        # Process the specific file
        csv_file = sys.argv[1]
        if os.path.exists(csv_file):
            convert_csv_to_json_dict(csv_file)
        else:
            print(f"File not found: {csv_file}")
    else:
        # Process all CSV files in the teams directory
        process_all_csv_files()
        
        # Or process just the Celtics file:
        # csv_file = "data/teams/celtics24.csv"
        # convert_csv_to_json_dict(csv_file)