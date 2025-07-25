"""
Team Storage Optimization System

This module provides an optimized team storage system with O(1) lookups
and league-based classification, designed for regular internet data updates.

Key Features:
- O(1) team lookups by name
- League-based organization for efficient filtering
- Support for regular data updates from internet sources
- Backward compatibility with existing Team objects
"""

import csv
from typing import Dict, List, Optional, Tuple
from core.entities.team import Team
from core.storage.elo_estimator import elo_estimator, TeamMetrics


class TeamStorage:
    """
    Optimized team storage with league classification and O(1) lookups.
    
    Storage structure:
    teams_by_name: {team_name: Team} - O(1) lookup by team name
    teams_by_league: {league_name: {country: [Team]}} - Organized by league/country
    league_metadata: {league_name: {country: metadata}} - League information
    """
    
    def __init__(self):
        self.teams_by_name: Dict[str, Team] = {}
        self.teams_by_league: Dict[str, Dict[str, List[Team]]] = {}
        self.league_metadata: Dict[str, Dict[str, dict]] = {}
        self._loaded_from_raw = False
        self._teams_with_estimated_elo: set = set()  # Track teams with estimated ELO
    
    def load_from_raw_data(self, csv_path: str, fifa_version: float = 24.0) -> bool:
        """
        Load teams from raw CSV data (internet updates format).
        
        Args:
            csv_path: Path to male_teams.csv file
            fifa_version: FIFA version to filter by
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Clear existing data
            self.teams_by_name.clear()
            self.teams_by_league.clear()
            self.league_metadata.clear()
            self._teams_with_estimated_elo.clear()
            
            # Read CSV using built-in csv module - Two-pass approach for ELO estimation
            all_rows = []
            teams_needing_estimation = []
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                all_rows = list(reader)
                
            # First pass: Build reference database for ELO estimation
            for row in all_rows:
                try:
                    if (float(row['fifa_version']) != fifa_version or 
                        row['league_name'] == 'Friendly International'):
                        continue
                        
                    team_name = row['team_name']
                    league_name = row['league_name'] 
                    country = row['nationality_name']
                    
                    if not team_name or not league_name or not country:
                        continue
                    
                    # If team has valid overall rating, add to reference database
                    if row['overall'] and row['overall'].strip():
                        try:
                            overall_rating = float(row['overall'])
                            if 30 <= overall_rating <= 100:
                                metrics = self._create_team_metrics(row, team_name, league_name, country)
                                calculated_elo = self._calculate_elo_from_overall(overall_rating)
                                elo_estimator.add_known_team(team_name, calculated_elo, metrics)
                        except (ValueError, TypeError):
                            teams_needing_estimation.append(row)
                    else:
                        teams_needing_estimation.append(row)
                        
                except (ValueError, TypeError, KeyError):
                    continue
                
            # Second pass: Process all teams with ELO estimation for missing data
            for row in all_rows:
                try:
                    # Filter by FIFA version and exclude international teams
                    if (float(row['fifa_version']) != fifa_version or 
                        row['league_name'] == 'Friendly International'):
                        continue
                        
                    team_name = row['team_name']
                    league_name = row['league_name'] 
                    country = row['nationality_name']
                    
                    # Skip teams with empty names
                    if not team_name or not league_name or not country:
                        continue
                    
                    # Get or estimate ELO
                    overall_rating = None
                    calculated_elo = None
                    
                    if row['overall'] and row['overall'].strip():
                        try:
                            overall_rating = float(row['overall'])
                            if 30 <= overall_rating <= 100:
                                calculated_elo = self._calculate_elo_from_overall(overall_rating)
                        except (ValueError, TypeError):
                            pass
                    
                    # If no valid ELO, estimate using similarity
                    if calculated_elo is None:
                        metrics = self._create_team_metrics(row, team_name, league_name, country)
                        calculated_elo = elo_estimator.estimate_elo(metrics, league_context=True)
                        # Track teams with estimated ELO
                        self._teams_with_estimated_elo.add(team_name)
                        # Store estimation info for debugging
                        confidence = elo_estimator.get_estimation_confidence(metrics)
                        if hasattr(self, '_estimation_log'):
                            self._estimation_log = getattr(self, '_estimation_log', [])
                            self._estimation_log.append(f"{team_name}: ELO {calculated_elo:.0f} (confidence: {confidence})")
                    
                    # Parse other numeric values with fallbacks
                    try:
                        if overall_rating is None:
                            overall_rating = float(row['overall']) if row['overall'] else 50.0
                        attack = float(row['attack']) if row['attack'] else 50.0
                        midfield = float(row['midfield']) if row['midfield'] else 50.0
                        defence = float(row['defence']) if row['defence'] else 50.0
                        transfer_budget = float(row.get('transfer_budget_eur', 0)) if row.get('transfer_budget_eur') else 0.0
                        club_worth = float(row.get('club_worth_eur', 0)) if row.get('club_worth_eur') else 0.0
                        team_id = int(row['team_id']) if row['team_id'] else 0
                        league_level = int(row.get('league_level', 1)) if row.get('league_level') else 1
                    except (ValueError, TypeError):
                        continue  # Skip teams with invalid data
                    
                    # Create Team object
                    team = Team(
                        name=team_name,
                        elo=calculated_elo
                    )
                    
                    # Store additional team metadata
                    team.league_info = {
                        'league_name': league_name,
                        'country': country,
                        'overall_rating': overall_rating,
                        'attack': attack,
                        'midfield': midfield,
                        'defence': defence,
                        'transfer_budget': transfer_budget,
                        'club_worth': club_worth,
                        'home_stadium': row.get('home_stadium', ''),
                        'team_id': team_id
                    }
                    
                    # Store in lookup structures
                    self.teams_by_name[team_name] = team
                    
                    # Organize by league and country
                    if league_name not in self.teams_by_league:
                        self.teams_by_league[league_name] = {}
                    if country not in self.teams_by_league[league_name]:
                        self.teams_by_league[league_name][country] = []
                    
                    self.teams_by_league[league_name][country].append(team)
                    
                    # Store league metadata
                    if league_name not in self.league_metadata:
                        self.league_metadata[league_name] = {}
                    if country not in self.league_metadata[league_name]:
                        self.league_metadata[league_name][country] = {
                            'team_count': 0,
                            'avg_rating': 0,
                            'league_level': league_level
                        }
                    
                    # Update metadata
                    meta = self.league_metadata[league_name][country]
                    meta['team_count'] += 1
                    
                except (ValueError, TypeError, KeyError):
                    # Skip individual team if there are issues
                    continue
                
            # Calculate league averages
            self._calculate_league_averages()
            self._loaded_from_raw = True
            
            return True
            
        except Exception as e:
            print(f"Error loading team data: {e}")
            return False
    
    def get_team(self, team_name: str) -> Optional[Team]:
        """Get team by name - O(1) lookup."""
        return self.teams_by_name.get(team_name)
    
    def get_league_teams(self, league_name: str, country: str = None) -> List[Team]:
        """Get all teams from a specific league/country."""
        if league_name not in self.teams_by_league:
            return []
        
        if country:
            return self.teams_by_league[league_name].get(country, [])
        
        # Return teams from all countries in this league
        all_teams = []
        for country_teams in self.teams_by_league[league_name].values():
            all_teams.extend(country_teams)
        return all_teams
    
    def get_available_leagues(self) -> List[Tuple[str, str, int]]:
        """
        Get list of available leagues with team counts.
        
        Returns:
            List of (league_name, country, team_count) tuples
        """
        leagues = []
        for league_name, countries in self.teams_by_league.items():
            for country, teams in countries.items():
                if len(teams) > 10:  # Only leagues with sufficient teams
                    leagues.append((league_name, country, len(teams)))
        
        return sorted(leagues, key=lambda x: (-x[2], x[0], x[1]))  # Sort by team count desc, then name
    
    def get_leagues_by_country(self) -> Dict[str, List[Tuple[str, int, bool]]]:
        """
        Get leagues grouped by country with ELO estimation status.
        
        Returns:
            Dict[country, List[(league_name, team_count, has_estimated_elo)]]
        """
        leagues_by_country = {}
        
        for league_name, countries in self.teams_by_league.items():
            for country, teams in countries.items():
                if len(teams) > 10:  # Only leagues with sufficient teams
                    # Check if any teams in this league have estimated ELO
                    has_estimated = any(team.name in self._teams_with_estimated_elo for team in teams)
                    
                    if country not in leagues_by_country:
                        leagues_by_country[country] = []
                    
                    leagues_by_country[country].append((league_name, len(teams), has_estimated))
        
        # Sort countries alphabetically and leagues by team count within each country
        for country in leagues_by_country:
            leagues_by_country[country].sort(key=lambda x: (-x[1], x[0]))  # Sort by team count desc, then name
        
        return dict(sorted(leagues_by_country.items()))  # Sort countries alphabetically
    
    def has_estimated_elo_teams(self, league_name: str, country: str) -> bool:
        """Check if a league has teams with estimated ELO."""
        teams = self.get_league_teams(league_name, country)
        return any(team.name in self._teams_with_estimated_elo for team in teams)
    
    def get_estimated_elo_count(self, league_name: str, country: str) -> int:
        """Get count of teams with estimated ELO in a league."""
        teams = self.get_league_teams(league_name, country)
        return sum(1 for team in teams if team.name in self._teams_with_estimated_elo)
    
    def get_random_teams(self, count: int, min_rating: int = 0, max_rating: int = 100) -> List[Team]:
        """Get random teams within rating range."""
        import random
        
        eligible_teams = [
            team for team in self.teams_by_name.values()
            if min_rating <= team.league_info.get('overall_rating', 50) <= max_rating
        ]
        
        if len(eligible_teams) < count:
            return eligible_teams
        
        return random.sample(eligible_teams, count)
    
    def search_teams(self, query: str, limit: int = 20) -> List[Team]:
        """Search teams by name (case insensitive)."""
        query_lower = query.lower()
        matches = []
        
        for team_name, team in self.teams_by_name.items():
            if query_lower in team_name.lower():
                matches.append(team)
                if len(matches) >= limit:
                    break
        
        return matches
    
    def get_statistics(self) -> dict:
        """Get storage statistics."""
        return {
            'total_teams': len(self.teams_by_name),
            'total_leagues': len(self.teams_by_league),
            'loaded_from_raw': self._loaded_from_raw,
            'leagues_with_10plus_teams': len([
                (league, country) for league, countries in self.teams_by_league.items()
                for country, teams in countries.items() if len(teams) > 10
            ])
        }
    
    def _calculate_elo_from_overall(self, overall_rating: float) -> float:
        """
        Convert FIFA overall rating to ELO with realistic distribution.
        
        Args:
            overall_rating: FIFA overall rating (0-100)
            
        Returns:
            float: ELO rating (1000-2000), defaults to 1500 if invalid
        """
        try:
            if overall_rating is None:
                return 1500.0
                
            rating = float(overall_rating)
            
            # Clamp rating to valid range
            if rating < 0:
                rating = 0
            elif rating > 100:
                rating = 100
            
            # More realistic ELO conversion with bell curve distribution
            # FIFA ratings 45-85 cover most teams, map to ELO 1200-1800
            if rating <= 45:
                # Very weak teams: 0-45 overall → 1000-1200 ELO
                elo = 1000 + (rating / 45) * 200
            elif rating <= 85:
                # Normal distribution: 45-85 overall → 1200-1800 ELO  
                normalized = (rating - 45) / 40  # 0-1 range
                elo = 1200 + normalized * 600
            else:
                # Elite teams: 85-100 overall → 1800-2000 ELO
                normalized = (rating - 85) / 15  # 0-1 range
                elo = 1800 + normalized * 200
            
            return float(elo)
            
        except (ValueError, TypeError, OverflowError):
            # Return default ELO for any invalid input
            return 1500.0
    
    def _create_team_metrics(self, row: dict, team_name: str, league_name: str, country: str) -> TeamMetrics:
        """Create TeamMetrics object from CSV row data."""
        def safe_float(value, default=None):
            try:
                return float(value) if value and str(value).strip() else default
            except (ValueError, TypeError):
                return default
        
        def safe_int(value, default=None):
            try:
                return int(value) if value and str(value).strip() else default
            except (ValueError, TypeError):
                return default
        
        return TeamMetrics(
            overall=safe_float(row.get('overall')),
            attack=safe_float(row.get('attack')),
            midfield=safe_float(row.get('midfield')),
            defence=safe_float(row.get('defence')),
            international_prestige=safe_float(row.get('international_prestige')),
            domestic_prestige=safe_float(row.get('domestic_prestige')),
            club_worth_eur=safe_float(row.get('club_worth_eur')),
            transfer_budget_eur=safe_float(row.get('transfer_budget_eur')),
            league_level=safe_int(row.get('league_level')),
            team_name=team_name,
            league_name=league_name,
            country=country
        )

    def _calculate_league_averages(self):
        """Calculate average ratings for each league."""
        for league_name, countries in self.teams_by_league.items():
            for country, teams in countries.items():
                if teams:
                    avg_rating = sum(team.league_info['overall_rating'] for team in teams) / len(teams)
                    self.league_metadata[league_name][country]['avg_rating'] = round(avg_rating, 1)


# Global team storage instance
team_storage = TeamStorage()


def initialize_team_storage(csv_path: str = None) -> bool:
    """
    Initialize the global team storage system.
    
    Args:
        csv_path: Path to raw team data, defaults to assets/raw/male_teams.csv
        
    Returns:
        bool: True if successful
    """
    if csv_path is None:
        import os
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'raw', 'male_teams.csv')
    
    return team_storage.load_from_raw_data(csv_path)


def get_team_by_name(team_name: str) -> Optional[Team]:
    """Convenience function for O(1) team lookup."""
    return team_storage.get_team(team_name)


def get_teams_by_league(league_name: str, country: str = None) -> List[Team]:
    """Convenience function to get teams by league."""
    return team_storage.get_league_teams(league_name, country)