"""
Team Manager
~~~~~~~~~~~~

Module for creating and managing teams in the Fantasy Football system.
"""

import json
import random
from typing import List, Optional, Dict, Tuple
from core.models import Team, Player, Position, TacticalStyle, FORMATIONS, POSITION_GROUPS
from core.managers.player_manager import PlayerManager


class TeamManager:
    """Manages team creation, loading, and saving."""
    
    def __init__(self, filename: str = "data/teams.json"):
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
    
    def get_players_on_teams(self) -> List[Player]:
        """Get all players currently assigned to teams."""
        assigned_players = []
        for team in self.teams:
            assigned_players.extend(team.players)
        return assigned_players
    
    def get_available_players(self, player_pool: List[Player]) -> List[Player]:
        """Get players from pool who are not already on any team."""
        # Get names of all players currently on teams
        assigned_names = set()
        for team in self.teams:
            for player in team.players:
                assigned_names.add(player.name)
        
        # Return players from pool who are not on any team
        available = [p for p in player_pool if p.name not in assigned_names]
        return available
    
    def create_random_team(self, name: str, player_pool: List[Player],
                          formation: Optional[str] = None,
                          style: Optional[TacticalStyle] = None,
                          create_missing: bool = False,
                          nationality: Optional[str] = None) -> Optional[Team]:
        """
        Create a random team from available players.
        
        Args:
            name: Team name
            player_pool: Pool of all players
            formation: Specific formation or None for random
            style: Tactical style or None for random
        
        Returns:
            Team instance or None if not enough players
        """
        # Only use players not already on teams
        available_players = self.get_available_players(player_pool)
        
        if len(available_players) < 11 and not create_missing:
            print(f"Not enough available players! Need 11, have {len(available_players)}.")
            print("Some players may already be assigned to other teams.")
            return None
        
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
        # available_players is already filtered to exclude players on teams
        
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
                if create_missing and nationality:
                    # Create missing players for this position and nationality
                    missing_count = count - len(candidates)
                    print(f"Creating {missing_count} new {nationality} {position.name} players...")
                    
                    # Import PlayerManager to create players
                    from core.managers.player_manager import PlayerManager
                    temp_pm = PlayerManager('data/players.json')  # Use existing player file
                    
                    for _ in range(missing_count):
                        new_player = temp_pm.create_player_by_nationality(position, nationality)
                        # Ensure nationality is set correctly in case of fallback
                        new_player.nationality = nationality
                        temp_pm.add_player(new_player)  # Add to database
                        candidates.append(new_player)
                        available_players.append(new_player)
                        print(f"  Created: {new_player.name} ({position.name}) - {nationality}")
                else:
                    print(f"Not enough players for position {position.name} (need {count}, have {len(candidates)})")
                    if nationality:
                        print(f"Tip: You can create missing players by allowing player generation")
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
        
        # Only use players not already on teams
        available_players = self.get_available_players(player_pool)
        
        if len(available_players) < 11:
            print(f"Not enough available players! Need 11, have {len(available_players)}.")
            print("Some players may already be assigned to other teams.")
            return None
        
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
        # available_players already filtered above
        
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
    
    def create_national_team(self, name: str, nationality: str, player_pool: List[Player],
                           formation: Optional[str] = None,
                           style: Optional[TacticalStyle] = None,
                           create_missing: bool = False) -> Optional[Team]:
        """
        Create a team with players all from the same nationality.
        
        Args:
            name: Team name
            nationality: Target nationality (e.g., "Brazilian", "German")
            player_pool: Pool of all players
            formation: Specific formation or None for random
            style: Tactical style or None for random
            create_missing: Whether to create new players if not enough available
        
        Returns:
            Team instance or None if not enough players of that nationality
        """
        # Filter for players of the specified nationality
        nationality_players = [p for p in player_pool if p.nationality.lower() == nationality.lower()]
        available_players = self.get_available_players(nationality_players)
        
        if len(available_players) < 11:
            if create_missing:
                print(f"Only {len(available_players)} available {nationality} players. Will create missing players as needed.")
            else:
                print(f"Not enough available {nationality} players! Need 11, have {len(available_players)}.")
                print(f"Tip: You can allow creation of missing players to complete the team.")
                return None
        else:
            print(f"Creating {nationality} national team with {len(available_players)} available players")
        
        return self.create_random_team(name, available_players, formation, style, create_missing, nationality)
    
    def create_mixed_nationality_team(self, name: str, nationality_mix: Dict[str, int], 
                                    player_pool: List[Player],
                                    formation: Optional[str] = None,
                                    style: Optional[TacticalStyle] = None,
                                    create_missing: bool = False) -> Optional[Team]:
        """
        Create a team with a specific mix of nationalities.
        
        Args:
            name: Team name
            nationality_mix: Dict of nationality -> minimum count (e.g., {"Brazilian": 5, "German": 3})
            player_pool: Pool of all players
            formation: Specific formation or None for random
            style: Tactical style or None for random
        
        Returns:
            Team instance or None if requirements cannot be met
        """
        if formation is None:
            formation = random.choice(list(FORMATIONS.keys()))
        if style is None:
            style = random.choice(list(TacticalStyle))
        
        # Check if formation is valid
        if formation not in FORMATIONS:
            print(f"Unknown formation: {formation}")
            return None
        
        # Get available players
        available_players = self.get_available_players(player_pool)
        
        # Check if we have enough players of each nationality
        for nationality, min_count in nationality_mix.items():
            nat_players = [p for p in available_players if p.nationality.lower() == nationality.lower()]
            if len(nat_players) < min_count:
                if create_missing:
                    # Create missing players for this nationality
                    missing_count = min_count - len(nat_players)
                    print(f"Creating {missing_count} new {nationality} players...")
                    
                    # Import PlayerManager to create players
                    from core.managers.player_manager import PlayerManager
                    temp_pm = PlayerManager('data/players.json')
                    
                    for _ in range(missing_count):
                        # Create random position player of this nationality
                        new_player = temp_pm.create_player_by_nationality(None, nationality)
                        # Ensure nationality is set correctly in case of fallback
                        new_player.nationality = nationality
                        temp_pm.add_player(new_player)  # Add to database
                        available_players.append(new_player)
                        print(f"  Created: {new_player.name} ({new_player.position.name}) - {nationality}")
                else:
                    print(f"Not enough {nationality} players! Need {min_count}, have {len(nat_players)}.")
                    print(f"Tip: You can allow creation of missing players to complete the team.")
                    return None
        
        # Select players according to nationality requirements
        selected_players = []
        remaining_players = available_players.copy()
        
        # First, select required players from each nationality
        for nationality, min_count in nationality_mix.items():
            nat_players = [p for p in remaining_players if p.nationality.lower() == nationality.lower()]
            
            # Sort by overall rating and select best
            nat_players.sort(key=lambda p: p.overall_rating(), reverse=True)
            
            for i in range(min_count):
                selected_players.append(nat_players[i])
                remaining_players.remove(nat_players[i])
        
        # Fill remaining positions with any available players
        total_required = sum(FORMATIONS[formation].values())
        remaining_slots = total_required - len(selected_players)
        
        if remaining_slots > 0:
            # Sort remaining players by rating and fill positions
            remaining_players.sort(key=lambda p: p.overall_rating(), reverse=True)
            for i in range(min(remaining_slots, len(remaining_players))):
                selected_players.append(remaining_players[i])
        
        if len(selected_players) < total_required:
            print(f"Could not fill all positions! Have {len(selected_players)}, need {total_required}")
            return None
        
        # Create the team
        team = Team(
            name=name,
            formation=formation,
            players=selected_players,
            style=style
        )
        
        # Remove selected players from available pool
        for player in selected_players:
            if player in available_players:
                available_players.remove(player)
        
        print(f"✅ Created {name} with nationality mix:")
        nationality_count = {}
        for player in selected_players:
            nat = player.nationality
            nationality_count[nat] = nationality_count.get(nat, 0) + 1
        
        for nat, count in sorted(nationality_count.items()):
            print(f"   {nat}: {count} players")
        
        return team
    
    def create_continental_team(self, name: str, continent: str, min_players: int,
                              player_pool: List[Player], 
                              formation: Optional[str] = None,
                              style: Optional[TacticalStyle] = None,
                              create_missing: bool = False) -> Optional[Team]:
        """
        Create a team with minimum number of players from a specific continent.
        
        Args:
            name: Team name
            continent: Target continent ("Europe", "Americas", "Asia", etc.)
            min_players: Minimum number of players from that continent
            player_pool: Pool of all players
            formation: Specific formation or None for random
            style: Tactical style or None for random
        
        Returns:
            Team instance or None if requirements cannot be met
        """
        # Define continental mappings
        continental_nationalities = {
            "Europe": ["British", "French", "German", "Italian", "Spanish", "Portuguese", "Polish", 
                      "Dutch", "Swedish", "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
                      "Romanian", "Croatian", "Slovenian", "Estonian", "Latvian", "Lithuanian", 
                      "Slovak", "Icelandic", "Irish"],
            "Americas": ["American", "Brazilian"],
            "Asia": ["Turkish", "Indonesian", "Filipino"],
            "All": []  # Special case for any nationality
        }
        
        if continent not in continental_nationalities:
            print(f"Unknown continent: {continent}. Available: {list(continental_nationalities.keys())}")
            return None
        
        # Get available players
        available_players = self.get_available_players(player_pool)
        
        # Filter players from the specified continent
        if continent == "All":
            continental_players = available_players
        else:
            target_nationalities = continental_nationalities[continent]
            continental_players = [p for p in available_players 
                                 if p.nationality in target_nationalities]
        
        if len(continental_players) < min_players:
            if create_missing:
                print(f"Only {len(continental_players)} available {continent} players. Will create missing players as needed.")
            else:
                print(f"Not enough {continent} players! Need {min_players}, have {len(continental_players)}.")
                print(f"Tip: You can allow creation of missing players to complete the team.")
                return None
        
        # Create mixed team with continental requirement
        nationality_mix = {}
        
        # Count current continental players and ensure minimum
        continental_count = {}
        for player in continental_players[:min_players]:
            nat = player.nationality
            continental_count[nat] = continental_count.get(nat, 0) + 1
        
        # Set the minimum requirements
        for nat, count in continental_count.items():
            nationality_mix[nat] = count
        
        print(f"Creating {continent} team with at least {min_players} players from the continent")
        return self.create_mixed_nationality_team(name, nationality_mix, player_pool, formation, style, create_missing)
    
    def get_nationality_availability(self, player_pool: List[Player]) -> Dict[str, Dict[str, int]]:
        """
        Get availability of players by nationality and position.
        
        Returns:
            Dict of nationality -> position -> count
        """
        available_players = self.get_available_players(player_pool)
        
        availability = {}
        for player in available_players:
            nationality = player.nationality
            position = player.position.name
            
            if nationality not in availability:
                availability[nationality] = {}
            
            if position not in availability[nationality]:
                availability[nationality][position] = 0
                
            availability[nationality][position] += 1
        
        return availability
    
    def can_create_national_team(self, nationality: str, player_pool: List[Player], 
                               formation: str = "4-3-3") -> Tuple[bool, str]:
        """
        Check if a national team can be created for the given nationality.
        
        Returns:
            (can_create, reason)
        """
        if formation not in FORMATIONS:
            return False, f"Unknown formation: {formation}"
        
        requirements = FORMATIONS[formation]
        availability = self.get_nationality_availability(player_pool)
        
        if nationality not in availability:
            return False, f"No {nationality} players available"
        
        nat_availability = availability[nationality]
        
        # Check each position requirement
        for position, needed in requirements.items():
            pos_name = position.name
            available = nat_availability.get(pos_name, 0)
            
            if available < needed:
                return False, f"Not enough {nationality} {pos_name}s: need {needed}, have {available}"
        
        return True, f"Can create {nationality} team with {formation}"
    
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