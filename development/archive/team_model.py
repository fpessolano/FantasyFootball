
from enum import Enum
from typing import List, Dict


class Position(Enum):
    GK = "GK"   # Goalkeeper
    CB = "CB"   # Center Back
    SW = "SW"   # Sweeper / Libero
    LB = "LB"   # Left Back
    RB = "RB"   # Right Back
    CM = "CM"   # Central Midfielder
    DM = "DM"   # Defensive Midfielder
    WB = "WB"   # Wing Back
    AM = "AM"   # Attacking Midfielder
    LM = "LM"   # Left Midfielder
    RM = "RM"   # Right Midfielder
    ST = "ST"   # Striker
    LW = "LW"   # Left Winger
    RW = "RW"   # Right Winger


class Player:
    def __init__(self, name: str, position: Position,
                 goalkeeping: int, defending: int, passing: int,
                 dribbling: int, shooting: int, physical: int):
        self.name = name
        self.position = position
        self.goalkeeping = goalkeeping
        self.defending = defending
        self.passing = passing
        self.dribbling = dribbling
        self.shooting = shooting
        self.physical = physical


class Team:
    def __init__(self, name: str, formation: str, players: List[Player]):
        self.name = name
        self.formation = formation
        self.players = players

    def compute_team_ratings(self) -> Dict[str, float]:
        # Compute ratings from player attributes
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
            total["keeping"] += p.goalkeeping if p.position == Position.GK else 0
            total["defence"] += p.defending
            total["midfield"] += p.passing + p.physical
            total["attack"] += p.shooting + p.dribbling
            total["left_flow"] += p.passing if p.position in (Position.LB, Position.LM, Position.LW) else 0
            total["right_flow"] += p.passing if p.position in (Position.RB, Position.RM, Position.RW) else 0
            total["center_flow"] += p.passing if p.position in (Position.CM, Position.AM, Position.DM, Position.ST) else 0

        count = len(self.players) or 1
        return {k: v / count for k, v in total.items()}
