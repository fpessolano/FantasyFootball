"""
Goals Calibration Module

This module loads and provides average goals per match data for different leagues
to ensure realistic match simulation results.
"""

import os
import pandas as pd
from typing import Dict, Optional


class GoalsCalibration:
    """Manages average goals per match data for different leagues."""
    
    def __init__(self):
        self.goals_data: Dict[str, float] = {}
        self._load_goals_data()
    
    def _load_goals_data(self):
        """Load average goals data from CSV file."""
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'league_average_goals.csv')
        
        try:
            df = pd.read_csv(csv_path)
            # Create a dictionary with league name as key
            for _, row in df.iterrows():
                # Handle different league name formats
                league_key = row['League'].replace(' ', '_')
                self.goals_data[league_key] = row['Average Goals per Match']
                
                # Also store with original name for flexibility
                self.goals_data[row['League']] = row['Average Goals per Match']
                
                # Store country-league combination
                country_league = f"{row['Country']}_{row['League']}"
                self.goals_data[country_league] = row['Average Goals per Match']
                
        except Exception as e:
            print(f"Warning: Could not load goals calibration data: {e}")
            # Set default average if file can't be loaded
            self.default_average = 2.75
    
    def get_league_average(self, league_name: str) -> float:
        """
        Get average goals per match for a specific league.
        
        Args:
            league_name: Name of the league
            
        Returns:
            Average goals per match for the league, or default if not found
        """
        # Try different variations of the league name
        variations = [
            league_name,
            league_name.replace('_', ' '),
            league_name.replace(' ', '_'),
        ]
        
        for variant in variations:
            if variant in self.goals_data:
                return self.goals_data[variant]
        
        # Return default if not found
        return getattr(self, 'default_average', 2.75)
    
    def get_team_league_average(self, team_name: str) -> Optional[float]:
        """
        Try to determine the league average based on team name.
        This searches through all leagues to find which one contains the team.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Average goals for the team's league, or None if not found
        """
        # Load team data to find their league
        import os
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'data')
        
        try:
            # Search through all country/league directories
            for country in os.listdir(data_dir):
                country_path = os.path.join(data_dir, country)
                if not os.path.isdir(country_path) or country in ['backups']:
                    continue
                    
                for league in os.listdir(country_path):
                    league_path = os.path.join(country_path, league)
                    if not os.path.isdir(league_path):
                        continue
                        
                    # Check if team exists in this league
                    team_file = os.path.join(league_path, f"{team_name}.csv")
                    if os.path.exists(team_file):
                        # Found the team, return this league's average
                        return self.get_league_average(league.replace('_', ' '))
                        
        except Exception:
            pass
            
        return None
    
    def get_calibration_factor(self, league_name: str, current_average: float) -> float:
        """
        Calculate a calibration factor to adjust goal generation.
        
        Args:
            league_name: Name of the league
            current_average: Current average goals in simulation
            
        Returns:
            Calibration factor to multiply goal probabilities
        """
        target_average = self.get_league_average(league_name)
        
        # Avoid division by zero
        if current_average == 0:
            return 1.0
            
        # Calculate factor to reach target average
        factor = target_average / current_average
        
        # Limit adjustment to reasonable range (0.7 to 1.3)
        return max(0.7, min(1.3, factor))


# Global instance
_calibration = None

def get_calibration():
    """Get the global calibration instance."""
    global _calibration
    if _calibration is None:
        _calibration = GoalsCalibration()
    return _calibration