#!/usr/bin/env python3
"""
Fantasy Football Manager
~~~~~~~~~~~~~~~~~~~~~~~~

Main application for the Fantasy Football simulation system.
"""

import os
import sys
from typing import Optional, List
from models import Position, TacticalStyle
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from tournament_manager import TournamentManager


class FantasyFootballApp:
    """Main application class."""
    
    def __init__(self):
        self.player_manager = PlayerManager()
        self.team_manager = TeamManager()
        self.match_engine = MatchEngine()
        self.tournament_manager = TournamentManager(self.team_manager, self.player_manager)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self, message="Press Enter to continue..."):
        """Pause and wait for user input."""
        try:
            input(f"\n{message}")
        except EOFError:
            pass
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("Welcome to FANTASY FOOTBALL MANAGER v2.0.2")
        print("="*60)
        print("\n1. Player Management")
        print("2. Team Management")
        print("3. Play Single Match")
        print("4. Play Multiple Matches")
        print("5. Play Multiple Matches (Random Teams)")
        print("6. Tournament Mode")
        print("7. View Rankings")
        print("8. Quick Play (Random Teams)")
        print("9. Settings")
        print("0. Exit")
        print("\n" + "="*60)
    
    def player_menu(self):
        """Player management submenu."""
        while True:
            self.clear_screen()
            print("=" * 60)
            print("PLAYER MANAGEMENT")
            print("=" * 60)
            print("\n1. View All Players")
            print("2. Create Random Player")
            print("3. Create Manual Player")
            print("4. Generate Player Pool")
            print("5. Search Players")
            print("6. View Top Players")
            print("0. Back to Main Menu")
            print("\n" + "=" * 60)
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                self.view_all_players()
                self.pause()
            elif choice == "2":
                self.create_random_player()
                self.pause()
            elif choice == "3":
                self.create_manual_player()
                self.pause()
            elif choice == "4":
                self.generate_player_pool()
                self.pause()
            elif choice == "5":
                self.search_players()
                self.pause()
            elif choice == "6":
                self.view_top_players()
                self.pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
                self.pause()
    
    def team_menu(self):
        """Team management submenu."""
        while True:
            self.clear_screen()
            print("=" * 60)
            print("TEAM MANAGEMENT")
            print("=" * 60)
            print("\n1. View All Teams")
            print("2. Create Random Team")
            print("3. Create Manual Team")
            print("4. View Team Details")
            print("5. Modify Team")
            print("6. Delete Team")
            print("0. Back to Main Menu")
            print("\n" + "=" * 60)
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                self.view_all_teams()
                self.pause()
            elif choice == "2":
                self.create_random_team()
                self.pause()
            elif choice == "3":
                self.create_manual_team()
                self.pause()
            elif choice == "4":
                self.view_team_details()
                self.pause()
            elif choice == "5":
                self.modify_team()
                self.pause()
            elif choice == "6":
                self.delete_team()
                self.pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
                self.pause()
    
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
        
        name_prefix = input("Name prefix (or Enter for default): ").strip() or None
        
        player = self.player_manager.create_random_player(position, name_prefix)
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
        """Search for players."""
        search_term = input("Enter player name (partial): ").strip()
        if not search_term:
            return
        
        found = self.player_manager.find_players_by_name(search_term)
        if not found:
            print("No players found!")
            return
        
        print(f"\nFound {len(found)} players:")
        for player in found:
            print(f"  {player.name} ({player.position.name}) - OVR: {player.overall_rating():.0f}")
    
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
    
    def view_all_teams(self):
        """Display all teams."""
        if not self.team_manager.teams:
            print("\nNo teams found!")
            return
        
        self.team_manager.display_team_rankings()
    
    def create_random_team(self):
        """Create a random team."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        name = input("Enter team name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        
        team = self.team_manager.create_random_team(
            name, self.player_manager.players
        )
        
        if team:
            self.team_manager.add_team(team)
            print(team.summary())
            print("\nTeam created successfully!")
    
    def create_manual_team(self):
        """Create a team manually."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        team = self.team_manager.create_manual_team(self.player_manager.players)
        
        if team:
            self.team_manager.add_team(team)
            print(team.summary())
            print("\nTeam created successfully!")
    
    def view_team_details(self):
        """View detailed team information."""
        team = self._select_team_by_number("Select team to view")
        if not team:
            return
        
        print(team.summary())
    
    def _select_team_by_number(self, prompt: str = "Select team"):
        """Helper method to select a team by number with list display."""
        if not self.team_manager.teams:
            print("\nNo teams found!")
            return None
        
        print("\nAvailable teams:")
        for i, team in enumerate(self.team_manager.teams, 1):
            print(f"{i}. {team.name}")
        
        try:
            choice = int(input(f"\n{prompt} (1-{len(self.team_manager.teams)}): ").strip())
            if not (1 <= choice <= len(self.team_manager.teams)):
                print("Invalid choice!")
                return None
            
            return self.team_manager.teams[choice - 1]
        except ValueError:
            print("Invalid input!")
            return None
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
    
    def modify_team(self):
        """Modify an existing team."""
        team = self._select_team_by_number("Select team to modify")
        if not team:
            return
        
        try:
            while True:
                self.clear_screen()
                print("=" * 60)
                print(f"MODIFY TEAM: {team.name}")
                print("=" * 60)
                print("\n1. Change Team Name")
                print("2. Change Formation")
                print("3. Change Tactical Style")
                print("4. Replace Player")
                print("5. View Current Team")
                print("0. Back")
                print("\n" + "=" * 60)
                
                choice = input("\nEnter choice: ").strip()
                
                if choice == "1":
                    self._change_team_name(team)
                elif choice == "2":
                    self._change_team_formation(team)
                elif choice == "3":
                    self._change_team_style(team)
                elif choice == "4":
                    self._replace_team_player(team)
                elif choice == "5":
                    print(team.summary())
                    self.pause()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
                    self.pause()
        except KeyboardInterrupt:
            print("\nReturning to team menu...")
            return
    
    def _change_team_name(self, team):
        """Change team name."""
        new_name = input(f"Enter new name for '{team.name}': ").strip()
        if not new_name:
            print("Name cannot be empty!")
            return
        
        # Check if name already exists
        existing = self.team_manager.find_team_by_name(new_name)
        if existing and existing != team:
            print("Team name already exists!")
            return
        
        old_name = team.name
        team.name = new_name
        self.team_manager.save_teams()
        print(f"Team name changed from '{old_name}' to '{new_name}'!")
        self.pause()
    
    def _change_team_formation(self, team):
        """Change team formation."""
        from models import FORMATIONS
        
        print("\nAvailable formations:")
        formations = list(FORMATIONS.keys())
        for i, formation in enumerate(formations, 1):
            print(f"{i}. {formation}")
        
        try:
            choice = int(input(f"\nSelect formation (1-{len(formations)}): ").strip())
            if 1 <= choice <= len(formations):
                new_formation = formations[choice - 1]
                team.formation = new_formation
                self.team_manager.save_teams()
                print(f"Formation changed to {new_formation}!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        self.pause()
    
    def _change_team_style(self, team):
        """Change team tactical style."""
        styles = list(TacticalStyle)
        
        print("\nAvailable tactical styles:")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            choice = int(input(f"\nSelect style (1-{len(styles)}): ").strip())
            if 1 <= choice <= len(styles):
                new_style = styles[choice - 1]
                team.style = new_style
                self.team_manager.save_teams()
                print(f"Tactical style changed to {new_style.name}!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        self.pause()
    
    def _get_formation_assignment(self, team):
        """Get formation position assignments for team players."""
        from models import FORMATIONS
        
        if team.formation not in FORMATIONS:
            # If formation not recognized, just use natural positions
            return {i: player.position for i, player in enumerate(team.players)}
        
        formation_req = FORMATIONS[team.formation]
        assignments = {}
        used_positions = {}
        
        # Sort players by position priority for formation
        position_priority = {
            'GK': 1, 'CB': 2, 'SW': 2, 'LB': 3, 'RB': 3,
            'LWB': 4, 'RWB': 4, 'DM': 5, 'CM': 6, 'WB': 4,
            'LM': 7, 'RM': 7, 'AM': 8, 'LW': 9, 'RW': 9, 'ST': 10
        }
        
        sorted_players = sorted(enumerate(team.players), 
                               key=lambda x: position_priority.get(x[1].position.name, 99))
        
        # Assign players to formation positions
        for player_idx, player in sorted_players:
            player_pos = player.position
            
            # Check if this position is needed in formation and not filled
            if player_pos in formation_req:
                needed = formation_req[player_pos]
                used = used_positions.get(player_pos, 0)
                
                if used < needed:
                    assignments[player_idx] = player_pos
                    used_positions[player_pos] = used + 1
                    continue
            
            # If natural position is full, find a compatible position
            compatible_positions = self._get_compatible_positions(player_pos)
            assigned = False
            
            for comp_pos in compatible_positions:
                if comp_pos in formation_req:
                    needed = formation_req[comp_pos]
                    used = used_positions.get(comp_pos, 0)
                    
                    if used < needed:
                        assignments[player_idx] = comp_pos
                        used_positions[comp_pos] = used + 1
                        assigned = True
                        break
            
            if not assigned:
                # Fallback to natural position
                assignments[player_idx] = player_pos
        
        return assignments
    
    def _get_compatible_positions(self, position):
        """Get positions compatible with the given position."""
        from models import Position
        
        compatibility = {
            Position.GK: [Position.GK],
            Position.CB: [Position.CB, Position.SW],
            Position.SW: [Position.SW, Position.CB],
            Position.LB: [Position.LB, Position.LWB, Position.WB],
            Position.RB: [Position.RB, Position.RWB, Position.WB],
            Position.LWB: [Position.LWB, Position.LB, Position.WB],
            Position.RWB: [Position.RWB, Position.RB, Position.WB],
            Position.WB: [Position.WB, Position.LWB, Position.RWB],
            Position.DM: [Position.DM, Position.CM],
            Position.CM: [Position.CM, Position.DM, Position.AM],
            Position.AM: [Position.AM, Position.CM],
            Position.LM: [Position.LM, Position.CM, Position.LW],
            Position.RM: [Position.RM, Position.CM, Position.RW],
            Position.LW: [Position.LW, Position.LM, Position.ST],
            Position.RW: [Position.RW, Position.RM, Position.ST],
            Position.ST: [Position.ST, Position.LW, Position.RW]
        }
        
        return compatibility.get(position, [position])
    
    def _replace_team_player(self, team):
        """Replace a player in the team."""
        # Get formation assignments
        assignments = self._get_formation_assignment(team)
        
        print(f"\nCurrent players in {team.name} (Formation: {team.formation}):")
        for i, player in enumerate(team.players, 1):
            natural_pos = player.position.name
            assigned_pos = assignments.get(i-1, player.position).name
            
            if natural_pos == assigned_pos:
                pos_display = f"Playing: {assigned_pos}"
            else:
                pos_display = f"Playing: {assigned_pos} (Natural: {natural_pos})"
            
            print(f"{i}. {player.name} - {pos_display} - OVR: {player.overall_rating():.0f}")
        
        try:
            player_idx = int(input(f"\nSelect player to replace (1-{len(team.players)}): ").strip()) - 1
            if not (0 <= player_idx < len(team.players)):
                print("Invalid choice!")
                self.pause()
                return
            
            old_player = team.players[player_idx]
            assigned_position = assignments.get(player_idx, old_player.position)
            
            print(f"\nReplacing {old_player.name} who is playing {assigned_position.name}")
            
            # Show available players for that assigned position (and compatible positions)
            compatible_positions = self._get_compatible_positions(assigned_position)
            available_players = [p for p in self.player_manager.players 
                               if p.position in compatible_positions and p not in team.players]
            
            if not available_players:
                print(f"No available players for {assigned_position.name} position!")
                print("Showing all available players instead...")
                available_players = [p for p in self.player_manager.players if p not in team.players]
            
            if not available_players:
                print("No available players!")
                self.pause()
                return
            
            print(f"\nAvailable players for {assigned_position.name} position:")
            for i, player in enumerate(available_players, 1):
                suitability = "✅" if player.position == assigned_position else "⚠️ " if player.position in self._get_compatible_positions(assigned_position) else "❌"
                print(f"{i}. {player.name} ({player.position.name}) {suitability} - OVR: {player.overall_rating():.0f}")
            
            new_player_idx = int(input(f"\nSelect replacement (1-{len(available_players)}): ").strip()) - 1
            if not (0 <= new_player_idx < len(available_players)):
                print("Invalid choice!")
                self.pause()
                return
            
            new_player = available_players[new_player_idx]
            team.players[player_idx] = new_player
            self.team_manager.save_teams()
            
            print(f"Replaced {old_player.name} with {new_player.name}!")
            print(f"{new_player.name} will play {assigned_position.name}")
            
        except (ValueError, KeyboardInterrupt):
            print("Operation cancelled!")
        
        self.pause()
    
    def delete_team(self):
        """Delete a team."""
        team = self._select_team_by_number("Select team to delete")
        if not team:
            return
        
        confirm = input(f"\nDelete team '{team.name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            self.team_manager.teams.remove(team)
            self.team_manager.save_teams()
            print("Team deleted!")
    
    def play_match(self):
        """Play a single match between two teams."""
        if len(self.team_manager.teams) < 2:
            print("\nNeed at least 2 teams to play a match!")
            return
        
        home_team, away_team = self._select_teams()
        if not home_team or not away_team:
            return
        
        self.clear_screen()
        print("=" * 60)
        print("SINGLE MATCH")
        print("=" * 60)
        
        # Show team info before match
        print(f"\n🏠 HOME: {home_team.name}")
        print(f"   Elo: {home_team.elo_rating:.0f} | Streak: {self._format_streak(home_team.streak_count)}")
        print(f"   Formation: {home_team.formation} | Style: {home_team.style.name}")
        
        print(f"\n✈️  AWAY: {away_team.name}")
        print(f"   Elo: {away_team.elo_rating:.0f} | Streak: {self._format_streak(away_team.streak_count)}")
        print(f"   Formation: {away_team.formation} | Style: {away_team.style.name}")
        
        self.pause("\nPress Enter to simulate match...")
        self.clear_screen()
        
        # Simulate match
        result = self.match_engine.simulate_match(home_team, away_team)
        self.match_engine.display_match_result(result)
        
        # Update Elo ratings
        self.team_manager.update_team_elo(
            home_team.name, away_team.name,
            (result.home_score, result.away_score)
        )
        
        print(f"\n{'='*60}")
        print("POST-MATCH RATINGS")
        print(f"{'='*60}")
        print(f"{home_team.name}: {home_team.elo_rating:.0f} (Streak: {self._format_streak(home_team.streak_count)})")
        print(f"{away_team.name}: {away_team.elo_rating:.0f} (Streak: {self._format_streak(away_team.streak_count)})")
    
    def play_multiple_matches(self):
        """Play multiple matches between two teams to see streak effects."""
        if len(self.team_manager.teams) < 2:
            print("\nNeed at least 2 teams to play matches!")
            return
        
        home_team, away_team = self._select_teams()
        if not home_team or not away_team:
            return
            
        try:
            num_matches = int(input("\nHow many matches to simulate? [5]: ") or "5")
            if num_matches < 1:
                print("Number of matches must be positive!")
                return
        except ValueError:
            print("Invalid number!")
            return
        
        self.clear_screen()
        print("=" * 80)
        print(f"MULTIPLE MATCHES: {home_team.name} vs {away_team.name}")
        print("=" * 80)
        
        # Store initial ratings
        initial_home_elo = home_team.elo_rating
        initial_away_elo = away_team.elo_rating
        
        results = []
        home_wins = away_wins = draws = 0
        
        # Determine display mode based on number of matches
        detailed_mode = num_matches <= 5
        
        if detailed_mode:
            print(f"\n📋 Will show detailed match-by-match results ({num_matches} matches)")
        else:
            print(f"\n⚡ Fast simulation mode - showing only final stats ({num_matches} matches)")
        
        self.pause("\nPress Enter to start the series...")
        
        for match_num in range(1, num_matches + 1):
            if detailed_mode:
                self.clear_screen()
                print(f"\n{'🎯 MATCH ' + str(match_num):^80}")
                print("-" * 80)
                
                # Show current status with enhanced streak display
                home_streak_display = self._format_streak(home_team.streak_count)
                away_streak_display = self._format_streak(away_team.streak_count)
                
                # Add streak icons
                home_streak_icon = "🔥" if home_team.streak_count >= 3 else "❄️" if home_team.streak_count <= -3 else "⚪"
                away_streak_icon = "🔥" if away_team.streak_count >= 3 else "❄️" if away_team.streak_count <= -3 else "⚪"
                
                print(f"Before Match:")
                print(f"  🏠 {home_team.name}: Elo {home_team.elo_rating:.0f} | {home_streak_icon} {home_streak_display}")
                print(f"  ✈️  {away_team.name}: Elo {away_team.elo_rating:.0f} | {away_streak_icon} {away_streak_display}")
                
                # Show momentum multipliers BEFORE the match
                home_momentum = home_team.adjust_for_streak()
                away_momentum = away_team.adjust_for_streak()
                if home_momentum != 1.0 or away_momentum != 1.0:
                    print(f"\n🔥 MOMENTUM ACTIVE:")
                    if home_momentum != 1.0:
                        momentum_type = "BOOST" if home_momentum > 1.0 else "PENALTY"
                        print(f"     {home_team.name}: {home_momentum:.1%} performance ({momentum_type})")
                    if away_momentum != 1.0:
                        momentum_type = "BOOST" if away_momentum > 1.0 else "PENALTY"
                        print(f"     {away_team.name}: {away_momentum:.1%} performance ({momentum_type})")
            else:
                # Fast mode - just show progress
                if match_num == 1 or match_num % 10 == 0 or match_num == num_matches:
                    print(f"\r🎮 Simulating matches... {match_num}/{num_matches}", end="", flush=True)
            
            # Simulate match
            result = self.match_engine.simulate_match(home_team, away_team)
            results.append(result)
            
            # Update counters
            if result.home_score > result.away_score:
                home_wins += 1
                result_emoji = "🏠"
                winner = home_team.name
            elif result.away_score > result.home_score:
                away_wins += 1
                result_emoji = "✈️"
                winner = away_team.name
            else:
                draws += 1
                result_emoji = "🤝"
                winner = "DRAW"
            
            # Update Elo
            self.team_manager.update_team_elo(
                home_team.name, away_team.name,
                (result.home_score, result.away_score)
            )
            
            if detailed_mode:
                # Show full match result (same as single match display)
                self.match_engine.display_enhanced_match_result(result)
                
                print(f"\n{'='*60}")
                print("POST-MATCH RATINGS")
                print(f"{'='*60}")
                new_home_icon = "🔥" if home_team.streak_count >= 3 else "❄️" if home_team.streak_count <= -3 else "⚪"
                new_away_icon = "🔥" if away_team.streak_count >= 3 else "❄️" if away_team.streak_count <= -3 else "⚪"
                
                print(f"🏠 {home_team.name}: {home_team.elo_rating:.0f} (Streak: {new_home_icon} {self._format_streak(home_team.streak_count)})")
                print(f"✈️  {away_team.name}: {away_team.elo_rating:.0f} (Streak: {new_away_icon} {self._format_streak(away_team.streak_count)})")
                
                # Highlight if streaks just hit the momentum threshold
                if abs(home_team.streak_count) == 3:
                    print(f"\n🎯 {home_team.name} {'enters hot streak' if home_team.streak_count > 0 else 'enters cold streak'}!")
                if abs(away_team.streak_count) == 3:
                    print(f"🎯 {away_team.name} {'enters hot streak' if away_team.streak_count > 0 else 'enters cold streak'}!")
                
                if match_num < num_matches:
                    self.pause("Press Enter for next match...")
                else:
                    # For the last match, pause before showing final summary 
                    self.pause("Press Enter to view final summary...")
        
        # Clear progress indicator for fast mode
        if not detailed_mode:
            print(f"\n✅ Completed {num_matches} matches!")
        
        # Final summary
        self.clear_screen()
        print("=" * 80)
        print("SERIES SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 Results after {num_matches} matches:")
        print(f"   🏠 {home_team.name} wins: {home_wins}")
        print(f"   ✈️  {away_team.name} wins: {away_wins}")
        print(f"   🤝 Draws: {draws}")
        
        print(f"\n📈 Elo Rating Changes:")
        home_change = home_team.elo_rating - initial_home_elo
        away_change = away_team.elo_rating - initial_away_elo
        
        print(f"   {home_team.name}: {initial_home_elo:.0f} → {home_team.elo_rating:.0f} "
              f"({home_change:+.0f})")
        print(f"   {away_team.name}: {initial_away_elo:.0f} → {away_team.elo_rating:.0f} "
              f"({away_change:+.0f})")
        
        print(f"\n🔥 Final Streaks:")
        print(f"   {home_team.name}: {self._format_streak(home_team.streak_count)}")
        print(f"   {away_team.name}: {self._format_streak(away_team.streak_count)}")
        
        # Goal statistics
        total_home_goals = sum(r.home_score for r in results)
        total_away_goals = sum(r.away_score for r in results)
        
        print(f"\n⚽ Goal Statistics:")
        print(f"   Total goals: {total_home_goals + total_away_goals}")
        print(f"   Average per match: {(total_home_goals + total_away_goals) / num_matches:.1f}")
        print(f"   {home_team.name} scored: {total_home_goals} ({total_home_goals/num_matches:.1f} per match)")
        print(f"   {away_team.name} scored: {total_away_goals} ({total_away_goals/num_matches:.1f} per match)")
    
    def _select_teams(self):
        """Helper method to select two teams."""
        print("\nAvailable teams:")
        for i, team in enumerate(self.team_manager.teams, 1):
            streak_info = self._format_streak(team.streak_count)
            print(f"{i}. {team.name} (Elo: {team.elo_rating:.0f}, Streak: {streak_info})")
        
        try:
            home_idx = int(input("\nSelect home team (number): ")) - 1
            away_idx = int(input("Select away team (number): ")) - 1
            
            if (home_idx < 0 or home_idx >= len(self.team_manager.teams) or
                away_idx < 0 or away_idx >= len(self.team_manager.teams) or
                home_idx == away_idx):
                print("Invalid selection!")
                return None, None
        except ValueError:
            print("Invalid input!")
            return None, None
        
        return self.team_manager.teams[home_idx], self.team_manager.teams[away_idx]
    
    def _format_streak(self, streak_count):
        """Format streak count for display."""
        if streak_count > 0:
            return f"{streak_count}W"
        elif streak_count < 0:
            return f"{abs(streak_count)}L"
        else:
            return "-"
    
    def play_multiple_random_games(self):
        """Play multiple matches between the same two random teams to see streak effects."""
        self.clear_screen()
        print("=" * 80)
        print("MULTIPLE MATCHES WITH RANDOM TEAMS")
        print("=" * 80)
        
        try:
            num_matches = int(input("\nHow many matches to simulate? [5]: ") or "5")
            if num_matches < 1:
                print("Number of matches must be positive!")
                return
        except ValueError:
            print("Invalid number!")
            return
        
        # Check if we need to generate more players
        if len(self.player_manager.players) < 50:
            print(f"\n🔄 Generating player pool...")
            players = self.player_manager.generate_player_pool(80)
            for p in players:
                self.player_manager.add_player(p)
            print("✅ Player pool ready!")
        
        # Create two random teams that will play multiple times
        print(f"\n🏗️  Creating random teams...")
        team1 = self.team_manager.create_random_team(
            "Team Alpha", self.player_manager.players
        )
        team2 = self.team_manager.create_random_team(
            "Team Beta", self.player_manager.players
        )
        
        if not team1 or not team2:
            print("❌ Failed to create teams!")
            return
        
        print("✅ Teams created!")
        
        self.clear_screen()
        print("=" * 80)
        print(f"MULTIPLE MATCHES: {team1.name} vs {team2.name}")
        print("=" * 80)
        
        # Show detailed team info first
        print(f"\n🏠 HOME TEAM: {team1.name}")
        print(f"   Formation: {team1.formation} | Style: {team1.style.name}")
        print(f"   Overall Strength: {team1.compute_strength():.1f}")
        print(f"   Starting Elo: {team1.elo_rating:.0f}")
        print(f"   Key Players:")
        
        # Show top 3 players by rating
        sorted_players = sorted(team1.players, 
                               key=lambda p: p.overall_rating(), reverse=True)
        for i, player in enumerate(sorted_players[:3], 1):
            print(f"     {i}. {player.name} ({player.position.name}) - OVR: {player.overall_rating():.0f}")
        
        print(f"\n✈️  AWAY TEAM: {team2.name}")
        print(f"   Formation: {team2.formation} | Style: {team2.style.name}")
        print(f"   Overall Strength: {team2.compute_strength():.1f}")
        print(f"   Starting Elo: {team2.elo_rating:.0f}")
        print(f"   Key Players:")
        
        # Show top 3 players by rating
        sorted_players = sorted(team2.players, 
                               key=lambda p: p.overall_rating(), reverse=True)
        for i, player in enumerate(sorted_players[:3], 1):
            print(f"     {i}. {player.name} ({player.position.name}) - OVR: {player.overall_rating():.0f}")
        
        # Store initial ratings
        initial_team1_elo = team1.elo_rating
        initial_team2_elo = team2.elo_rating
        
        results = []
        team1_wins = team2_wins = draws = 0
        
        # Determine display mode based on number of matches
        detailed_mode = num_matches <= 5
        
        if detailed_mode:
            print(f"\n📋 Will show detailed match-by-match results ({num_matches} matches)")
        else:
            print(f"\n⚡ Fast simulation mode - showing only final stats ({num_matches} matches)")
        
        self.pause("\nPress Enter to start the series...")
        
        for match_num in range(1, num_matches + 1):
            if detailed_mode:
                self.clear_screen()
                print(f"{'🎯 MATCH ' + str(match_num):^80}")
                print("-" * 80)
                
                # Show current status with enhanced streak display
                team1_streak_display = self._format_streak(team1.streak_count)
                team2_streak_display = self._format_streak(team2.streak_count)
                
                # Add streak icons
                team1_streak_icon = "🔥" if team1.streak_count >= 3 else "❄️" if team1.streak_count <= -3 else "⚪"
                team2_streak_icon = "🔥" if team2.streak_count >= 3 else "❄️" if team2.streak_count <= -3 else "⚪"
                
                print(f"Before Match:")
                print(f"  🏠 {team1.name}: Elo {team1.elo_rating:.0f} | {team1_streak_icon} {team1_streak_display}")
                print(f"  ✈️  {team2.name}: Elo {team2.elo_rating:.0f} | {team2_streak_icon} {team2_streak_display}")
                
                # Show momentum multipliers BEFORE the match
                team1_momentum = team1.adjust_for_streak()
                team2_momentum = team2.adjust_for_streak()
                if team1_momentum != 1.0 or team2_momentum != 1.0:
                    print(f"\n🔥 MOMENTUM ACTIVE:")
                    if team1_momentum != 1.0:
                        momentum_type = "BOOST" if team1_momentum > 1.0 else "PENALTY"
                        print(f"     {team1.name}: {team1_momentum:.1%} performance ({momentum_type})")
                    if team2_momentum != 1.0:
                        momentum_type = "BOOST" if team2_momentum > 1.0 else "PENALTY"
                        print(f"     {team2.name}: {team2_momentum:.1%} performance ({momentum_type})")
                
                self.pause("\nPress Enter to simulate match...")
                self.clear_screen()
            else:
                # Fast mode - just show progress
                if match_num == 1 or match_num % 10 == 0 or match_num == num_matches:
                    print(f"\r🎮 Simulating matches... {match_num}/{num_matches}", end="", flush=True)
            
            # Simulate match
            result = self.match_engine.simulate_match(team1, team2)
            results.append(result)
            
            # Update counters
            if result.home_score > result.away_score:
                team1_wins += 1
                result_emoji = "🏠"
                winner = team1.name
            elif result.away_score > result.home_score:
                team2_wins += 1
                result_emoji = "✈️"
                winner = team2.name
            else:
                draws += 1
                result_emoji = "🤝"
                winner = "DRAW"
            
            # Manually update streaks and Elo
            if result.home_score > result.away_score:
                team1.streak_count = max(0, team1.streak_count) + 1
                team2.streak_count = min(0, team2.streak_count) - 1
            elif result.away_score > result.home_score:
                team1.streak_count = min(0, team1.streak_count) - 1
                team2.streak_count = max(0, team2.streak_count) + 1
            else:
                team1.streak_count = 0
                team2.streak_count = 0
            
            # Update Elo ratings
            expected_1 = 1 / (1 + 10**((team2.elo_rating - team1.elo_rating) / 400))
            expected_2 = 1 - expected_1
            
            if result.home_score > result.away_score:
                actual_1, actual_2 = 1, 0
            elif result.away_score > result.home_score:
                actual_1, actual_2 = 0, 1
            else:
                actual_1, actual_2 = 0.5, 0.5
            
            k_factor = 20
            team1.elo_rating += k_factor * (actual_1 - expected_1)
            team2.elo_rating += k_factor * (actual_2 - expected_2)
            
            if detailed_mode:
                # Show full match result (same as single match display)
                self.match_engine.display_enhanced_match_result(result)
                
                print(f"\n{'='*60}")
                print("POST-MATCH RATINGS")
                print(f"{'='*60}")
                new_team1_icon = "🔥" if team1.streak_count >= 3 else "❄️" if team1.streak_count <= -3 else "⚪"
                new_team2_icon = "🔥" if team2.streak_count >= 3 else "❄️" if team2.streak_count <= -3 else "⚪"
                
                print(f"🏠 {team1.name}: {team1.elo_rating:.0f} (Streak: {new_team1_icon} {self._format_streak(team1.streak_count)})")
                print(f"✈️  {team2.name}: {team2.elo_rating:.0f} (Streak: {new_team2_icon} {self._format_streak(team2.streak_count)})")
                
                # Highlight if streaks just hit the momentum threshold
                if abs(team1.streak_count) == 3:
                    print(f"\n🎯 {team1.name} {'enters hot streak' if team1.streak_count > 0 else 'enters cold streak'}!")
                if abs(team2.streak_count) == 3:
                    print(f"🎯 {team2.name} {'enters hot streak' if team2.streak_count > 0 else 'enters cold streak'}!")
                
                if match_num < num_matches:
                    self.pause("Press Enter for next match...")
                else:
                    # For the last match, pause before showing final summary
                    self.pause("Press Enter to view final summary...")
        
        # Clear progress indicator for fast mode
        if not detailed_mode:
            print(f"\n✅ Completed {num_matches} matches!")
        
        # Final summary
        self.clear_screen()
        print("=" * 80)
        print("SERIES SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 Results after {num_matches} matches:")
        print(f"   🏠 {team1.name} wins: {team1_wins}")
        print(f"   ✈️  {team2.name} wins: {team2_wins}")
        print(f"   🤝 Draws: {draws}")
        
        print(f"\n📈 Elo Rating Changes:")
        team1_change = team1.elo_rating - initial_team1_elo
        team2_change = team2.elo_rating - initial_team2_elo
        
        print(f"   {team1.name}: {initial_team1_elo:.0f} → {team1.elo_rating:.0f} "
              f"({team1_change:+.0f})")
        print(f"   {team2.name}: {initial_team2_elo:.0f} → {team2.elo_rating:.0f} "
              f"({team2_change:+.0f})")
        
        print(f"\n🔥 Final Streaks:")
        print(f"   {team1.name}: {self._format_streak(team1.streak_count)}")
        print(f"   {team2.name}: {self._format_streak(team2.streak_count)}")
        
        # Goal statistics
        total_team1_goals = sum(r.home_score for r in results)
        total_team2_goals = sum(r.away_score for r in results)
        
        print(f"\n⚽ Goal Statistics:")
        print(f"   Total goals: {total_team1_goals + total_team2_goals}")
        print(f"   Average per match: {(total_team1_goals + total_team2_goals) / num_matches:.1f}")
        print(f"   {team1.name} scored: {total_team1_goals} ({total_team1_goals/num_matches:.1f} per match)")
        print(f"   {team2.name} scored: {total_team2_goals} ({total_team2_goals/num_matches:.1f} per match)")
    
    def quick_play(self):
        """Quick play with random teams."""
        self.clear_screen()
        print("=" * 60)
        print("QUICK PLAY - INSTANT MATCH")
        print("=" * 60)
        
        # Generate players if needed
        if len(self.player_manager.players) < 50:
            print("\n🔄 Generating player pool...")
            players = self.player_manager.generate_player_pool(50)
            for p in players:
                self.player_manager.add_player(p)
            print("✅ Player pool ready!")
        
        # Create two random teams
        print("\n🏗️  Creating random teams...")
        team1 = self.team_manager.create_random_team(
            "Team Alpha", self.player_manager.players
        )
        team2 = self.team_manager.create_random_team(
            "Team Beta", self.player_manager.players
        )
        
        if not team1 or not team2:
            print("❌ Failed to create teams!")
            return
        
        print("✅ Teams created!")
        print(team1.summary())
        print(team2.summary())
        
        # Play match
        self.pause("\nPress Enter to simulate the instant match...")
        self.clear_screen()
        
        result = self.match_engine.simulate_match(team1, team2)
        self.match_engine.display_match_result(result)
    
    def tournament_menu(self):
        """Tournament management submenu."""
        while True:
            self.clear_screen()
            print("=" * 70)
            print("🏆 TOURNAMENT MODE")
            print("=" * 70)
            print("\n1. Create New Tournament")
            print("2. Continue Existing Tournament")
            print("3. View Tournament Bracket")
            print("0. Back to Main Menu")
            print("\n" + "=" * 70)
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                self.create_tournament()
                self.pause()
            elif choice == "2":
                self.continue_tournament()
                self.pause()
            elif choice == "3":
                self.view_tournament_bracket()
                self.pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
                self.pause()
    
    def create_tournament(self):
        """Create a new tournament."""
        self.clear_screen()
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
        
        # Clear screen before team selection
        self.clear_screen()
        
        # Check if we have enough existing teams
        existing_teams_count = len(self.team_manager.teams)
        
        print("=" * 70)
        print(f"🏆 {tournament_name.upper()} - TEAM SELECTION")
        print("=" * 70)
        print(f"\nTeam Selection Options:")
        print(f"Available existing teams: {existing_teams_count}")
        print(f"Teams needed: {num_teams}")
        
        print(f"\n1. Select existing teams manually")
        print(f"2. Randomly select from existing teams")
        print(f"3. Create all teams randomly")
        print(f"4. Mix existing and random teams")
        
        selection_choice = input("\nSelect option: ").strip()
        
        selected_teams = []
        
        if selection_choice == "1":
            # Manually select existing teams
            if existing_teams_count < num_teams:
                print(f"Not enough existing teams! Have {existing_teams_count}, need {num_teams}")
                return
            
            selected_teams = self._select_existing_teams(num_teams)
            
        elif selection_choice == "2":
            # Randomly select from existing teams
            if existing_teams_count == 0:
                print("No existing teams available!")
                return
            
            if existing_teams_count < num_teams:
                print(f"Not enough existing teams! Have {existing_teams_count}, need {num_teams}")
                print(f"1. Use all {existing_teams_count} existing teams")
                print(f"2. Cancel and select different option")
                
                sub_choice = input("Select option: ").strip()
                if sub_choice == "1":
                    selected_teams = self._randomly_select_existing_teams(existing_teams_count)
                else:
                    return
            else:
                # Ask how many to select if we have more than needed
                if existing_teams_count > num_teams:
                    print(f"\nYou need {num_teams} teams, but have {existing_teams_count} available.")
                    print(f"1. Randomly select exactly {num_teams} teams")
                    print(f"2. Use all {existing_teams_count} teams")
                    
                    sub_choice = input("Select option: ").strip()
                    if sub_choice == "1":
                        selected_teams = self._randomly_select_existing_teams(num_teams)
                    elif sub_choice == "2":
                        selected_teams = self._randomly_select_existing_teams(existing_teams_count)
                    else:
                        print("Invalid selection!")
                        return
                else:
                    # Exactly the right number
                    selected_teams = self._randomly_select_existing_teams(num_teams)
            
        elif selection_choice == "3":
            # Create all random teams
            print(f"\n🔄 Creating {num_teams} random teams...")
            random_teams = self.tournament_manager.create_random_teams_for_tournament(
                num_teams, f"{tournament_name}"
            )
            selected_teams = [team.name for team in random_teams]
            print(f"✅ Created {len(random_teams)} teams!")
            
        elif selection_choice == "4":
            # Mix existing and random
            use_existing = min(existing_teams_count, num_teams)
            if use_existing > 0:
                print(f"\nHow many existing teams to use? (max {use_existing}):")
                try:
                    existing_count = int(input().strip())
                    existing_count = min(max(0, existing_count), use_existing)
                    
                    if existing_count > 0:
                        print(f"\n1. Select {existing_count} existing teams manually")
                        print(f"2. Randomly select {existing_count} existing teams")
                        
                        sub_choice = input("Select option: ").strip()
                        
                        if sub_choice == "1":
                            existing_selected = self._select_existing_teams(existing_count)
                        elif sub_choice == "2":
                            existing_selected = self._randomly_select_existing_teams(existing_count)
                        else:
                            print("Invalid selection!")
                            return
                        
                        selected_teams.extend(existing_selected)
                except ValueError:
                    print("Invalid number!")
                    return
            
            remaining = num_teams - len(selected_teams)
            if remaining > 0:
                print(f"\n🔄 Creating {remaining} additional random teams...")
                random_teams = self.tournament_manager.create_random_teams_for_tournament(
                    remaining, f"{tournament_name} Random"
                )
                selected_teams.extend([team.name for team in random_teams])
                print(f"✅ Created {len(random_teams)} additional teams!")
        else:
            print("Invalid selection!")
            return
        
        if len(selected_teams) < 2:
            print("Not enough teams selected! Need at least 2 teams for a tournament.")
            return
        
        # Inform user if tournament will be padded to next power of 2
        if len(selected_teams) != num_teams:
            print(f"\n📝 Note: Selected {len(selected_teams)} teams instead of {num_teams}")
            print(f"Tournament will automatically adjust bracket size if needed.")
        
        # Create tournament
        try:
            tournament = self.tournament_manager.create_tournament(tournament_name, selected_teams)
            
            # Clear screen before showing tournament created message and bracket
            self.clear_screen()
            
            print("=" * 70)
            print(f"🏆 TOURNAMENT CREATED: {tournament_name.upper()}")
            print("=" * 70)
            print(f"\n✅ Tournament '{tournament_name}' created successfully!")
            print(f"📊 Teams: {len(tournament.teams)}")
            print(f"🔥 Rounds: {len(tournament.rounds)}")
            
            # Display bracket
            print(self.tournament_manager.get_tournament_bracket_display(tournament))
            
            # Store tournament for continuation
            self.current_tournament = tournament
            
            # Ask if user wants to start immediately
            start_now = input("\nStart tournament now? (y/n): ").strip().lower()
            if start_now == 'y':
                # Clear screen before starting tournament
                self.clear_screen()
                # print("=" * 70)
                # print(f"🚀 STARTING TOURNAMENT: {tournament_name.upper()}")
                # print("=" * 70)
                # self.pause("Press Enter to begin...")
                self._simulate_tournament(tournament)
            
        except Exception as e:
            print(f"Error creating tournament: {e}")
    
    def _select_existing_teams(self, count: int) -> List[str]:
        """Helper to select existing teams."""
        available_teams = [team.name for team in self.team_manager.teams]
        selected = []
        
        print(f"\nAvailable teams:")
        for i, team_name in enumerate(available_teams, 1):
            team = self.team_manager.find_team_by_name(team_name)
            elo = team.elo_rating if team else 0
            print(f"{i}. {team_name} (Elo: {elo:.0f})")
        
        while len(selected) < count:
            try:
                choice = input(f"\nSelect team {len(selected) + 1}/{count} (number): ").strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(available_teams):
                    team_name = available_teams[idx]
                    if team_name not in selected:
                        selected.append(team_name)
                        print(f"✅ Selected: {team_name}")
                    else:
                        print("Team already selected!")
                else:
                    print("Invalid team number!")
            except ValueError:
                print("Invalid input!")
        
        return selected
    
    def _randomly_select_existing_teams(self, count: int) -> List[str]:
        """Randomly select teams from existing teams."""
        import random
        
        available_teams = [team.name for team in self.team_manager.teams]
        
        if count >= len(available_teams):
            # If we need all teams or more, just return all
            selected = available_teams.copy()
            print(f"\n🎲 Randomly selected all {len(selected)} available teams:")
        else:
            # Randomly sample the requested number
            selected = random.sample(available_teams, count)
            print(f"\n🎲 Randomly selected {count} teams from {len(available_teams)} available:")
        
        # Display selected teams with their Elo ratings
        for i, team_name in enumerate(selected, 1):
            team = self.team_manager.find_team_by_name(team_name)
            elo = team.elo_rating if team else 0
            print(f"   {i}. {team_name} (Elo: {elo:.0f})")
        
        return selected
    
    def _display_tournament_progress(self, tournament):
        """Display tournament progress header."""
        completed_rounds = sum(1 for r in tournament.rounds if r.completed)
        total_rounds = len(tournament.rounds)
        
        print(f"\n🏆 {tournament.name.upper()}")
        print(f"📊 Progress: Round {tournament.current_round + 1}/{total_rounds} "
              f"({completed_rounds}/{total_rounds} rounds completed)")
        
        # Show progress bar
        progress = completed_rounds / total_rounds if total_rounds > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"▌{bar}▐ {progress * 100:.0f}%")
        
        # Show remaining teams
        if not tournament.completed:
            current_round = tournament.get_current_round()
            if current_round:
                active_teams = set()
                for match in current_round.matches:
                    if match.home_team:
                        active_teams.add(match.home_team)
                    if match.away_team:
                        active_teams.add(match.away_team)
                print(f"🎯 Teams remaining: {len(active_teams)}")
    
    def _display_round_winners(self, round_obj):
        """Display winners of a completed round."""
        winners = [match.winner for match in round_obj.matches if match.winner]
        if winners:
            print(f"\n🏆 {round_obj.round_name} Winners:")
            for i, winner in enumerate(winners, 1):
                print(f"   {i}. {winner}")
            print(f"\n➡️  {len(winners)} teams advance to the next round")
    
    def continue_tournament(self):
        """Continue an existing tournament."""
        if not hasattr(self, 'current_tournament') or not self.current_tournament:
            print("\nNo active tournament found!")
            return
        
        tournament = self.current_tournament
        
        if tournament.completed:
            self.clear_screen()
            print("=" * 70)
            print(f"🏆 TOURNAMENT COMPLETED: {tournament.name.upper()}")
            print("=" * 70)
            print(f"\n🥇 Winner: {tournament.winner}")
            print(self.tournament_manager.get_tournament_bracket_display(tournament))
            return
        
        # Clear screen and show current status
        self.clear_screen()
        print("=" * 70)
        print(f"🔄 CONTINUING TOURNAMENT: {tournament.name.upper()}")
        print("=" * 70)
        
        # Show current status
        print(self.tournament_manager.get_tournament_bracket_display(tournament))
        self.pause("Press Enter to continue tournament...")
        
        # Continue simulation
        self._simulate_tournament(tournament)
    
    def view_tournament_bracket(self):
        """View the current tournament bracket."""
        if not hasattr(self, 'current_tournament') or not self.current_tournament:
            print("\nNo active tournament found!")
            return
        
        self.clear_screen()
        print("=" * 70)
        print(f"📋 TOURNAMENT BRACKET: {self.current_tournament.name.upper()}")
        print("=" * 70)
        
        print(self.tournament_manager.get_tournament_bracket_display(self.current_tournament))
    
    def _simulate_tournament(self, tournament):
        """Simulate tournament matches."""
        while not tournament.completed:
            current_round = tournament.get_current_round()
            if not current_round:
                break
            
            # We'll show the round info before each match, so no need for detailed round intro
            
            # Simulate all matches in current round
            for match_num, match in enumerate(current_round.matches, 1):
                if not match.completed:
                    # Clear screen before each match announcement
                    self.clear_screen()
                    
                    # Show tournament progress
                    self._display_tournament_progress(tournament)
                    
                    print(f"\n{'─' * 70}")
                    match_preview = self.tournament_manager._generate_match_preview(match.home_team, match.away_team)
                    print(f"⚽ MATCH {match_num}/{len(current_round.matches)}: {match_preview}")
                    print(f"📍 {current_round.round_name}")
                    print(f"{'─' * 70}")
                    
                    
                    # Simulate the match
                    match_result = self.tournament_manager.simulate_tournament_match(
                        tournament, match.match_id, self.match_engine
                    )
                    
                    if match_result:
                        result_match, full_result = match_result
                        
                        print()  # Just add some spacing
                        print("="*80)
                        print(f"TOURNAMENT MATCH RESULT: {result_match.home_team} vs {result_match.away_team}")
                        print("="*80)
                        
                        # 1. FINAL SCORE
                        print(f"\nFINAL SCORE: {result_match.home_team} {full_result.home_score} - "
                              f"{full_result.away_score} {result_match.away_team}")
                        
                        # 2. PENALTY SHOOTOUT RESULT (if applicable)
                        if "(" in str(result_match.home_score):
                            print(f"\n🥅 PENALTY SHOOTOUT RESULT:")
                            print(f"   {result_match.home_team} {result_match.home_score} - "
                                  f"{result_match.away_score} {result_match.away_team}")
                            print(f"   🏆 Winner on penalties: {result_match.winner}")
                        
                        # 3. ADVANCES TO NEXT ROUND (or wins tournament)
                        current_round = tournament.get_current_round()
                        if tournament.current_round + 1 >= len(tournament.rounds):
                            print(f"\n🏆 {result_match.winner} wins the tournament!")
                        else:
                            next_round_name = tournament.rounds[tournament.current_round + 1].round_name if tournament.current_round + 1 < len(tournament.rounds) else "Final"
                            print(f"\n🏆 {result_match.winner} advances to the {next_round_name}!")
                        
                        # 4. ENHANCED MATCH STATISTICS (without header since we already showed it)
                        print(f"\n{'='*80}")
                        print("ENHANCED MATCH STATISTICS")
                        print(f"{'='*80}")
                        
                        # Events - separate regular match events from penalty events
                        regular_events = []
                        penalty_events = []
                        
                        for event in full_result.events:
                            if event.event_type == "penalty":
                                penalty_events.append(event)
                            else:
                                regular_events.append(event)
                        
                        if regular_events:
                            print("\nMATCH EVENTS:")
                            for event in regular_events:
                                if event.event_type == "goal":
                                    emoji = "⚽"
                                elif event.event_type == "yellow_card":
                                    emoji = "🟨"
                                elif event.event_type == "red_card":
                                    emoji = "🟥"
                                elif event.event_type == "match_abandoned":
                                    emoji = "🚫"
                                else:
                                    emoji = "📝"
                                print(f"{event.minute}' {emoji} {event.team} - {event.description}")
                        
                        if penalty_events:
                            print("\nPENALTY SHOOTOUT EVENTS:")
                            for event in penalty_events:
                                emoji = "🥅"
                                print(f"{event.minute}' {emoji} {event.team} - {event.description}")
                        
                        # Statistics table
                        print("\nMATCH STATISTICS:")
                        print(f"{'Stat':<25} {full_result.home_team:<20} {full_result.away_team:<20}")
                        print("-" * 65)
                        
                        home_stats = full_result.stats[full_result.home_team]
                        away_stats = full_result.stats[full_result.away_team]
                        
                        print(f"{'Possession':<25} {home_stats['possession']:<20.1f}% "
                              f"{away_stats['possession']:<20.1f}%")
                        print(f"{'Expected Goals':<25} {home_stats['expected_goals']:<20.1f} "
                              f"{away_stats['expected_goals']:<20.1f}")
                        print(f"{'Shots':<25} {home_stats['shots']:<20.0f} "
                              f"{away_stats['shots']:<20.0f}")
                        print(f"{'Shots on Target':<25} {home_stats['shots_on_target']:<20.0f} "
                              f"{away_stats['shots_on_target']:<20.0f}")
                        print(f"{'Pass Accuracy':<25} {home_stats['pass_accuracy']:<20.1f}% "
                              f"{away_stats['pass_accuracy']:<20.1f}%")
                        print(f"{'Team Rating':<25} {home_stats['team_rating']:<20.1f} "
                              f"{away_stats['team_rating']:<20.1f}")
                        print(f"{'Players Available':<25} {home_stats['players_available']:<20.0f} "
                              f"{away_stats['players_available']:<20.0f}")
                        print(f"{'Average Stamina':<25} {home_stats['average_stamina']:<20.1f}% "
                              f"{away_stats['average_stamina']:<20.1f}%")
                        print(f"{'Team Momentum':<25} {home_stats['momentum']:<20.1f} "
                              f"{away_stats['momentum']:<20.1f}")
                        
                        print("="*80)
                        
                        # Always show pause prompt after each match, including the last one
                        if match_num < len(current_round.matches):
                            self.pause("Press Enter for next match...")
                        else:
                            self.pause("Press Enter to view round summary...")
            
            # Show updated bracket after round
            if current_round.completed:
                self.clear_screen()
                print(f"\n✅ {current_round.round_name.upper()} COMPLETED!")
                print("=" * 70)
                self._display_round_winners(current_round)
                print(self.tournament_manager.get_tournament_bracket_display(tournament))
                
                if not tournament.completed:
                    next_round = tournament.rounds[tournament.current_round + 1] if tournament.current_round + 1 < len(tournament.rounds) else None
                    if next_round:
                        print(f"\n🔜 Next up: {next_round.round_name}")
                    self.pause("Press Enter to continue to next round...")
        
        # Tournament finished
        if tournament.completed:
            self.clear_screen()
            print("\n" + "🏆" * 20)
            print(f"TOURNAMENT COMPLETED: {tournament.name}")
            print("🏆" * 20)
            print(f"\n🥇 CHAMPION: {tournament.winner}")
            print(f"\nCongratulations to {tournament.winner}!")
            print("\nFinal Bracket:")
            print(self.tournament_manager.get_tournament_bracket_display(tournament))
    
    def settings_menu(self):
        """Settings submenu."""
        while True:
            self.clear_screen()
            print("=" * 60)
            print("SETTINGS")
            print("=" * 60)
            print(f"\n1. Toggle Momentum (Currently: {'🔥 ON' if self.match_engine.use_momentum else '❄️ OFF'})")
            print(f"2. Toggle Detailed Simulation (Currently: {'📊 ON' if self.match_engine.detailed_sim else '⚡ OFF'})")
            print("3. Reset All Data")
            print("4. View System Info")
            print("0. Back to Main Menu")
            print("\n" + "=" * 60)
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                self.match_engine.use_momentum = not self.match_engine.use_momentum
                status = "🔥 ENABLED" if self.match_engine.use_momentum else "❄️ DISABLED"
                print(f"\nMomentum system {status}!")
                self.pause()
            elif choice == "2":
                self.match_engine.detailed_sim = not self.match_engine.detailed_sim
                status = "📊 ENABLED" if self.match_engine.detailed_sim else "⚡ DISABLED"
                print(f"\nDetailed simulation {status}!")
                self.pause()
            elif choice == "3":
                confirm = input("\n⚠️  Delete all players and teams? This cannot be undone! (y/n): ").strip().lower()
                if confirm == 'y':
                    self.player_manager.players = []
                    self.player_manager.save_players()
                    self.team_manager.teams = []
                    self.team_manager.save_teams()
                    print("\n🗑️  All data has been reset!")
                else:
                    print("\nOperation cancelled.")
                self.pause()
            elif choice == "4":
                self.show_system_info()
                self.pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
                self.pause()
    
    def show_system_info(self):
        """Display system information."""
        print("\n" + "=" * 60)
        print("SYSTEM INFORMATION")
        print("=" * 60)
        
        print(f"\n📊 Database Statistics:")
        print(f"   Players: {len(self.player_manager.players)}")
        print(f"   Teams: {len(self.team_manager.teams)}")
        
        if self.team_manager.teams:
            avg_elo = sum(t.elo_rating for t in self.team_manager.teams) / len(self.team_manager.teams)
            print(f"   Average Elo: {avg_elo:.0f}")
        
        print(f"\n⚙️  Current Settings:")
        print(f"   Momentum System: {'🔥 ON' if self.match_engine.use_momentum else '❄️ OFF'}")
        print(f"   Detailed Simulation: {'📊 ON' if self.match_engine.detailed_sim else '⚡ OFF'}")
        
        print(f"\n📁 Data Files:")
        print(f"   Players: {self.player_manager.filename}")
        print(f"   Teams: {self.team_manager.filename}")
        
        print(f"\n🎮 Available Features:")
        print("   ✅ Player creation (manual/random)")
        print("   ✅ Team building with formations")
        print("   ✅ Single and multiple match simulation")
        print("   ✅ Elo rating system")
        print("   ✅ Momentum/streak effects")
        print("   ✅ Match statistics and events")
    
    def run(self):
        """Main application loop."""
        # self.clear_screen()
        # print("Welcome to Fantasy Football Manager v2.0.2!")
        # self.pause()
        
        try:
            while True:
                self.clear_screen()
                self.display_menu()
                choice = input("\nEnter choice: ").strip()
                
                if choice == "1":
                    self.player_menu()
                elif choice == "2":
                    self.team_menu()
                elif choice == "3":
                    self.play_match()
                    self.pause()
                elif choice == "4":
                    self.play_multiple_matches()
                    self.pause()
                elif choice == "5":
                    self.play_multiple_random_games()
                    self.pause()
                elif choice == "6":
                    self.tournament_menu()
                elif choice == "7":
                    self.view_all_teams()
                    self.pause()
                elif choice == "8":
                    self.quick_play()
                    self.pause()
                elif choice == "9":
                    self.settings_menu()
                elif choice == "0":
                    self.clear_screen()
                    print("\nGoodbye! 👋")
                    break
                else:
                    print("Invalid choice!")
                    self.pause()
        except KeyboardInterrupt:
            self.clear_screen()
            print("\n\nExiting Fantasy Football Manager... Goodbye! 👋")
            sys.exit(0)


def main():
    """Entry point."""
    app = FantasyFootballApp()
    app.run()


if __name__ == "__main__":
    main()