from util.team_util import load_team_from_csv

# Load Celtics and Nuggets teams
celtics = load_team_from_csv('celtics.csv')
nuggets = load_team_from_csv('nuggets.csv')

# Print team info
def print_team_info(team):
    print(f"\n=== {team._name} ===")
    print(f"Number of players: {len(team._players)}")
    
    print("\nStarting lineup:")
    for i, player in enumerate(team._lineup):
        print(f"{i+1}. {player._name} ({player._pos.name}) - Height: {player._height_in_inches//12}'{player._height_in_inches%12}\"")
    
    print("\nBench players:")
    for i, player in enumerate(team._bench):
        print(f"{i+1}. {player._name} ({player._pos.name})")
    
    # Print a key player's ratings
    star_player = team._lineup[0]
    print(f"\nSample player ratings for {star_player._name}:")
    print(f"3PT: {star_player._rating.tp}")
    print(f"FG: {star_player._rating.ins}")
    print(f"Speed: {star_player._rating.spd}")
    print(f"Overall: {star_player.ovr()}")

print_team_info(celtics)
print_team_info(nuggets)