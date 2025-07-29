#!/usr/bin/env python3
"""
Fantasy Football Manager
~~~~~~~~~~~~~~~~~~~~~~~~

Main application for the Fantasy Football simulation system.
"""

import os
import sys
from typing import Optional
from models import Position, TacticalStyle
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine


class FantasyFootballApp:
    """Main application class."""
    
    def __init__(self):
        self.player_manager = PlayerManager()
        self.team_manager = TeamManager()
        self.match_engine = MatchEngine()
    
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
        print("FANTASY FOOTBALL MANAGER v2.0")
        print("="*60)
        print("\n1. Player Management")
        print("2. Team Management")
        print("3. Play Single Match")
        print("4. Play Multiple Matches")
        print("5. Play Multiple Matches (Random Teams)")
        print("6. View Rankings")
        print("7. Quick Play (Random Teams)")
        print("8. Settings")
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
            print("5. Delete Team")
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
        name = input("Enter team name: ").strip()
        team = self.team_manager.find_team_by_name(name)
        
        if not team:
            print("Team not found!")
            return
        
        print(team.summary())
    
    def delete_team(self):
        """Delete a team."""
        name = input("Enter team name to delete: ").strip()
        team = self.team_manager.find_team_by_name(name)
        
        if not team:
            print("Team not found!")
            return
        
        confirm = input(f"Delete team '{team.name}'? (y/n): ").strip().lower()
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
        self.clear_screen()
        print("Welcome to Fantasy Football Manager v2.0!")
        self.pause()
        
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
                self.view_all_teams()
                self.pause()
            elif choice == "7":
                self.quick_play()
                self.pause()
            elif choice == "8":
                self.settings_menu()
            elif choice == "0":
                self.clear_screen()
                print("\nGoodbye! 👋")
                break
            else:
                print("Invalid choice!")
                self.pause()


def main():
    """Entry point."""
    app = FantasyFootballApp()
    app.run()


if __name__ == "__main__":
    main()