from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from datetime import datetime
from util.helpers import generate_id


@dataclass
class GameEvent:
    # "shot_made", "shot_missed", "free_throw", "foul" (TODO), "turnover", "substitution"
    # also "tip_off", "quarter_change", "game_end"
    event_type: str
    timestamp: float  # Game clock time in seconds
    quarter: int
    team_id: int  # 0 or 1 (index of the team in the game.teams list)
    player_id: int  # Player index in team lineup
    details: Optional[Dict]  # Additional event-specific details

    # For tip-offs:
    # tip_off - Done (no details needed)

    # For quarter changes:
    # quarter_change - Done (no details needed)

    # For game end:
    # game_end - Done (no details needed)

    # For shots:
    # shot_made and shot_missed - Done
    # details = {
    #    "shot_type": "fga_inside|fga_midrange|fga_threepoint",
    #    "points": 2 or 3,
    #    "shooting_foul": bool,
    #    "assist_player_id": Optional[int],  # Player who assisted, if any
    #    "defender_id": Optional[int]  # Player who defended, if any
    #    "rebounder_id": Optional[int]  # Player who got the rebound, if any
    #    "rebound_type": Optional["offensive|defensive"],
    # }

    # For free throws:
    # free_throw - Done
    # details = {
    #    "made_sequence": List[bool]  # List of booleans indicating made or missed free throws
    #    "shooter_id": int
    #    "rebounder_id": Optional[int]  # Player who got the rebound on the last free throw, if any
    #    "rebound_type": Optional["offensive|defensive"],
    # }

    # For fouls: TODO - this is not implemented in the game engine yet
    # details = {
    #    "foul_type": "shooting|personal|technical",
    #    "fouled_by_player_id": int
    # }

    # For turnovers:
    # turnover - Done
    # details = {
    #    "steal_player_id": Optional[int],  # Player who got the steal, if any
    # }

    # For substitutions:
    # substitution - Done
    # details = {
    #    "player_in_id": int,
    #    "player_out_id": int
    # }


@dataclass
class GameEventLog:
    # Game information
    game_id: str
    date: str

    # Teams information (List of team dictionaries)
    teams: List[Dict]

    # Game events
    events: List[GameEvent]

    # Methods for JSON conversion
    def to_json(self) -> str:
        # Convert to dictionary with compact format
        data = {
            "game_info": {
                "game_id": self.game_id,
                "date": self.date,
                "teams": self.teams
            },
            "events": [
                {
                    "event_type": e.event_type,
                    "timestamp": self._format_timestamp(e.timestamp),
                    "quarter": e.quarter,
                    "team_id": e.team_id,
                    "player_id": e.player_id,
                    "details": e.details
                } for e in self.events
            ]
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        # Convert seconds to MM:SS format
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    @classmethod
    def from_json(cls, json_str: str) -> 'GameEventLog':
        data = json.loads(json_str)
        game_info = data["game_info"]

        # Parse events
        events = [
            GameEvent(
                event_type=e["event_type"],
                # Convert MM:SS back to seconds
                timestamp=cls._parse_timestamp(e["timestamp"]),
                quarter=e["quarter"],
                team_id=e["team_id"],
                player_id=e["player_id"],
                details=e["details"]
            ) for e in data["events"]
        ]

        return cls(
            game_id=game_info["game_id"],
            date=game_info["date"],
            teams=game_info["teams"],
            events=events
        )

    @staticmethod
    def _parse_timestamp(timestamp: str) -> float:
        # Convert MM:SS format to seconds
        parts = timestamp.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds


class GameLogger:
    def __init__(self, game):
        self.game = game
        self.event_log = self._initialize_event_log()
    
    def _initialize_event_log(self) -> GameEventLog:
        # Set up teams information as an array
        teams = [
            {
                "team_id": 0,
                "team_name": self.game.teams[0]._name,
                "players": [self._player_info(p, 0) for p in self.game.teams[0]._players]
            },
            {
                "team_id": 1,
                "team_name": self.game.teams[1]._name,
                "players": [self._player_info(p, 1) for p in self.game.teams[1]._players]
            }
        ]
        
        return GameEventLog(
            game_id=generate_id(self.game),
            date=datetime.now().strftime("%Y-%m-%d"),
            teams=teams,
            events=[]
        )
    
    def _player_info(self, player, team_id) -> Dict:
        # Extract relevant player information
        return {
            "player_id": player._id,
            "player_name": player._name,
            "player_index": self.game.teams[team_id]._players.index(player)
        }
    
    def log_event(self, event_type, player_id, details=None) -> None:
        # Create and add event to the log
        if details is None:
            details = {}
            
        event = GameEvent(
            event_type=event_type,
            timestamp=self.game.game_clock,
            quarter=self.game.quarter_no,
            team_id=self.game.o,  # Current offensive team
            player_id=player_id,
            details=details
        )
        
        self.event_log.events.append(event)
    
    def save_to_file(self, filename=None) -> str:
        # Save the event log to a JSON file
        if filename is None:
            filename = f"game_{self.event_log.game_id}.json"
        
        with open(filename, 'w') as f:
            f.write(self.event_log.to_json())
        
        return filename