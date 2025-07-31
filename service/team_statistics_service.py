#!/usr/bin/env python3
"""
Team Statistics Service - New service for team statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all team statistics and leaderboard functionality.
"""


class TeamStatisticsService:
    """Service for team statistics and analytics operations."""
    
    def __init__(self, team_manager, tournament_manager):
        self.team_manager = team_manager
        self.tournament_manager = tournament_manager
    
    def show_tournament_history(self):
        """Show tournament history with team winners."""
        print("=" * 60)
        print("🏆 TOURNAMENT HISTORY")
        print("=" * 60)
        
        print("\nTournament history tracking is not yet implemented.")
        print("This feature will be available in a future version.")
    
    def show_overall_ranking(self):
        """Show overall team rankings based on Elo ratings."""
        if not self.team_manager.teams:
            print("No teams found!")
            return
        
        print("=" * 60)
        print("📊 OVERALL TEAM RANKINGS")
        print("=" * 60)
        
        # Sort teams by Elo rating
        sorted_teams = sorted(
            self.team_manager.teams, 
            key=lambda t: t.elo_rating, 
            reverse=True
        )
        
        print(f"\n{'Rank':<6}{'Team Name':<25}{'Elo Rating':<12}{'Streak':<10}")
        print("-" * 60)
        
        for i, team in enumerate(sorted_teams, 1):
            streak_display = self._format_streak(team.streak_count)
            print(f"{i:<6}{team.name:<25}{team.elo_rating:<12.0f}{streak_display:<10}")
        
        # Show some statistics
        if len(sorted_teams) > 0:
            highest_elo = sorted_teams[0].elo_rating
            lowest_elo = sorted_teams[-1].elo_rating
            avg_elo = sum(t.elo_rating for t in sorted_teams) / len(sorted_teams)
            
            print(f"\n📈 Rating Statistics:")
            print(f"   Highest: {highest_elo:.0f} ({sorted_teams[0].name})")
            print(f"   Lowest: {lowest_elo:.0f} ({sorted_teams[-1].name})")
            print(f"   Average: {avg_elo:.0f}")
            print(f"   Range: {highest_elo - lowest_elo:.0f} points")
        
        # Show teams with active streaks
        hot_teams = [t for t in sorted_teams if t.streak_count >= 3]
        cold_teams = [t for t in sorted_teams if t.streak_count <= -3]
        
        if hot_teams:
            print(f"\n🔥 Hot Streaks:")
            for team in hot_teams:
                print(f"   {team.name}: {team.streak_count}W")
        
        if cold_teams:
            print(f"\n❄️  Cold Streaks:")
            for team in cold_teams:
                print(f"   {team.name}: {abs(team.streak_count)}L")
    
    def _format_streak(self, streak_count):
        """Format streak count for display."""
        if streak_count > 0:
            return f"{streak_count}W"
        elif streak_count < 0:
            return f"{abs(streak_count)}L"
        else:
            return "-"