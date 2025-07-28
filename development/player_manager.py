"""
Player Manager
~~~~~~~~~~~~~~

Module for creating and managing players in the Fantasy Football system.
"""

import json
import random
from typing import List, Optional, Dict
from models import Player, Position


class PlayerManager:
    """Manages player creation, loading, and saving."""
    
    def __init__(self, filename: str = "players.json"):
        self.filename = filename
        self.players: List[Player] = []
        self.load_players()
    
    def load_players(self) -> None:
        """Load players from JSON file."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.players = [Player.from_dict(p) for p in data]
        except FileNotFoundError:
            self.players = []
    
    def save_players(self) -> None:
        """Save players to JSON file."""
        with open(self.filename, "w") as f:
            json.dump([p.to_dict() for p in self.players], f, indent=2)
    
    def add_player(self, player: Player) -> None:
        """Add a player to the roster."""
        self.players.append(player)
        self.save_players()
    
    def create_random_player(self, position: Optional[Position] = None, 
                           name_prefix: Optional[str] = None) -> Player:
        """
        Create a random player with randomized attributes.
        
        Args:
            position: Specific position or None for random
            name_prefix: Prefix for player name or None for position-based
        
        Returns:
            New Player instance
        """
        if position is None:
            position = random.choice(list(Position))
        
        if name_prefix is None:
            name = f"{position.name}_{random.randint(1000, 9999)}"
        else:
            name = f"{name_prefix}_{random.randint(100, 999)}"
        
        # Generate attributes based on position
        if position == Position.GK:
            goalkeeping = random.randint(60, 95)
            defending = random.randint(20, 50)
            passing = random.randint(20, 60)
            dribbling = random.randint(10, 30)
            shooting = random.randint(10, 30)
            physical = random.randint(40, 80)
        elif position in [Position.CB, Position.SW]:
            goalkeeping = 0
            defending = random.randint(60, 95)
            passing = random.randint(30, 70)
            dribbling = random.randint(20, 50)
            shooting = random.randint(20, 50)
            physical = random.randint(50, 90)
        elif position in [Position.LB, Position.RB]:
            goalkeeping = 0
            defending = random.randint(50, 85)
            passing = random.randint(40, 80)
            dribbling = random.randint(40, 75)
            shooting = random.randint(20, 60)
            physical = random.randint(50, 85)
        elif position in [Position.DM, Position.CM]:
            goalkeeping = 0
            defending = random.randint(40, 80)
            passing = random.randint(50, 90)
            dribbling = random.randint(40, 80)
            shooting = random.randint(30, 70)
            physical = random.randint(50, 85)
        elif position in [Position.LM, Position.RM, Position.LWB, Position.RWB, Position.WB]:
            goalkeeping = 0
            defending = random.randint(30, 70)
            passing = random.randint(50, 85)
            dribbling = random.randint(50, 85)
            shooting = random.randint(30, 70)
            physical = random.randint(45, 80)
        elif position == Position.AM:
            goalkeeping = 0
            defending = random.randint(20, 60)
            passing = random.randint(60, 95)
            dribbling = random.randint(60, 90)
            shooting = random.randint(40, 80)
            physical = random.randint(40, 75)
        else:  # ST, LW, RW
            goalkeeping = 0
            defending = random.randint(20, 50)
            passing = random.randint(40, 80)
            dribbling = random.randint(50, 90)
            shooting = random.randint(60, 95)
            physical = random.randint(50, 85)
        
        return Player(
            name=name,
            position=position,
            goalkeeping=goalkeeping,
            defending=defending,
            passing=passing,
            dribbling=dribbling,
            shooting=shooting,
            physical=physical
        )
    
    def create_manual_player(self) -> Optional[Player]:
        """Create a player through user input."""
        print("\n=== Create New Player ===")
        
        name = input("Enter player name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return None
        
        # Select position
        print("\nAvailable positions:")
        positions = list(Position)
        for i, pos in enumerate(positions, 1):
            print(f"{i}. {pos.name} - {pos.value}")
        
        try:
            pos_idx = int(input("Select position (number): ")) - 1
            if pos_idx < 0 or pos_idx >= len(positions):
                print("Invalid position selection!")
                return None
            position = positions[pos_idx]
        except ValueError:
            print("Invalid input!")
            return None
        
        # Get attributes
        print("\nEnter attributes (0-100):")
        try:
            if position == Position.GK:
                goalkeeping = int(input("Goalkeeping: "))
            else:
                goalkeeping = 0
                print("Goalkeeping: 0 (not a goalkeeper)")
            
            defending = int(input("Defending: "))
            passing = int(input("Passing: "))
            dribbling = int(input("Dribbling: "))
            shooting = int(input("Shooting: "))
            physical = int(input("Physical: "))
            
            # Validate ranges
            attrs = [goalkeeping, defending, passing, dribbling, shooting, physical]
            if any(a < 0 or a > 100 for a in attrs):
                print("All attributes must be between 0 and 100!")
                return None
            
        except ValueError:
            print("Invalid input! Attributes must be numbers.")
            return None
        
        return Player(
            name=name,
            position=position,
            goalkeeping=goalkeeping,
            defending=defending,
            passing=passing,
            dribbling=dribbling,
            shooting=shooting,
            physical=physical
        )
    
    def generate_player_pool(self, count: int, ensure_all_positions: bool = True) -> List[Player]:
        """
        Generate a pool of random players.
        
        Args:
            count: Number of players to generate
            ensure_all_positions: If True, ensures at least 2 per position
        
        Returns:
            List of generated players
        """
        players = []
        
        if ensure_all_positions:
            # Ensure at least 2 players per position
            positions = list(Position)
            for pos in positions:
                players.append(self.create_random_player(pos))
                players.append(self.create_random_player(pos))
            
            # Fill remaining slots randomly
            while len(players) < count:
                players.append(self.create_random_player())
        else:
            # Generate completely random players
            for _ in range(count):
                players.append(self.create_random_player())
        
        return players
    
    def find_players_by_position(self, position: Position) -> List[Player]:
        """Find all players with a specific position."""
        return [p for p in self.players if p.position == position]
    
    def find_players_by_name(self, name_part: str) -> List[Player]:
        """Find players whose name contains the given string."""
        name_lower = name_part.lower()
        return [p for p in self.players if name_lower in p.name.lower()]
    
    def get_top_players(self, count: int = 10) -> List[Player]:
        """Get top players by overall rating."""
        return sorted(self.players, key=lambda p: p.overall_rating(), reverse=True)[:count]
    
    def display_player_stats(self, player: Player) -> None:
        """Display detailed player statistics."""
        print(f"\n{'='*50}")
        print(f"Name: {player.name}")
        print(f"Position: {player.position.value}")
        print(f"Overall Rating: {player.overall_rating():.0f}")
        print(f"\nAttributes:")
        print(f"  Goalkeeping: {player.goalkeeping}")
        print(f"  Defending:   {player.defending}")
        print(f"  Passing:     {player.passing}")
        print(f"  Dribbling:   {player.dribbling}")
        print(f"  Shooting:    {player.shooting}")
        print(f"  Physical:    {player.physical}")
        print(f"{'='*50}")