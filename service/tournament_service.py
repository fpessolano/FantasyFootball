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
            team_names = [team.name for team in selected_teams]
            tournament = self.tournament_manager.create_tournament(tournament_name, team_names)
            if tournament:
                # Clear success message without extra details
                self._clear_screen()
                print(f"✅ Tournament '{tournament_name}' created with {num_teams} teams!")
                input("\nPress Enter to view bracket and start playing...")
                # Automatically start the tournament
                self._play_tournament_interactive(tournament)
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
                self._play_tournament_interactive(tournament)
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
            status = "Completed" if tournament.completed else "Active"
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
            status = "✅ Completed" if tournament.completed else "🏃 Active"
            winner = f" (Winner: {tournament.winner})" if tournament.completed and tournament.winner else ""
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
            status = "Completed" if tournament.completed else "Active"
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
    
    def _play_tournament_interactive(self, tournament):
        """Play tournament interactively match by match."""
        # Clear screen and show initial bracket
        self._clear_screen()
        self.tournament_manager.display_bracket(tournament)
        input("\nPress Enter to start playing matches...")
        
        while not tournament.completed:
            current_round = tournament.get_current_round()
            if not current_round:
                # Tournament complete - clear screen and show final results
                self._clear_screen()
                print("🏆 TOURNAMENT COMPLETE! 🏆\n")
                self.tournament_manager.display_bracket(tournament)
                break
            
            # Get all matches in current round that need to be played
            available_matches = [m for m in current_round.matches if not m.completed and m.home_team and m.away_team and not m.home_team.startswith('BYE') and not m.away_team.startswith('BYE')]
            
            if not available_matches:
                # Check if round is complete
                if all(m.completed or m.home_team.startswith('BYE') or m.away_team.startswith('BYE') for m in current_round.matches):
                    print(f"\n✅ Round {current_round.round_name} Complete!")
                    self.tournament_manager._advance_to_next_round(tournament, current_round)
                    
                    # Show updated bracket after round completion
                    if not tournament.completed:
                        input("\nRound complete! Press Enter to see updated bracket...")
                        self._clear_screen()
                        next_round_name = tournament.get_current_round().round_name if tournament.get_current_round() else 'Final'
                        print(f"Advancing to {next_round_name}...\n")
                        self.tournament_manager.display_bracket(tournament)
                        input("\nPress Enter to continue...")
                    continue
                else:
                    print("No matches available to play!")
                    break
            
            # Clear screen and show current round status
            self._clear_screen()
            print(f"🏆 {tournament.name} - {current_round.round_name}")
            print("=" * 50)
            
            # Show all matches in this round with their status
            print("\nMatches in this round:")
            for i, match in enumerate(current_round.matches, 1):
                if match.home_team and match.away_team and not match.home_team.startswith('BYE') and not match.away_team.startswith('BYE'):
                    if match.completed:
                        print(f"  ✅ {match.home_team} {match.home_score}-{match.away_score} {match.away_team} (Winner: {match.winner})")
                    else:
                        print(f"  ⏳ {match.home_team} vs {match.away_team} - PENDING")
                elif match.home_team and match.home_team.startswith('BYE'):
                    print(f"  ➡️  {match.away_team} - Advances automatically (BYE)")
                elif match.away_team and match.away_team.startswith('BYE'):
                    print(f"  ➡️  {match.home_team} - Advances automatically (BYE)")
            
            # Get next match to play
            next_match = available_matches[0]
            print(f"\n⚽ NEXT MATCH: {next_match.home_team} vs {next_match.away_team}")
            
            # Ask user if they want to continue
            try:
                response = input("\nPlay this match? (Enter to play, q to quit): ").strip().lower()
                if response == 'q':
                    print("Tournament paused. Use 'Continue Existing Tournament' to resume later.")
                    break
                else:  # Enter or any other key (default to yes)
                    self._play_single_match(tournament, next_match)
            except KeyboardInterrupt:
                print("\nTournament paused. Use 'Continue Existing Tournament' to resume.")
                break
    
    def _play_single_match(self, tournament, match):
        """Play a single tournament match."""
        print(f"\n{'='*60}")
        print(f"TOURNAMENT MATCH: {match.home_team} vs {match.away_team}")
        print(f"{'='*60}")
        
        try:
            # Import match engine
            from core.engines.match_engine import MatchEngine
            
            # Get team objects
            home_team_obj = None
            away_team_obj = None
            
            for team in self.team_manager.teams:
                if team.name == match.home_team:
                    home_team_obj = team
                if team.name == match.away_team:
                    away_team_obj = team
            
            if not home_team_obj:
                print(f"❌ Error: Could not find home team '{match.home_team}'")
                return
            
            if not away_team_obj:
                print(f"❌ Error: Could not find away team '{match.away_team}'")
                return
            
            # Show team info before match (like single matches)
            print(f"\n🏀 HOME: {match.home_team}")
            print(f"   Formation: {home_team_obj.formation} | Style: {home_team_obj.style.name}")
            print(f"   Elo: {home_team_obj.elo_rating:.0f}")
            
            print(f"\n✈️ AWAY: {match.away_team}")
            print(f"   Formation: {away_team_obj.formation} | Style: {away_team_obj.style.name}")
            print(f"   Elo: {away_team_obj.elo_rating:.0f}")
            
            input("\nPress Enter to simulate match...")
            
            # Create match engine and simulate
            engine = MatchEngine()
            match_result = engine.simulate_match(home_team_obj, away_team_obj)
            
            # Display detailed match result (same as single matches)
            engine.display_match_result(match_result)
            
            # Update tournament match
            match.home_score = match_result.home_score
            match.away_score = match_result.away_score
            
            # Determine winner from scores
            if match_result.home_score > match_result.away_score:
                match.winner = match.home_team
            elif match_result.away_score > match_result.home_score:
                match.winner = match.away_team
            else:
                # Handle draws - for tournaments, we need a winner
                match.winner = self._resolve_draw(match.home_team, match.away_team)
            
            match.completed = True
            
            # Show tournament context after detailed match
            print(f"\n⚽ TOURNAMENT MATCH COMPLETE")
            
            # Check if this is the final match
            current_round = tournament.get_current_round()
            if current_round and current_round.round_name.lower() == 'final':
                print(f"🏆 CHAMPION: {match.winner} wins the tournament!")
                print(f"🎆 {match.winner} are the champions!")
            else:
                print(f"🏆 Winner: {match.winner} advances to next round!")
            
            # Save tournament state
            self.tournament_manager.save_tournaments()
            
            input("\nPress Enter to continue...")
            
        except ImportError as e:
            print(f"❌ Error importing match engine: {e}")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"❌ Error playing match: {e}")
            input("Press Enter to continue...")
    
    def _clear_screen(self):
        """Clear the screen for better visual flow."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _resolve_draw(self, home_team, away_team):
        """Resolve a draw using penalty shootout simulation."""
        import random
        print(f"\n⚽ Match is tied! Going to penalty shootout...")
        
        # Simple penalty shootout simulation
        home_penalties = random.randint(3, 5)  # 3-5 penalties scored
        away_penalties = random.randint(3, 5)
        
        # Ensure there's a winner
        while home_penalties == away_penalties:
            home_penalties = random.randint(3, 5)
            away_penalties = random.randint(3, 5)
        
        winner = home_team if home_penalties > away_penalties else away_team
        print(f"Penalty Shootout: {home_team} {home_penalties}-{away_penalties} {away_team}")
        print(f"Winner: {winner}")
        
        return winner