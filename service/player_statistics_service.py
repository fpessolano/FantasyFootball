#!/usr/bin/env python3
"""
Player Statistics Service - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all player statistics and leaderboard functionality.
"""

class PlayerStatisticsService:
    """Service for player statistics and analytics operations."""
    
    def __init__(self, stats_manager, player_manager, tournament_manager):
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        self.tournament_manager = tournament_manager
    
    def show_career_leaders(self):
        """Show career statistics leaders."""
        print("=" * 60)
        print("🏆 CAREER STATISTICS LEADERS")
        print("=" * 60)
        
        # Goals leaders
        goals_leaders = self.stats_manager.get_top_scorers()
        if goals_leaders:
            print("\n⚽ Top Goal Scorers:")
            for i, (player_name, goals) in enumerate(goals_leaders[:10], 1):
                print(f"{i:2}. {player_name:<20} {goals:3} goals")
        
        # Assists leaders
        assists_leaders = self.stats_manager.get_top_assists()
        if assists_leaders:
            print("\n🎯 Top Assist Providers:")
            for i, (player_name, assists) in enumerate(assists_leaders[:10], 1):
                print(f"{i:2}. {player_name:<20} {assists:3} assists")
        
        # Appearances leaders
        appearances_leaders = self.stats_manager.get_most_appearances()
        if appearances_leaders:
            print("\n👕 Most Appearances:")
            for i, (player_name, appearances) in enumerate(appearances_leaders[:10], 1):
                print(f"{i:2}. {player_name:<20} {appearances:3} matches")
        
        # Clean sheets (goalkeepers)
        clean_sheets_leaders = self.stats_manager.get_most_clean_sheets()
        if clean_sheets_leaders:
            print("\n🥅 Most Clean Sheets (Goalkeepers):")
            for i, (player_name, clean_sheets) in enumerate(clean_sheets_leaders[:10], 1):
                print(f"{i:2}. {player_name:<20} {clean_sheets:3} clean sheets")
    
    def show_tournament_leaders(self):
        """Show tournament-specific statistics leaders."""
        tournaments = self.tournament_manager.get_completed_tournaments()
        if not tournaments:
            print("No completed tournaments found!")
            return
        
        print("\nSelect tournament:")
        for i, tournament in enumerate(tournaments, 1):
            print(f"{i}. {tournament.name}")
        
        try:
            choice = int(input("Choose tournament: ")) - 1
            if 0 <= choice < len(tournaments):
                tournament = tournaments[choice]
                self._show_tournament_stats(tournament)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def show_individual_analysis(self):
        """Show detailed analysis for individual player."""
        if not self.player_manager.players:
            print("No players found!")
            return
        
        # Show top players by rating
        top_players = self.player_manager.get_top_players(20)
        print("\nTop 20 players by rating:")
        for i, player in enumerate(top_players, 1):
            print(f"{i:2}. {player.name:<20} ({player.position.name}) OVR: {player.overall_rating():.0f}")
        
        try:
            choice = int(input("\nSelect player for detailed analysis: ")) - 1
            if 0 <= choice < len(top_players):
                player = top_players[choice]
                self._show_player_analysis(player)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
    
    def show_tournament_history(self):
        """Show tournament history."""
        history = self.tournament_manager.get_tournament_history()
        if not history:
            print("No tournament history found!")
            return
        
        print("=" * 60)
        print("🏆 TOURNAMENT HISTORY")
        print("=" * 60)
        
        for tournament_data in history:
            print(f"\n🏅 {tournament_data['name']}")
            print(f"   Winner: {tournament_data.get('winner', 'Unknown')}")
            print(f"   Date: {tournament_data.get('date', 'Unknown')}")
            if 'top_scorer' in tournament_data:
                print(f"   Top Scorer: {tournament_data['top_scorer']}")
    
    def show_performance_comparison(self):
        """Show performance comparison between players."""
        if len(self.player_manager.players) < 2:
            print("Need at least 2 players for comparison!")
            return
        
        print("Select players to compare:")
        
        # Select first player
        top_players = self.player_manager.get_top_players(20)
        print("\nPlayer 1:")
        for i, player in enumerate(top_players, 1):
            print(f"{i:2}. {player.name:<20} ({player.position.name})")
        
        try:
            choice1 = int(input("Select first player: ")) - 1
            if not (0 <= choice1 < len(top_players)):
                print("Invalid choice!")
                return
            player1 = top_players[choice1]
        except ValueError:
            print("Invalid input!")
            return
        
        # Select second player
        remaining_players = [p for p in top_players if p != player1]
        print("\nPlayer 2:")
        for i, player in enumerate(remaining_players, 1):
            print(f"{i:2}. {player.name:<20} ({player.position.name})")
        
        try:
            choice2 = int(input("Select second player: ")) - 1
            if not (0 <= choice2 < len(remaining_players)):
                print("Invalid choice!")
                return
            player2 = remaining_players[choice2]
        except ValueError:
            print("Invalid input!")
            return
        
        self._compare_players(player1, player2)
    
    def export_statistics(self):
        """Export statistics to file."""
        print("=" * 60)
        print("📤 EXPORT STATISTICS")
        print("=" * 60)
        
        print("\nExport options:")
        print("1. Career statistics (CSV)")
        print("2. Tournament statistics (CSV)")
        print("3. Player profiles (JSON)")
        print("4. Complete dataset (JSON)")
        
        try:
            choice = int(input("Select export option: "))
            filename = input("Enter filename (without extension): ").strip()
            
            if not filename:
                print("Filename cannot be empty!")
                return
            
            if choice == 1:
                self.stats_manager.export_career_stats(f"{filename}.csv")
                print(f"Career statistics exported to {filename}.csv")
            elif choice == 2:
                self.stats_manager.export_tournament_stats(f"{filename}.csv")
                print(f"Tournament statistics exported to {filename}.csv")
            elif choice == 3:
                self.stats_manager.export_player_profiles(f"{filename}.json")
                print(f"Player profiles exported to {filename}.json")
            elif choice == 4:
                self.stats_manager.export_complete_dataset(f"{filename}.json")
                print(f"Complete dataset exported to {filename}.json")
            else:
                print("Invalid choice!")
        
        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Export failed: {e}")
    
    def _show_tournament_stats(self, tournament):
        """Show statistics for a specific tournament."""
        print(f"\n🏆 {tournament.name} Statistics")
        print("=" * 50)
        
        # Get tournament stats
        stats = self.stats_manager.get_tournament_stats(tournament.id)
        
        if stats and 'top_scorer' in stats:
            print(f"🥇 Tournament Winner: {tournament.winner or 'Unknown'}")
            print(f"⚽ Top Scorer: {stats['top_scorer']['name']} ({stats['top_scorer']['goals']} goals)")
            
            if 'top_assists' in stats:
                print(f"🎯 Most Assists: {stats['top_assists']['name']} ({stats['top_assists']['assists']} assists)")
        else:
            print("No detailed statistics available for this tournament.")
    
    def _show_player_analysis(self, player):
        """Show detailed analysis for a player."""
        print(f"\n👤 {player.name} - Detailed Analysis")
        print("=" * 50)
        
        print(f"Position: {player.position.name}")
        print(f"Nationality: {player.nationality}")
        print(f"Overall Rating: {player.overall_rating():.1f}")
        
        # Get player stats
        stats = self.stats_manager.get_player_stats(player.name)
        
        if stats:
            print(f"\n📊 Career Statistics:")
            print(f"Matches Played: {stats.get('matches', 0)}")
            print(f"Goals: {stats.get('goals', 0)}")
            print(f"Assists: {stats.get('assists', 0)}")
            print(f"Yellow Cards: {stats.get('yellow_cards', 0)}")
            print(f"Red Cards: {stats.get('red_cards', 0)}")
            
            if player.position.name == 'GK':
                print(f"Clean Sheets: {stats.get('clean_sheets', 0)}")
        else:
            print("\nNo match statistics available yet.")
        
        # Show key attributes
        print(f"\n🔍 Key Attributes:")
        if hasattr(player, 'pace'):
            print(f"Pace: {player.pace}")
        if hasattr(player, 'shooting'):
            print(f"Shooting: {player.shooting}")
        if hasattr(player, 'passing'):
            print(f"Passing: {player.passing}")
        if hasattr(player, 'defending'):
            print(f"Defending: {player.defending}")
    
    def _compare_players(self, player1, player2):
        """Compare two players."""
        print(f"\n⚖️  Player Comparison")
        print("=" * 60)
        
        print(f"{'Attribute':<15} | {player1.name:<20} | {player2.name:<20}")
        print("-" * 60)
        
        print(f"{'Position':<15} | {player1.position.name:<20} | {player2.position.name:<20}")
        print(f"{'Nationality':<15} | {player1.nationality:<20} | {player2.nationality:<20}")
        print(f"{'Overall':<15} | {player1.overall_rating():<20.1f} | {player2.overall_rating():<20.1f}")
        
        # Compare key attributes if available
        if hasattr(player1, 'pace') and hasattr(player2, 'pace'):
            print(f"{'Pace':<15} | {player1.pace:<20} | {player2.pace:<20}")
        if hasattr(player1, 'shooting') and hasattr(player2, 'shooting'):
            print(f"{'Shooting':<15} | {player1.shooting:<20} | {player2.shooting:<20}")
        if hasattr(player1, 'passing') and hasattr(player2, 'passing'):
            print(f"{'Passing':<15} | {player1.passing:<20} | {player2.passing:<20}")
        if hasattr(player1, 'defending') and hasattr(player2, 'defending'):
            print(f"{'Defending':<15} | {player1.defending:<20} | {player2.defending:<20}")
        
        # Compare statistics
        stats1 = self.stats_manager.get_player_stats(player1.name)
        stats2 = self.stats_manager.get_player_stats(player2.name)
        
        if stats1 and stats2:
            print("\n📊 Career Statistics Comparison:")
            print(f"{'Statistic':<15} | {player1.name:<20} | {player2.name:<20}")
            print("-" * 60)
            print(f"{'Matches':<15} | {stats1.get('matches', 0):<20} | {stats2.get('matches', 0):<20}")
            print(f"{'Goals':<15} | {stats1.get('goals', 0):<20} | {stats2.get('goals', 0):<20}")
            print(f"{'Assists':<15} | {stats1.get('assists', 0):<20} | {stats2.get('assists', 0):<20}")