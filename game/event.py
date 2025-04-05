from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
from datetime import datetime
from util.helpers import generate_id


@dataclass
class GameEvent:
    # "shot_made", "shot_missed", "free_throw", "rebound", "foul" (TODO), "turnover", "substitution"
    # also "tip_off", "quarter_end", "game_end"
    event_type: str
    timestamp: float  # Game clock time in seconds
    quarter: int
    team_id: int  # 0 or 1 (index of the team in the game.teams list)
    player_id: int  # Player index in team lineup
    details: Optional[Dict]  # Additional event-specific details

    # For tip-offs:
    # tip_off - Done (no details needed)

    # For quarter changes:
    # quarter_end - Done (no details needed)

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
    # }

    # For free throws:
    # free_throw - Done
    # details = {
    #    "made": bool,
    #    "free_throw_num": int,  # 1, 2, or 3 in sequence
    #    "total_free_throws": int  # Total in this trip
    # }

    # For rebounds:
    # rebound - Done
    # details = {
    #    "rebound_type": "offensive|defensive"
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
class GameCheckpoint:
    """Represents a complete game state at a specific point in time."""
    # Identification
    checkpoint_id: str
    timestamp: str  # ISO format timestamp when checkpoint was created

    # Game state
    game_time: str  # Game clock in MM:SS format
    quarter: int
    home_score: int
    away_score: int
    # The state machine state ('inbound', 'take_shot', etc.)
    current_state: str
    offensive_team_id: int  # Current offensive team (0 or 1)

    # Player states (key: player_id, value: player state dict)
    player_states: Dict[str, Dict]

    # Event reference
    last_event_index: int  # Index of last event in event log

    # Add team stats
    team_stats: List[Dict]  # Stats for each team (home=0, away=1)


@dataclass
class GameEventLog:
    # Game information
    game_id: str
    date: str

    # Teams information (List of team dictionaries)
    teams: List[Dict]

    # Game events
    events: List[GameEvent]

    # Add checkpoints
    checkpoints: List[GameCheckpoint] = field(default_factory=list)

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
            ],
            "checkpoints": [
                {
                    "checkpoint_id": cp.checkpoint_id,
                    "timestamp": cp.timestamp,
                    "game_time": cp.game_time,
                    "quarter": cp.quarter,
                    "home_score": cp.home_score,
                    "away_score": cp.away_score,
                    "current_state": cp.current_state,
                    "offensive_team_id": cp.offensive_team_id,
                    "player_states": cp.player_states,
                    "last_event_index": cp.last_event_index,
                    "team_stats": cp.team_stats
                } for cp in self.checkpoints
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

        # Parse checkpoints if they exist
        checkpoints = []
        if "checkpoints" in data:
            checkpoints = [
                GameCheckpoint(
                    checkpoint_id=cp["checkpoint_id"],
                    timestamp=cp["timestamp"],
                    game_time=cp["game_time"],
                    quarter=cp["quarter"],
                    home_score=cp["home_score"],
                    away_score=cp["away_score"],
                    current_state=cp["current_state"],
                    offensive_team_id=cp["offensive_team_id"],
                    player_states=cp["player_states"],
                    last_event_index=cp["last_event_index"],
                    team_stats=cp["team_stats"] if "team_stats" in cp else []
                ) for cp in data["checkpoints"]
            ]

        return cls(
            game_id=game_info["game_id"],
            date=game_info["date"],
            teams=game_info["teams"],
            events=events,
            checkpoints=checkpoints
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
                "abbreviation": self.game.teams[0]._abbreviation,
                "players": [self._player_info(p, 0) for p in self.game.teams[0]._players],
                "starting_lineup": [p._id for p in self.game.teams[0]._lineup],
                "season": self.game.teams[0]._season,
                "coach": self.game.teams[0]._coach,
                "record": self.game.teams[0]._record,
                "arena": self.game.teams[0]._arena
            },
            {
                "team_id": 1,
                "team_name": self.game.teams[1]._name,
                "abbreviation": self.game.teams[1]._abbreviation,
                "players": [self._player_info(p, 1) for p in self.game.teams[1]._players],
                "starting_lineup": [p._id for p in self.game.teams[1]._lineup],
                "season": self.game.teams[1]._season,
                "coach": self.game.teams[1]._coach,
                "record": self.game.teams[1]._record,
                "arena": self.game.teams[1]._arena
            }
        ]

        return GameEventLog(
            game_id=self.game._id,
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
        
        # Collect player states
        player_states = {}
        for team_id, team in enumerate(self.game.teams):
            for player in team._players:
                player_states[player._id] = {
                    "ast": player._stat.ast,
                    "blk": player._stat.blk,
                    "court_time": player._stat.court_time,
                    "drb": player._stat.drb,
                    "energy": round(player._stat.energy, 1),
                    "fg": player._stat.fg,
                    "fga": player._stat.fga,
                    "fg_threepoint": player._stat.fg_threepoint,
                    "fga_threepoint": player._stat.fga_threepoint,
                    "ft": player._stat.ft,
                    "fta": player._stat.fta,
                    "orb": player._stat.orb,
                    "mp": player._stat.mp,  # remember this is stored as int
                    "pf": player._stat.pf,
                    "pts": player._stat.pts,
                    "stl": player._stat.stl,
                    "tov": player._stat.tov,
                }
        details["player_states"] = player_states
        if event_type == "substitution":
            team_id = details["team_id"]
        else:
            team_id = self.game.o
        event = GameEvent(
            event_type=event_type,
            timestamp=self.game.game_clock,
            quarter=self.game.quarter_no,
            team_id=team_id,  # Current offensive team
            player_id=player_id,
            details=details
        )

        self.event_log.events.append(event)

    def create_checkpoint(self, checkpoint_type="quarter") -> str:
        """Create a checkpoint of the current game state.

        Args:
            checkpoint_type: Type of checkpoint ("quarter", "minute", or "manual")

        Returns:
            checkpoint_id: Unique identifier for this checkpoint
        """
        # Generate unique ID for this checkpoint
        checkpoint_id = f"{self.event_log.game_id}_cp_{len(self.event_log.checkpoints) + 1}"

        # Format game time as MM:SS
        minutes = self.game.game_clock // 60
        seconds = self.game.game_clock % 60
        game_time = f"{minutes}:{seconds:02d}"

        # Collect player states
        player_states = {}
        for team_id, team in enumerate(self.game.teams):
            for player in team._players:
                player_states[player._id] = {
                    "ast": player._stat.ast,
                    "blk": player._stat.blk,
                    "court_time": player._stat.court_time,
                    "drb": player._stat.drb,
                    "energy": round(player._stat.energy, 1),
                    "fg": player._stat.fg,
                    "fga": player._stat.fga,
                    "fg_threepoint": player._stat.fg_threepoint,
                    "fga_threepoint": player._stat.fga_threepoint,
                    "ft": player._stat.ft,
                    "fta": player._stat.fta,
                    "orb": player._stat.orb,
                    "mp": player._stat.mp,  # remember this is stored as int
                    "pf": player._stat.pf,
                    "pts": player._stat.pts,
                    "stl": player._stat.stl,
                    "tov": player._stat.tov,
                }

        # Collect team stats
        team_stats = []
        for team in self.game.teams:
            stats = {
                # Traditional stats
                "pts": team._stat.pts,
                "fg": team._stat.fg,
                "fga": team._stat.fga,
                "tp": team._stat.tp,
                "tpa": team._stat.tpa,
                "twop": team._stat.twop,
                "twopa": team._stat.twopa,
                "ft": team._stat.ft,
                "fta": team._stat.fta,
                "orb": team._stat.orb,
                "drb": team._stat.drb,
                "ast": team._stat.ast,
                "stl": team._stat.stl,
                "blk": team._stat.blk,
                "tov": team._stat.tov,
                "pf": team._stat.pf,

                # Derived stats (if you want to include them)
                "fg_pct": round(team._stat.fg*100 / team._stat.fga, 1) if team._stat.fga > 0 else 0,
                "tp_pct": round(team._stat.tp*100 / team._stat.tpa, 1) if team._stat.tpa > 0 else 0,
                "ft_pct": round(team._stat.ft*100 / team._stat.fta, 1) if team._stat.fta > 0 else 0,
            }
            team_stats.append(stats)
        
        # In the create_checkpoint method
        current_time = self.game.game_clock
        last_event_index = -1

        # Find the index of the last event at or before the current time
        for i, event in enumerate(self.event_log.events):
            if event.timestamp >= current_time:  # Events are stored in seconds remaining, so larger values are earlier
                last_event_index = i

        # Create checkpoint
        checkpoint = GameCheckpoint(
            checkpoint_id=checkpoint_id,
            timestamp=datetime.now().isoformat(),
            game_time=game_time,
            quarter=self.game.quarter_no,
            home_score=self.game.teams[0]._stat.pts,
            away_score=self.game.teams[1]._stat.pts,
            current_state=self.game.state,
            offensive_team_id=self.game.o,
            player_states=player_states,
            last_event_index=last_event_index,
            team_stats=team_stats
        )

        # Add checkpoint to event log
        self.event_log.checkpoints.append(checkpoint)

        return checkpoint_id

    def save_to_file(self, filename=None) -> str:
        # Save the event log to a JSON file
        if filename is None:
            filename = f"data/games/game_{self.event_log.game_id}.json"

        with open(filename, 'w') as f:
            f.write(self.event_log.to_json())

        return filename
