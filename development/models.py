"""
Fantasy Football Models
~~~~~~~~~~~~~~~~~~~~~~~

Core data models for the Fantasy Football simulation system.
"""

from enum import Enum
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import json


class Position(Enum):
    """Player positions with their abbreviations."""
    GK = "GK"   # Goalkeeper
    CB = "CB"   # Center Back
    SW = "SW"   # Sweeper / Libero
    LB = "LB"   # Left Back
    RB = "RB"   # Right Back
    CM = "CM"   # Central Midfielder
    DM = "DM"   # Defensive Midfielder
    WB = "WB"   # Wing Back (generic)
    LWB = "LWB" # Left Wing Back
    RWB = "RWB" # Right Wing Back
    AM = "AM"   # Attacking Midfielder
    LM = "LM"   # Left Midfielder
    RM = "RM"   # Right Midfielder
    ST = "ST"   # Striker
    LW = "LW"   # Left Winger
    RW = "RW"   # Right Winger


class TacticalStyle(Enum):
    """Team tactical styles with their effect multipliers."""
    BALANCED = (1.0, 1.0, 1.0)  # (attack_mult, defence_mult, midfield_mult)
    ATTACKING = (1.2, 0.9, 1.0)
    DEFENSIVE = (0.8, 1.2, 1.0)
    WIDE = (1.0, 1.0, 1.1)      # emphasises side flows
    CENTRAL = (1.0, 1.0, 0.9)   # emphasises central play
    
    def multipliers(self) -> Tuple[float, float, float]:
        return self.value


@dataclass
class Player:
    """
    Represents a football player with their attributes.
    
    Attributes:
        name: Player's name
        position: Playing position (Position enum)
        goalkeeping: Goalkeeping ability (0-100)
        defending: Defensive ability (0-100)
        passing: Passing ability (0-100)
        dribbling: Dribbling ability (0-100)
        shooting: Shooting ability (0-100)
        physical: Physical ability (0-100)
    """
    name: str
    position: Position
    goalkeeping: int
    defending: int
    passing: int
    dribbling: int
    shooting: int
    physical: int
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "position": self.position.name,
            "goalkeeping": self.goalkeeping,
            "defending": self.defending,
            "passing": self.passing,
            "dribbling": self.dribbling,
            "shooting": self.shooting,
            "physical": self.physical
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary."""
        return cls(
            name=data["name"],
            position=Position[data["position"]],
            goalkeeping=data["goalkeeping"],
            defending=data["defending"],
            passing=data["passing"],
            dribbling=data["dribbling"],
            shooting=data["shooting"],
            physical=data["physical"]
        )
    
    def overall_rating(self) -> float:
        """Calculate overall player rating based on position."""
        if self.position == Position.GK:
            return (self.goalkeeping * 0.5 + self.defending * 0.2 + 
                    self.physical * 0.2 + self.passing * 0.1)
        elif self.position in [Position.CB, Position.SW, Position.LB, Position.RB]:
            return (self.defending * 0.4 + self.physical * 0.3 + 
                    self.passing * 0.2 + self.dribbling * 0.1)
        elif self.position in [Position.CM, Position.DM, Position.WB, Position.LWB, Position.RWB]:
            return (self.passing * 0.3 + self.defending * 0.2 + 
                    self.physical * 0.2 + self.dribbling * 0.2 + self.shooting * 0.1)
        elif self.position in [Position.AM, Position.LM, Position.RM]:
            return (self.passing * 0.3 + self.dribbling * 0.3 + 
                    self.shooting * 0.2 + self.physical * 0.1 + self.defending * 0.1)
        else:  # ST, LW, RW
            return (self.shooting * 0.35 + self.dribbling * 0.25 + 
                    self.physical * 0.2 + self.passing * 0.15 + self.defending * 0.05)


@dataclass
class Team:
    """
    Represents a football team.
    
    Attributes:
        name: Team name
        formation: Team formation (e.g., "4-4-2")
        players: List of players in the team
        style: Tactical style
        elo_rating: Elo rating for competitive play
        streak_count: Current win/loss streak
    """
    name: str
    formation: str
    players: List[Player] = field(default_factory=list)
    style: TacticalStyle = TacticalStyle.BALANCED
    elo_rating: float = 1500.0
    streak_count: int = 0
    
    def compute_team_ratings(self) -> Dict[str, float]:
        """Compute aggregated team ratings from player attributes."""
        total = {
            "keeping": 0,
            "defence": 0,
            "midfield": 0,
            "attack": 0,
            "left_flow": 0,
            "right_flow": 0,
            "center_flow": 0,
        }
        
        for p in self.players:
            # Goalkeeping
            total["keeping"] += p.goalkeeping if p.position == Position.GK else 0
            
            # Defence
            total["defence"] += p.defending
            
            # Midfield
            total["midfield"] += p.passing + p.physical
            
            # Attack
            total["attack"] += p.shooting + p.dribbling
            
            # Flow calculations
            if p.position in [Position.LB, Position.LM, Position.LW, Position.LWB]:
                total["left_flow"] += p.passing
            elif p.position in [Position.RB, Position.RM, Position.RW, Position.RWB]:
                total["right_flow"] += p.passing
            elif p.position in [Position.CM, Position.AM, Position.DM, Position.ST, Position.SW]:
                total["center_flow"] += p.passing
        
        # Normalize by player count
        count = max(len(self.players), 1)
        return {k: v / count for k, v in total.items()}
    
    def compute_strength(self) -> float:
        """Compute overall team strength."""
        ratings = self.compute_team_ratings()
        att_mult, def_mult, mid_mult = self.style.multipliers()
        
        # Apply tactical multipliers
        gk = ratings["keeping"]
        defense = ratings["defence"] * def_mult
        midfield = ratings["midfield"] * mid_mult
        attack = ratings["attack"] * att_mult
        
        # Weighted average
        return gk * 0.1 + defense * 0.3 + midfield * 0.3 + attack * 0.3
    
    def adjust_for_streak(self, enabled: bool = True) -> float:
        """Calculate momentum adjustment based on streak."""
        if not enabled:
            return 1.0
        streak_bonus = min(max(self.streak_count, -5), 5)
        return 1 + 0.03 * streak_bonus
    
    def to_dict(self) -> Dict:
        """Convert team to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "formation": self.formation,
            "style": self.style.name,
            "elo_rating": self.elo_rating,
            "players": [p.to_dict() for p in self.players]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Team':
        """Create team from dictionary."""
        players = [Player.from_dict(p) for p in data.get("players", [])]
        return cls(
            name=data["name"],
            formation=data["formation"],
            players=players,
            style=TacticalStyle[data.get("style", "BALANCED")],
            elo_rating=data.get("elo_rating", 1500.0)
        )
    
    def validate_formation(self) -> Tuple[bool, str]:
        """
        Validate team formation.
        
        Returns:
            Tuple of (is_valid, message)
        """
        if len(self.players) != 11:
            return False, f"Team must have exactly 11 players, has {len(self.players)}"
        
        gk_count = sum(1 for p in self.players if p.position == Position.GK)
        if gk_count != 1:
            return False, f"Team must have exactly 1 goalkeeper, has {gk_count}"
        
        return True, "Valid formation"
    
    def summary(self) -> str:
        """Generate a summary of the team."""
        ratings = self.compute_team_ratings()
        strength = self.compute_strength()
        
        # Format streak
        if self.streak_count > 0:
            streak_str = f"{self.streak_count}W streak"
            streak_emoji = "🔥"
        elif self.streak_count < 0:
            streak_str = f"{abs(self.streak_count)}L streak"
            streak_emoji = "❄️"
        else:
            streak_str = "No streak"
            streak_emoji = "⚪"
        
        lines = [
            f"\n📋 {self.name} ({self.style.name})",
            f"Formation: {self.formation}",
            f"Elo Rating: {self.elo_rating:.0f}",
            f"Current Form: {streak_emoji} {streak_str}",
            f"Total Strength: {strength:.2f}",
            "",
            "Players:"
        ]
        
        for p in sorted(self.players, key=lambda x: x.position.name):
            lines.append(
                f"  {p.name:20} {p.position.name:3} "
                f"G:{p.goalkeeping:2d} D:{p.defending:2d} P:{p.passing:2d} "
                f"Dr:{p.dribbling:2d} S:{p.shooting:2d} Ph:{p.physical:2d} "
                f"(OVR: {p.overall_rating():.0f})"
            )
        
        lines.extend([
            "",
            "Team Ratings:",
            f"  Keeping: {ratings['keeping']:.1f}",
            f"  Defence: {ratings['defence']:.1f}",
            f"  Midfield: {ratings['midfield']:.1f}",
            f"  Attack: {ratings['attack']:.1f}",
            f"  Left Flow: {ratings['left_flow']:.1f}",
            f"  Center Flow: {ratings['center_flow']:.1f}",
            f"  Right Flow: {ratings['right_flow']:.1f}"
        ])
        
        return "\n".join(lines)


# Position groupings for team building
POSITION_GROUPS = {
    "Goalkeeper": [Position.GK],
    "Defenders": [Position.CB, Position.SW, Position.LB, Position.RB],
    "Defensive Midfielders": [Position.DM, Position.WB, Position.LWB, Position.RWB],
    "Midfielders": [Position.CM, Position.LM, Position.RM],
    "Attacking Midfielders": [Position.AM],
    "Forwards": [Position.ST, Position.LW, Position.RW],
}

# Common formations with position requirements
FORMATIONS = {
    "4-4-2": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.CM: 2,
        Position.LM: 1,
        Position.RM: 1,
        Position.ST: 2
    },
    "4-3-3": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.CM: 3,
        Position.LW: 1,
        Position.RW: 1,
        Position.ST: 1
    },
    "3-5-2": {
        Position.GK: 1,
        Position.CB: 3,
        Position.CM: 2,
        Position.LWB: 1,
        Position.RWB: 1,
        Position.AM: 1,
        Position.ST: 2
    },
    "4-2-3-1": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.DM: 2,
        Position.AM: 1,
        Position.LW: 1,
        Position.RW: 1,
        Position.ST: 1
    },
    "5-3-2": {
        Position.GK: 1,
        Position.CB: 3,
        Position.LWB: 1,
        Position.RWB: 1,
        Position.CM: 3,
        Position.ST: 2
    }
}