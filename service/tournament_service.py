#!/usr/bin/env python3
"""
Tournament Menu - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all tournament management functionality.
"""

class TournamentService:
    """Service for tournament management operations."""
    
    def __init__(self, tournament_manager, team_manager, player_manager):
        self.tournament_manager = tournament_manager
        self.team_manager = team_manager
        self.player_manager = player_manager
    
    def create_tournament(self):
        """Create a new tournament."""
        print("=" * 70)
        print("🏆 CREATE NEW TOURNAMENT")
        print("=" * 70)
        
        tournament_name = input("\nEnter tournament name: ").strip()
        if not tournament_name:
            print("Tournament name cannot be empty!")
            return
        
        # Get number of teams
        try:
            num_teams = int(input("Enter number of teams (must be power of 2, e.g., 4, 8, 16): "))
            if num_teams < 2:
                print("Need at least 2 teams!")
                return
        except ValueError:
            print("Invalid number!")
            return
        
        # Check if we have enough teams
        if len(self.team_manager.teams) < num_teams:
            print(f"Not enough teams! You have {len(self.team_manager.teams)}, need {num_teams}")
            return
        
        # Team selection options
        print("\nTeam selection:")
        print("1. Select teams manually")
        print("2. Use random teams")
        
        try:
            selection_choice = int(input("Choose option (1-2): "))
        except ValueError:
            selection_choice = 2
        
        if selection_choice == 1:
            # Manual team selection
            selected_teams = self._select_teams_manually(num_teams)
        else:
            # Random team selection
            import random
            selected_teams = random.sample(self.team_manager.teams, num_teams)
        
        if len(selected_teams) != num_teams:
            print("Failed to select enough teams!")
            return
        
        # Create tournament
        try:
            tournament = self.tournament_manager.create_tournament(tournament_name, selected_teams)
            if tournament:
                print(f"\n✅ Tournament '{tournament_name}' created successfully!")
                print(f"Teams: {num_teams}")
            else:
                print("\n❌ Failed to create tournament.")
        except Exception as e:
            print(f"\n❌ Error creating tournament: {e}")
    
    def continue_tournament(self):
        """Continue an existing tournament."""
        tournaments = self.tournament_manager.get_active_tournaments()
        if not tournaments:
            print("No active tournaments found!")
            return
        
        print("\nActive tournaments:")
        for i, tournament in enumerate(tournaments, 1):
            print(f"{i}. {tournament.name}")
        
        try:
            choice = int(input("Select tournament to continue: ")) - 1
            if 0 <= choice < len(tournaments):
                tournament = tournaments[choice]
                self.tournament_manager.continue_tournament(tournament)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def view_tournament_bracket(self):
        """View tournament bracket."""
        tournaments = self.tournament_manager.get_all_tournaments()
        if not tournaments:
            print("No tournaments found!")
            return
        
        print("\nAvailable tournaments:")
        for i, tournament in enumerate(tournaments, 1):
            status = "Completed" if tournament.is_complete else "Active"
            print(f"{i}. {tournament.name} ({status})")
        
        try:
            choice = int(input("Select tournament to view: ")) - 1
            if 0 <= choice < len(tournaments):
                tournament = tournaments[choice]
                self.tournament_manager.display_bracket(tournament)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def show_tournament_list(self):
        """Show list of all tournaments."""
        tournaments = self.tournament_manager.get_all_tournaments()
        if not tournaments:
            print("No tournaments found!")
            return
        
        print("\n=== Tournament List ===")
        for tournament in tournaments:
            status = "✅ Completed" if tournament.is_complete else "🏃 Active"
            winner = f" (Winner: {tournament.winner})" if tournament.is_complete and tournament.winner else ""
            print(f"{status} {tournament.name}{winner}")
    
    def rename_tournament(self):
        """Rename a tournament."""
        tournaments = self.tournament_manager.get_all_tournaments()
        if not tournaments:
            print("No tournaments found!")
            return
        
        print("\nAvailable tournaments:")
        for i, tournament in enumerate(tournaments, 1):
            print(f"{i}. {tournament.name}")
        
        try:
            choice = int(input("Select tournament to rename: ")) - 1
            if 0 <= choice < len(tournaments):
                tournament = tournaments[choice]
                new_name = input(f"Enter new name for '{tournament.name}': ").strip()
                if new_name and new_name != tournament.name:
                    old_name = tournament.name
                    tournament.name = new_name
                    self.tournament_manager.save_tournaments()
                    print(f"Tournament renamed from '{old_name}' to '{new_name}'!")
                else:
                    print("Name unchanged.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def delete_tournament(self):
        """Delete a tournament."""
        tournaments = self.tournament_manager.get_all_tournaments()
        if not tournaments:
            print("No tournaments found!")
            return
        
        print("\nAvailable tournaments:")
        for i, tournament in enumerate(tournaments, 1):
            status = "Completed" if tournament.is_complete else "Active"
            print(f"{i}. {tournament.name} ({status})")
        
        try:
            choice = int(input("Select tournament to delete: ")) - 1
            if 0 <= choice < len(tournaments):
                tournament = tournaments[choice]
                confirm = input(f"Delete tournament '{tournament.name}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    self.tournament_manager.delete_tournament(tournament)
                    print(f"Tournament '{tournament.name}' deleted!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def _select_teams_manually(self, num_teams):
        """Helper to manually select teams."""
        selected_teams = []
        available_teams = self.team_manager.teams.copy()
        
        print(f"\nSelect {num_teams} teams:")
        
        for i in range(num_teams):
            if not available_teams:
                break
                
            print(f"\nSelect team {i + 1}:")
            for j, team in enumerate(available_teams, 1):
                print(f"{j}. {team.name}")
            
            try:
                choice = int(input("Choose team: ")) - 1
                if 0 <= choice < len(available_teams):
                    selected_team = available_teams.pop(choice)
                    selected_teams.append(selected_team)
                    print(f"Selected: {selected_team.name}")
                else:
                    print("Invalid choice! Skipping...")
            except ValueError:
                print("Invalid input! Skipping...")
        
        return selected_teams