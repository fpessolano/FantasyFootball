#!/usr/bin/env python3
"""
Player Menu - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all player management functionality.
"""

from core.models import Position
class PlayerService:
    """Service for player management operations."""
    
    def __init__(self, player_manager):
        self.player_manager = player_manager
    
    def view_all_players(self):
        """Display all players."""
        if not self.player_manager.players:
            print("\nNo players found!")
            return
        
        print(f"\nTotal players: {len(self.player_manager.players)}")
        
        # Group by position
        by_position = {}
        for player in self.player_manager.players:
            if player.position not in by_position:
                by_position[player.position] = []
            by_position[player.position].append(player)
        
        for position in sorted(by_position.keys(), key=lambda p: p.name):
            print(f"\n{position.name} ({len(by_position[position])} players):")
            for player in sorted(by_position[position], 
                               key=lambda p: p.overall_rating(), reverse=True)[:5]:
                print(f"  {player.name:<20} OVR: {player.overall_rating():.0f}")
    
    def create_random_player(self):
        """Create a random player."""
        print("\nCreate Random Player")
        print("Select position (or 0 for random):")
        
        positions = list(Position)
        for i, pos in enumerate(positions, 1):
            print(f"{i}. {pos.name}")
        
        choice = input("\nEnter choice: ").strip()
        
        position = None
        if choice != "0":
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(positions):
                    position = positions[idx]
            except ValueError:
                pass
        
        # Nationality selection
        print("\nSelect nationality (or Enter for random):")
        available_nationalities = [
            'Brazilian', 'Spanish', 'French', 'German', 'Italian', 'Portuguese',
            'British', 'American', 'Dutch', 'Russian', 'Polish', 'Swedish',
            'Norwegian', 'Danish', 'Finnish', 'Japanese', 'Korean', 'Chinese',
            'Turkish', 'Greek', 'Hebrew'
        ]
        
        for i, nat in enumerate(available_nationalities, 1):
            print(f"{i:2}. {nat}")
        
        nat_choice = input("\nEnter nationality choice (or Enter for random): ").strip()
        
        nationality = None
        if nat_choice:
            try:
                idx = int(nat_choice) - 1
                if 0 <= idx < len(available_nationalities):
                    nationality = available_nationalities[idx]
            except ValueError:
                pass
        
        if nationality:
            player = self.player_manager.create_player_by_nationality(position, nationality)
        else:
            player = self.player_manager.create_random_player(position)
        
        self.player_manager.add_player(player)
        
        print(f"\nCreated player:")
        self.player_manager.display_player_stats(player)
    
    def create_manual_player(self):
        """Create a player manually."""
        player = self.player_manager.create_manual_player()
        if player:
            self.player_manager.add_player(player)
            print(f"\nCreated player:")
            self.player_manager.display_player_stats(player)
    
    def generate_player_pool(self):
        """Generate multiple random players."""
        try:
            count = int(input("How many players to generate? "))
            if count < 1:
                print("Count must be positive!")
                return
        except ValueError:
            print("Invalid number!")
            return
        
        players = self.player_manager.generate_player_pool(count)
        for player in players:
            self.player_manager.add_player(player)
        
        print(f"\nGenerated {len(players)} players successfully!")
    
    def search_players(self):
        """Search for players with multiple criteria."""
        print("\n=== Player Search ===")
        print("1. Search by Name")
        print("2. Search by Nationality")
        print("3. Search by Position")
        print("4. Advanced Search (Multiple Criteria)")
        
        try:
            choice = int(input("Select search type (1-4): "))
        except ValueError:
            choice = 1
        
        if choice == 1:
            # Search by name
            search_term = input("Enter player name (partial): ").strip()
            if not search_term:
                return
            
            found = self.player_manager.find_players_by_name(search_term)
            if not found:
                print("No players found!")
                return
            
            print(f"\nFound {len(found)} players:")
            for player in found:
                print(f"  {player.name} ({player.position.name}) - {player.nationality} - OVR: {player.overall_rating():.0f}")
        
        elif choice == 2:
            # Search by nationality
            distribution = self.player_manager.get_nationality_distribution()
            print("\n=== Available Nationalities ===")
            sorted_nationalities = sorted(distribution.items())
            for i, (nationality, count) in enumerate(sorted_nationalities, 1):
                print(f"{i:2}. {nationality}: {count} players")
            
            nationality_input = input("\nEnter nationality (name or number): ").strip()
            if not nationality_input:
                return
            
            # Check if input is a number
            nationality = None
            try:
                choice_num = int(nationality_input)
                if 1 <= choice_num <= len(sorted_nationalities):
                    nationality = sorted_nationalities[choice_num - 1][0]
                else:
                    print(f"Invalid number! Please choose 1-{len(sorted_nationalities)}")
                    return
            except ValueError:
                # Input is a nationality name
                nationality = nationality_input
            
            found = self.player_manager.find_players_by_nationality(nationality)
            if not found:
                print(f"No {nationality} players found!")
                return
            
            print(f"\nFound {len(found)} {nationality} players:")
            # Group by position
            from collections import defaultdict
            by_position = defaultdict(list)
            for player in found:
                by_position[player.position.name].append(player)
            
            for position, players in sorted(by_position.items()):
                print(f"\n  {position} ({len(players)}):")
                for player in sorted(players, key=lambda p: p.overall_rating(), reverse=True):
                    print(f"    {player.name} - OVR: {player.overall_rating():.0f}")
        
        elif choice == 3:
            # Search by position
            positions = [pos.name for pos in Position]
            print("\n=== Available Positions ===")
            for i, pos in enumerate(positions, 1):
                print(f"{i:2}. {pos}")
            
            try:
                pos_choice = int(input("Select position (number): "))
                if 1 <= pos_choice <= len(positions):
                    position_name = positions[pos_choice - 1]
                else:
                    print("Invalid choice!")
                    return
            except ValueError:
                print("Invalid input!")
                return
            
            found = [p for p in self.player_manager.players if p.position.name == position_name]
            if not found:
                print(f"No {position_name} players found!")
                return
            
            # Sort by rating
            found.sort(key=lambda p: p.overall_rating(), reverse=True)
            
            print(f"\nFound {len(found)} {position_name} players:")
            for player in found[:20]:  # Show top 20
                print(f"  {player.name} ({player.nationality}) - OVR: {player.overall_rating():.0f}")
        
        elif choice == 4:
            # Advanced search with multiple criteria
            print("\n=== Advanced Search ===")
            print("Enter criteria (leave empty to skip):")
            
            # Get search criteria
            name_filter = input("Name contains: ").strip().lower()
            
            # Show available nationalities
            distribution = self.player_manager.get_nationality_distribution()
            print("\nAvailable Nationalities:")
            sorted_nationalities = sorted(distribution.items())
            for i, (nationality, count) in enumerate(sorted_nationalities, 1):
                print(f"{i:2}. {nationality}: {count} players")
            
            nationality_input = input("\nNationality (name or number, or Enter to skip): ").strip()
            nationality_filter = ""
            if nationality_input:
                try:
                    choice_num = int(nationality_input)
                    if 1 <= choice_num <= len(sorted_nationalities):
                        nationality_filter = sorted_nationalities[choice_num - 1][0]
                    else:
                        print(f"Invalid number! Using text search.")
                        nationality_filter = nationality_input
                except ValueError:
                    nationality_filter = nationality_input
            
            # Show available positions
            print("\nAvailable Positions:")
            positions = list(Position)
            for i, pos in enumerate(positions, 1):
                print(f"{i:2}. {pos.name}")
            
            position_input = input("\nPosition (name or number, or Enter to skip): ").strip()
            position_filter = ""
            if position_input:
                try:
                    choice_num = int(position_input)
                    if 1 <= choice_num <= len(positions):
                        position_filter = positions[choice_num - 1].name
                    else:
                        print(f"Invalid number! Using text search.")
                        position_filter = position_input.upper()
                except ValueError:
                    position_filter = position_input.upper()
            
            try:
                min_rating = input("Minimum overall rating: ").strip()
                min_rating = float(min_rating) if min_rating else 0
            except ValueError:
                min_rating = 0
            
            try:
                max_rating = input("Maximum overall rating: ").strip()
                max_rating = float(max_rating) if max_rating else 100
            except ValueError:
                max_rating = 100
            
            # Apply filters
            found = []
            for player in self.player_manager.players:
                # Name filter
                if name_filter and name_filter not in player.name.lower():
                    continue
                
                # Nationality filter
                if nationality_filter and nationality_filter.lower() != player.nationality.lower():
                    continue
                
                # Position filter
                if position_filter and position_filter != player.position.name:
                    continue
                
                # Rating filter
                rating = player.overall_rating()
                if not (min_rating <= rating <= max_rating):
                    continue
                
                found.append(player)
            
            if not found:
                print("No players match the criteria!")
                return
            
            # Sort by rating
            found.sort(key=lambda p: p.overall_rating(), reverse=True)
            
            print(f"\nFound {len(found)} players matching criteria:")
            for player in found[:30]:  # Show top 30
                print(f"  {player.name} ({player.nationality}) - {player.position.name} - OVR: {player.overall_rating():.0f}")
        
        else:
            print("Invalid choice!")
            return
    
    def view_top_players(self):
        """View top players by rating."""
        try:
            count = int(input("How many top players to show? [10]: ") or "10")
        except ValueError:
            count = 10
        
        top_players = self.player_manager.get_top_players(count)
        
        print(f"\nTop {len(top_players)} Players:")
        print(f"{'Rank':<6}{'Name':<20}{'Position':<10}{'OVR':<6}")
        print("-" * 42)
        
        for i, player in enumerate(top_players, 1):
            print(f"{i:<6}{player.name:<20}{player.position.name:<10}"
                  f"{player.overall_rating():<6.0f}")