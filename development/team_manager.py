"""
Team Manager
~~~~~~~~~~~~

Module for creating and managing teams in the Fantasy Football system.
"""

import json
import random
from typing import List, Optional, Dict, Tuple
from models import Team, Player, Position, TacticalStyle, FORMATIONS, POSITION_GROUPS
from player_manager import PlayerManager


class TeamManager:
    """Manages team creation, loading, and saving."""
    
    def __init__(self, filename: str = "teams.json"):
        self.filename = filename
        self.teams: List[Team] = []
        self.load_teams()
    
    def load_teams(self) -> None:
        """Load teams from JSON file."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.teams = [Team.from_dict(t) for t in data]
        except FileNotFoundError:
            self.teams = []
    
    def save_teams(self) -> None:
        """Save teams to JSON file."""
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.teams], f, indent=2)
    
    def add_team(self, team: Team) -> None:
        """Add a team to the roster."""
        self.teams.append(team)
        self.save_teams()
    
    def create_random_team(self, name: str, player_pool: List[Player],
                          formation: Optional[str] = None,
                          style: Optional[TacticalStyle] = None) -> Optional[Team]:
        """
        Create a random team from available players.
        
        Args:
            name: Team name
            player_pool: Pool of available players
            formation: Specific formation or None for random
            style: Tactical style or None for random
        
        Returns:
            Team instance or None if not enough players
        """
        if formation is None:
            formation = random.choice(list(FORMATIONS.keys()))
        
        if style is None:
            style = random.choice(list(TacticalStyle))
        
        if formation not in FORMATIONS:
            print(f"Unknown formation: {formation}")
            return None
        
        # Get position requirements
        requirements = FORMATIONS[formation]
        selected_players = []
        available_players = player_pool.copy()
        
        # Try to fill each position requirement
        for position, count in requirements.items():
            # Find players for this position
            candidates = [p for p in available_players if p.position == position]
            
            if len(candidates) < count:
                # Try to find similar positions
                if position in [Position.LB, Position.RB]:
                    # Wing backs can play as full backs
                    candidates.extend([p for p in available_players 
                                     if p.position in [Position.WB, Position.LWB, Position.RWB] 
                                     and p not in candidates])
                elif position in [Position.LWB, Position.RWB]:
                    # Full backs can play as wing backs
                    candidates.extend([p for p in available_players 
                                     if p.position in [Position.LB, Position.RB, Position.WB] 
                                     and p not in candidates])
                elif position == Position.DM:
                    # CMs can play as DMs
                    candidates.extend([p for p in available_players 
                                     if p.position == Position.CM and p not in candidates])
                elif position == Position.AM:
                    # CMs can play as AMs
                    candidates.extend([p for p in available_players 
                                     if p.position == Position.CM and p not in candidates])
            
            if len(candidates) < count:
                print(f"Not enough players for position {position.name} (need {count}, have {len(candidates)})")
                return None
            
            # Select best players for position
            candidates.sort(key=lambda p: p.overall_rating(), reverse=True)
            for i in range(count):
                selected_players.append(candidates[i])
                available_players.remove(candidates[i])
        
        team = Team(
            name=name,
            formation=formation,
            players=selected_players,
            style=style
        )
        
        return team
    
    def create_manual_team(self, player_pool: List[Player]) -> Optional[Team]:
        """Create a team through user input."""
        print("\n=== Create New Team ===")
        
        name = input("Enter team name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return None
        
        # Select formation
        print("\nAvailable formations:")
        formations = list(FORMATIONS.keys())
        for i, form in enumerate(formations, 1):
            positions = FORMATIONS[form]
            pos_str = ", ".join(f"{k.name}:{v}" for k, v in positions.items())
            print(f"{i}. {form}: {pos_str}")
        
        print(f"{len(formations) + 1}. Custom (select 11 players manually)")
        
        try:
            choice = int(input("Select formation (number): "))
            if choice < 1 or choice > len(formations) + 1:
                print("Invalid choice!")
                return None
        except ValueError:
            print("Invalid input!")
            return None
        
        # Select tactical style
        print("\nAvailable tactical styles:")
        styles = list(TacticalStyle)
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            style_idx = int(input("Select tactical style (number): ")) - 1
            if style_idx < 0 or style_idx >= len(styles):
                print("Invalid style selection!")
                return None
            style = styles[style_idx]
        except ValueError:
            print("Invalid input!")
            return None
        
        selected_players = []
        available_players = player_pool.copy()
        
        if choice <= len(formations):
            # Use predefined formation
            formation = formations[choice - 1]
            requirements = FORMATIONS[formation]
            
            print(f"\nBuilding {formation} formation...")
            
            for position, count in requirements.items():
                for i in range(count):
                    print(f"\nSelect {position.name} ({i+1}/{count}):")
                    
                    # Show available players for this position
                    candidates = [p for p in available_players if p.position == position]
                    
                    # Add compatible positions
                    if position in [Position.LB, Position.RB]:
                        candidates.extend([p for p in available_players 
                                         if p.position in [Position.WB, Position.LWB, Position.RWB] 
                                         and p not in candidates])
                    
                    if not candidates:
                        print(f"No available players for position {position.name}!")
                        return None
                    
                    for j, player in enumerate(candidates, 1):
                        print(f"{j}. {player.name} ({player.position.name}) - "
                              f"OVR: {player.overall_rating():.0f}")
                    
                    try:
                        p_idx = int(input("Select player (number): ")) - 1
                        if p_idx < 0 or p_idx >= len(candidates):
                            print("Invalid selection!")
                            return None
                        
                        selected = candidates[p_idx]
                        selected_players.append(selected)
                        available_players.remove(selected)
                    except ValueError:
                        print("Invalid input!")
                        return None
        else:
            # Custom formation
            formation = "Custom"
            
            print("\nSelect 11 players:")
            while len(selected_players) < 11:
                print(f"\nPlayer {len(selected_players) + 1}/11")
                
                # Group players by position type
                for group_name, positions in POSITION_GROUPS.items():
                    group_players = [p for p in available_players 
                                   if p.position in positions]
                    if group_players:
                        print(f"\n{group_name}:")
                        for i, player in enumerate(group_players, 1):
                            print(f"  {i}. {player.name} ({player.position.name}) - "
                                  f"OVR: {player.overall_rating():.0f}")
                
                try:
                    player_name = input("Enter player name (or number from above): ").strip()
                    
                    # Try to find player by name
                    found = None
                    for p in available_players:
                        if p.name.lower() == player_name.lower():
                            found = p
                            break
                    
                    if found:
                        selected_players.append(found)
                        available_players.remove(found)
                    else:
                        print("Player not found!")
                except Exception as e:
                    print(f"Error: {e}")
        
        team = Team(
            name=name,
            formation=formation,
            players=selected_players,
            style=style
        )
        
        # Validate team
        is_valid, message = team.validate_formation()
        if not is_valid:
            print(f"Invalid team: {message}")
            return None
        
        return team
    
    def find_team_by_name(self, name: str) -> Optional[Team]:
        """Find a team by name."""
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return None
    
    def get_team_rankings(self) -> List[Team]:
        """Get teams ranked by Elo rating."""
        return sorted(self.teams, key=lambda t: t.elo_rating, reverse=True)
    
    def update_team_elo(self, team1_name: str, team2_name: str, 
                       score: Tuple[int, int], k: float = 20.0) -> bool:
        """
        Update Elo ratings after a match.
        
        Args:
            team1_name: Name of first team
            team2_name: Name of second team
            score: Tuple of (team1_goals, team2_goals)
            k: Elo K-factor
        
        Returns:
            True if successful, False otherwise
        """
        team1 = self.find_team_by_name(team1_name)
        team2 = self.find_team_by_name(team2_name)
        
        if not team1 or not team2:
            return False
        
        # Calculate expected scores
        expected1 = 1 / (1 + 10 ** ((team2.elo_rating - team1.elo_rating) / 400))
        expected2 = 1 - expected1
        
        # Actual scores
        if score[0] > score[1]:
            actual1, actual2 = 1.0, 0.0
            team1.streak_count = max(1, team1.streak_count + 1)
            team2.streak_count = min(-1, team2.streak_count - 1)
        elif score[0] < score[1]:
            actual1, actual2 = 0.0, 1.0
            team1.streak_count = min(-1, team1.streak_count - 1)
            team2.streak_count = max(1, team2.streak_count + 1)
        else:
            actual1, actual2 = 0.5, 0.5
            team1.streak_count = 0
            team2.streak_count = 0
        
        # Update ratings
        team1.elo_rating += k * (actual1 - expected1)
        team2.elo_rating += k * (actual2 - expected2)
        
        self.save_teams()
        return True
    
    def display_team_rankings(self) -> None:
        """Display current team rankings."""
        rankings = self.get_team_rankings()
        
        print("\n=== Team Rankings ===")
        print(f"{'Rank':<6}{'Team':<20}{'Elo':<8}{'W/L Streak':<12}{'Formation':<10}{'Style':<12}")
        print("-" * 76)
        
        for i, team in enumerate(rankings, 1):
            streak_str = f"{abs(team.streak_count)}W" if team.streak_count > 0 else \
                        f"{abs(team.streak_count)}L" if team.streak_count < 0 else "-"
            
            print(f"{i:<6}{team.name:<20}{team.elo_rating:<8.0f}"
                  f"{streak_str:<12}{team.formation:<10}{team.style.name:<12}")