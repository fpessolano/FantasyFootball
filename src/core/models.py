"""
Core domain models for Fantasy Football Manager.
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Player:
    """Represents a football player."""
    id: str
    name: str
    age: int
    position: str
    overall_rating: float
    team_id: Optional[str] = None


@dataclass
class Team:
    """Represents a football team."""
    id: str
    name: str
    elo_rating: float
    players: List[Player]
    league_id: Optional[str] = None


@dataclass
class Match:
    """Represents a football match."""
    id: str
    home_team_id: str
    away_team_id: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_date: Optional[datetime] = None
    completed: bool = False


@dataclass
class League:
    """Represents a football league."""
    id: str
    name: str
    country: str
    teams: List[Team]
    current_season: int
    matches: List[Match]