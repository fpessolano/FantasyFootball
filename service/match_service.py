#!/usr/bin/env python3
"""
Match Service - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all match playing functionality.
"""


class MatchService:
    """Service for match playing operations."""
    
    def __init__(self, team_manager, player_manager, match_engine):
        self.team_manager = team_manager
        self.player_manager = player_manager
        self.match_engine = match_engine
    
    def select_teams(self, random_selection=False, create_teams=False):
        """Select teams based on parameters and return them."""
        if create_teams:
            # Create new random teams
            # Check if we need to generate more players
            if len(self.player_manager.players) < 50:
                print(f"\n🔄 Generating player pool...")
                players = self.player_manager.generate_player_pool(80)
                for p in players:
                    self.player_manager.add_player(p)
                print("✅ Player pool ready!")
            
            # Create two random teams
            print(f"\n🏗️  Creating random teams...")
            team1 = self.team_manager.create_random_team("Team Alpha", self.player_manager.players)
            team2 = self.team_manager.create_random_team("Team Beta", self.player_manager.players)
            
            if not team1 or not team2:
                print("❌ Failed to create teams!")
                return None, None
            
            print("✅ Teams created!")
            
            # Show detailed team info for newly created teams
            print(f"\n🏠 HOME TEAM: {team1.name}")
            print(f"   Formation: {team1.formation} | Style: {team1.style.name}")
            print(f"   Overall Strength: {team1.compute_strength():.1f}")
            print(f"   Starting Elo: {team1.elo_rating:.0f}")
            
            print(f"\n✈️  AWAY TEAM: {team2.name}")
            print(f"   Formation: {team2.formation} | Style: {team2.style.name}")
            print(f"   Overall Strength: {team2.compute_strength():.1f}")
            print(f"   Starting Elo: {team2.elo_rating:.0f}")
            
            return team1, team2
            
        else:
            # Use existing teams
            if len(self.team_manager.teams) < 2:
                print("\nNeed at least 2 teams to play matches!")
                return None, None
            
            if random_selection:
                # Randomly select two different teams
                import random
                available_teams = self.team_manager.teams.copy()
                random.shuffle(available_teams)
                home_team = available_teams[0]
                away_team = available_teams[1]
                
                print(f"\n🎲 Randomly selected teams:")
                print(f"   🏠 Home: {home_team.name}")
                print(f"   ✈️  Away: {away_team.name}")
                
                return home_team, away_team
            else:
                # Let user select teams
                return self._select_teams()
    
    def run_matches(self, home_team, away_team, num_matches=1, match_title="MATCH"):
        """Run one or multiple matches between two teams."""
        if num_matches == 1:
            # Single match logic
            print("=" * 60)
            print(match_title)
            print("=" * 60)
            
            # Show team info before match
            print(f"\n🏠 HOME: {home_team.name}")
            print(f"   Elo: {home_team.elo_rating:.0f} | Streak: {self._format_streak(home_team.streak_count)}")
            print(f"   Formation: {home_team.formation} | Style: {home_team.style.name}")
            
            print(f"\n✈️  AWAY: {away_team.name}")
            print(f"   Elo: {away_team.elo_rating:.0f} | Streak: {self._format_streak(away_team.streak_count)}")
            print(f"   Formation: {away_team.formation} | Style: {away_team.style.name}")
            
            input("\nPress Enter to simulate match...")
            
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
            
            return [result]
            
        else:
            # Multiple matches logic
            print("=" * 80)
            print(f"{match_title}: {home_team.name} vs {away_team.name}")
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
            
            input("\nPress Enter to start the series...")
            
            for match_num in range(1, num_matches + 1):
                if detailed_mode:
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
                    # Show full match result
                    self.match_engine.display_match_result(result)
                    
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
                        input("Press Enter for next match...")
            
            # Clear progress indicator for fast mode
            if not detailed_mode:
                print(f"\n✅ Completed {num_matches} matches!")

            input("Press Enter for series summary...")
            
            # Clear screen before final summary
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Final summary for multiple matches
            self._display_series_summary(home_team, away_team, num_matches, home_wins, away_wins, draws, 
                                       initial_home_elo, initial_away_elo, results)
            
            return results
    
    def _display_series_summary(self, home_team, away_team, num_matches, home_wins, away_wins, draws,
                              initial_home_elo, initial_away_elo, results):
        """Display summary statistics for a match series."""
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
    
    def quick_play(self):
        """Quick play with random teams."""
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
        input("\nPress Enter to simulate the instant match...")
        
        result = self.match_engine.simulate_match(team1, team2)
        self.match_engine.display_match_result(result)
    
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