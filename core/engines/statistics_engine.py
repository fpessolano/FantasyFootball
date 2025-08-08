#!/usr/bin/env python3
"""
Player Statistics Manager
~~~~~~~~~~~~~~~~~~~~~~~~~

Handles player statistics tracking, rankings, and leaderboards.
"""

from typing import List, Dict, Tuple, Optional
from core.models import Player, Position
from collections import defaultdict


class PlayerStatisticsManager:
    """
    Manages player statistics, rankings, and leaderboards.
    """
    
    def __init__(self):
        """Initialize the statistics manager."""
        pass
    
    def update_match_stats(self, player: Player, stats_update: Dict[str, int], 
                          tournament: Optional[str] = None):
        """
        Update player statistics after a match.
        
        Args:
            player: The player to update
            stats_update: Dictionary of stat_name -> value to add
            tournament: Optional tournament name for per-tournament tracking
        """
        for stat_name, value in stats_update.items():
            # Update career stats
            if hasattr(player.stats, f'career_{stat_name}'):
                current_value = getattr(player.stats, f'career_{stat_name}')
                setattr(player.stats, f'career_{stat_name}', current_value + value)
            
            # Update tournament stats if tournament specified
            if tournament:
                player.stats.add_tournament_stat(tournament, stat_name, value)
    
    def get_top_scorers(self, players: List[Player], limit: int = 10, 
                       tournament: Optional[str] = None) -> List[Tuple[Player, int]]:
        """
        Get top goal scorers.
        
        Args:
            players: List of players to rank
            limit: Maximum number of players to return
            tournament: Optional tournament to filter by
            
        Returns:
            List of (player, goals) tuples sorted by goals descending
        """
        import heapq
        
        # Build list of (player, goals) tuples with list comprehension
        scorers = [
            (player, player.stats.get_tournament_stat(tournament, 'goals') if tournament else player.stats.career_goals)
            for player in players
        ]
        
        # Filter valid scorers and use heapq for efficient top-K selection
        valid_scorers = [(player, goals) for player, goals in scorers if goals > 0]
        return heapq.nlargest(limit, valid_scorers, key=lambda x: x[1])
    
    def get_top_assisters(self, players: List[Player], limit: int = 10,
                         tournament: Optional[str] = None) -> List[Tuple[Player, int]]:
        """Get top assist providers."""
        import heapq
        
        # Build list of (player, assists) tuples with list comprehension
        assisters = [
            (player, player.stats.get_tournament_stat(tournament, 'assists') if tournament else player.stats.career_assists)
            for player in players
        ]
        
        # Filter valid assisters and use heapq for efficient top-K selection
        valid_assisters = [(player, assists) for player, assists in assisters if assists > 0]
        return heapq.nlargest(limit, valid_assisters, key=lambda x: x[1])
    
    def get_clean_sheet_leaders(self, players: List[Player], limit: int = 10,
                               tournament: Optional[str] = None) -> List[Tuple[Player, int]]:
        """Get players with most clean sheets (typically goalkeepers)."""
        import heapq
        
        # Build list of (player, clean_sheets) tuples with list comprehension
        leaders = [
            (player, player.stats.get_tournament_stat(tournament, 'clean_sheets') if tournament else player.stats.career_clean_sheets)
            for player in players
        ]
        
        # Filter valid leaders and use heapq for efficient top-K selection
        valid_leaders = [(player, clean_sheets) for player, clean_sheets in leaders if clean_sheets > 0]
        return heapq.nlargest(limit, valid_leaders, key=lambda x: x[1])
    
    def get_most_disciplined(self, players: List[Player], limit: int = 10,
                           tournament: Optional[str] = None) -> List[Tuple[Player, int]]:
        """Get players with fewest cards (lower is better)."""
        disciplined = []
        for player in players:
            if tournament:
                yellow_cards = player.stats.get_tournament_stat(tournament, 'yellow_cards')
                red_cards = player.stats.get_tournament_stat(tournament, 'red_cards')
            else:
                yellow_cards = player.stats.career_yellow_cards
                red_cards = player.stats.career_red_cards
            
            total_cards = yellow_cards + (red_cards * 2)  # Red cards count double
            if player.stats.career_matches > 0:  # Only include players who have played
                disciplined.append((player, total_cards))
        
        disciplined.sort(key=lambda x: x[1])  # Ascending order (fewer cards is better)
        return disciplined[:limit]
    
    def get_most_appearances(self, players: List[Player], limit: int = 10,
                           tournament: Optional[str] = None) -> List[Tuple[Player, int]]:
        """Get players with most match appearances."""
        appearances = []
        for player in players:
            if tournament:
                matches = player.stats.get_tournament_stat(tournament, 'matches')
            else:
                matches = player.stats.career_matches
            
            if matches > 0:
                appearances.append((player, matches))
        
        appearances.sort(key=lambda x: x[1], reverse=True)
        return appearances[:limit]
    
    def get_player_efficiency_rating(self, player: Player, tournament: Optional[str] = None) -> float:
        """
        Calculate a composite efficiency rating for a player.
        Takes into account goals, assists, pass accuracy, etc.
        """
        if tournament:
            matches = player.stats.get_tournament_stat(tournament, 'matches')
            goals = player.stats.get_tournament_stat(tournament, 'goals')
            assists = player.stats.get_tournament_stat(tournament, 'assists')
            passes = player.stats.get_tournament_stat(tournament, 'passes')
            passes_completed = player.stats.get_tournament_stat(tournament, 'passes_completed')
        else:
            matches = player.stats.career_matches
            goals = player.stats.career_goals
            assists = player.stats.career_assists
            passes = player.stats.career_passes
            passes_completed = player.stats.career_passes_completed
        
        if matches == 0:
            return 0.0
        
        # Base rating from goals and assists per game
        attacking_rating = (goals + assists) / matches * 10
        
        # Pass accuracy bonus
        pass_accuracy = (passes_completed / passes * 100) if passes > 0 else 0
        accuracy_bonus = pass_accuracy / 10  # Up to 10 points for 100% accuracy
        
        # Position-specific adjustments
        if player.position == Position.GK:
            # Goalkeepers get bonus for clean sheets
            if tournament:
                clean_sheets = player.stats.get_tournament_stat(tournament, 'clean_sheets')
            else:
                clean_sheets = player.stats.career_clean_sheets
            attacking_rating = clean_sheets / matches * 15  # Clean sheets worth more for GK
        
        elif player.position in [Position.CB, Position.SW, Position.LB, Position.RB]:
            # Defenders get less weight on goals/assists, more on defensive actions
            attacking_rating *= 0.5
            # Add defensive bonuses (would need defensive stats implementation)
        
        return min(attacking_rating + accuracy_bonus, 100.0)  # Cap at 100
    
    def get_efficiency_leaders(self, players: List[Player], limit: int = 10,
                             tournament: Optional[str] = None) -> List[Tuple[Player, float]]:
        """Get players with highest efficiency ratings."""
        efficiency_list = []
        for player in players:
            rating = self.get_player_efficiency_rating(player, tournament)
            if rating > 0:
                efficiency_list.append((player, rating))
        
        efficiency_list.sort(key=lambda x: x[1], reverse=True)
        return efficiency_list[:limit]
    
    def print_leaderboard(self, title: str, leaderboard: List[Tuple[Player, any]], 
                         stat_name: str, format_spec: str = ""):
        """
        Print a formatted leaderboard.
        
        Args:
            title: Title of the leaderboard
            leaderboard: List of (player, value) tuples
            stat_name: Name of the statistic being displayed
            format_spec: Format specification for the value (e.g., ".1f" for floats)
        """
        print(f"\n🏆 {title}")
        print("=" * 50)
        
        if not leaderboard:
            print("No data available.")
            return
        
        for i, (player, value) in enumerate(leaderboard, 1):
            # Use f-string formatting directly instead of .format()
            if format_spec:
                formatted_value = f"{value:{format_spec}}"
            else:
                formatted_value = str(value)
            print(f"{i:2}. {player.name:<25} ({player.nationality}) - {formatted_value} {stat_name}")
    
    def generate_full_report(self, players: List[Player], tournament: Optional[str] = None):
        """Generate a comprehensive statistics report."""
        title_suffix = f" - {tournament}" if tournament else " - Career"
        
        print(f"\n📊 PLAYER STATISTICS REPORT{title_suffix}")
        print("=" * 60)
        
        # Top scorers
        top_scorers = self.get_top_scorers(players, 10, tournament)
        self.print_leaderboard("Top Goal Scorers", top_scorers, "goals")
        
        # Top assisters
        top_assisters = self.get_top_assisters(players, 10, tournament)
        self.print_leaderboard("Top Assist Providers", top_assisters, "assists")
        
        # Clean sheet leaders (for goalkeepers)
        gk_players = [p for p in players if p.position == Position.GK]
        clean_sheet_leaders = self.get_clean_sheet_leaders(gk_players, 5, tournament)
        self.print_leaderboard("Clean Sheet Leaders (GK)", clean_sheet_leaders, "clean sheets")
        
        # Most appearances
        most_appearances = self.get_most_appearances(players, 10, tournament)
        self.print_leaderboard("Most Appearances", most_appearances, "matches")
        
        # Efficiency leaders
        efficiency_leaders = self.get_efficiency_leaders(players, 10, tournament)
        self.print_leaderboard("Efficiency Leaders", efficiency_leaders, "rating", ".1f")
        
        # Most disciplined
        most_disciplined = self.get_most_disciplined(players, 10, tournament)
        self.print_leaderboard("Most Disciplined (Fewest Cards)", most_disciplined, "cards")
    
    def get_player_detailed_stats(self, player: Player, tournament: Optional[str] = None) -> Dict:
        """Get detailed statistics for a specific player."""
        if tournament:
            return {
                'matches': player.stats.get_tournament_stat(tournament, 'matches'),
                'minutes': player.stats.get_tournament_stat(tournament, 'minutes'),
                'goals': player.stats.get_tournament_stat(tournament, 'goals'),
                'assists': player.stats.get_tournament_stat(tournament, 'assists'),
                'saves': player.stats.get_tournament_stat(tournament, 'saves'),
                'clean_sheets': player.stats.get_tournament_stat(tournament, 'clean_sheets'),
                'yellow_cards': player.stats.get_tournament_stat(tournament, 'yellow_cards'),
                'red_cards': player.stats.get_tournament_stat(tournament, 'red_cards'),
                'motm': player.stats.get_tournament_stat(tournament, 'motm'),
            }
        else:
            return {
                'matches': player.stats.career_matches,
                'minutes': player.stats.career_minutes,
                'goals': player.stats.career_goals,
                'assists': player.stats.career_assists,
                'saves': player.stats.career_saves,
                'clean_sheets': player.stats.career_clean_sheets,
                'yellow_cards': player.stats.career_yellow_cards,
                'red_cards': player.stats.career_red_cards,
                'motm': player.stats.career_motm,
                'goals_per_game': player.stats.get_goals_per_game(),
                'assists_per_game': player.stats.get_assists_per_game(),
                'pass_accuracy': player.stats.get_pass_accuracy(),
                'efficiency_rating': self.get_player_efficiency_rating(player, tournament)
            }