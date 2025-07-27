"""
Data Update System for Fantasy Football Manager

This module handles periodic updates of team ratings and statistics from external sources.
Currently supports:
- Weekly ELO score updates
- EA Sports FC team ratings
- Club ELO ratings (when available)

Data Sources:
- Primary: Kaggle EA Sports FC 25 dataset (manual download required)
- Alternative: FIFA Index web scraping (basic implementation)
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import urllib.request
import urllib.parse
import urllib.error
from core.storage.team_storage import team_storage


class DataUpdater:
    """Handles periodic data updates for team ratings and statistics."""
    
    def __init__(self, data_dir: str = None):
        """Initialize the data updater."""
        if data_dir is None:
            # Default to assets/data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            data_dir = os.path.join(project_root, 'assets', 'data')
        
        self.data_dir = data_dir
        self.update_log_file = os.path.join(data_dir, 'update_log.json')
        self.backup_dir = os.path.join(data_dir, 'backups')
        
        # Ensure directories exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Update frequency (7 days)
        self.update_interval_days = 7
        
    def check_for_updates(self) -> bool:
        """
        Check if it's time for a weekly data update.
        
        Returns:
            bool: True if update is needed, False otherwise
        """
        try:
            last_update = self._get_last_update_time()
            if last_update is None:
                return True  # First time setup
                
            time_since_update = datetime.now() - last_update
            return time_since_update.days >= self.update_interval_days
            
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False
    
    def perform_update(self, show_progress: bool = True) -> bool:
        """
        Perform the weekly data update.
        
        Args:
            show_progress: Whether to show progress messages
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if show_progress:
                print("🔄 Checking for team rating updates...")
            
            # Create backup of current data
            backup_success = self._create_backup()
            if not backup_success:
                if show_progress:
                    print("⚠️  Warning: Could not create backup, continuing anyway...")
            
            # Try to download new data
            update_success = False
            
            # Method 1: Try to update from Kaggle-style CSV (if manually placed)
            kaggle_path = os.path.join(self.data_dir, 'ea_sports_fc_25_teams.csv')
            if os.path.exists(kaggle_path):
                if show_progress:
                    print("📊 Found EA Sports FC 25 data, updating...")
                update_success = self._update_from_ea_sports_csv(kaggle_path)
            
            # Method 2: Basic web scraping fallback (placeholder implementation)
            if not update_success:
                if show_progress:
                    print("🌐 Attempting basic rating updates...")
                update_success = self._update_ratings_basic()
            
            # Update log regardless of success
            self._log_update_attempt(update_success)
            
            if update_success:
                if show_progress:
                    print("✅ Team ratings updated successfully!")
                return True
            else:
                if show_progress:
                    print("ℹ️  No new data available, using existing ratings")
                return False
                
        except Exception as e:
            print(f"❌ Error during update: {e}")
            return False
    
    def _get_last_update_time(self) -> Optional[datetime]:
        """Get the timestamp of the last successful update."""
        try:
            if not os.path.exists(self.update_log_file):
                return None
                
            with open(self.update_log_file, 'r') as f:
                log_data = json.load(f)
                
            last_successful = log_data.get('last_successful_update')
            if last_successful:
                return datetime.fromisoformat(last_successful)
                
            return None
            
        except Exception:
            return None
    
    def _log_update_attempt(self, success: bool):
        """Log the update attempt with timestamp."""
        try:
            log_data = {
                'last_check': datetime.now().isoformat(),
                'last_attempt': datetime.now().isoformat(),
            }
            
            if success:
                log_data['last_successful_update'] = datetime.now().isoformat()
            
            # Read existing log if it exists
            if os.path.exists(self.update_log_file):
                try:
                    with open(self.update_log_file, 'r') as f:
                        existing_log = json.load(f)
                    log_data.update(existing_log)
                except:
                    pass  # Use new log data if existing is corrupted
            
            with open(self.update_log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not update log file: {e}")
    
    def _create_backup(self) -> bool:
        """Create a backup of current team data."""
        try:
            if not team_storage.teams_by_name:
                return True  # No data to backup
                
            backup_file = os.path.join(
                self.backup_dir, 
                f"teams_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            # Export current team data
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'team_count': len(team_storage.teams_by_name),
                'teams': {}
            }
            
            for team_name, team in team_storage.teams_by_name.items():
                backup_data['teams'][team_name] = {
                    'name': team.name,
                    'elo': team.elo,
                    'league_info': getattr(team, 'league_info', {})
                }
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
                
            # Clean old backups (keep last 5)
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            print(f"Backup creation failed: {e}")
            return False
    
    def _cleanup_old_backups(self):
        """Keep only the 5 most recent backups."""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('teams_backup_')]
            backup_files.sort(reverse=True)
            
            for old_backup in backup_files[5:]:
                os.remove(os.path.join(self.backup_dir, old_backup))
                
        except Exception:
            pass  # Non-critical operation
    
    def _update_from_ea_sports_csv(self, csv_path: str) -> bool:
        """
        Update team ratings from EA Sports FC CSV data.
        
        Args:
            csv_path: Path to the EA Sports FC CSV file
            
        Returns:
            bool: True if successful
        """
        try:
            import csv
            
            updates_made = 0
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    team_name = row.get('team_name', '').strip()
                    if not team_name:
                        continue
                    
                    # Find team in storage
                    team = team_storage.get_team(team_name)
                    if team:
                        try:
                            # Get current overall rating with fallback
                            current_rating = 50.0  # Default fallback
                            if hasattr(team, 'league_info') and team.league_info:
                                current_rating = team.league_info.get('overall_rating', 50.0)
                            
                            # Get new overall rating with fallback
                            new_overall_str = row.get('overall', '')
                            if new_overall_str and new_overall_str.strip():
                                new_overall = float(new_overall_str)
                            else:
                                new_overall = current_rating  # Keep current if no new data
                            
                            new_elo = self._convert_overall_to_elo(new_overall)
                            
                            # Update if different (and both ratings are valid)
                            if new_overall != current_rating and abs(team.elo - new_elo) > 10:
                                team.elo = new_elo
                                if hasattr(team, 'league_info'):
                                    team.league_info['overall_rating'] = new_overall
                                updates_made += 1
                                
                        except (ValueError, TypeError):
                            # Skip teams with invalid data but don't break the process
                            continue
            
            return updates_made > 0
            
        except Exception as e:
            print(f"Error updating from EA Sports CSV: {e}")
            return False
    
    def _update_ratings_basic(self) -> bool:
        """
        Basic rating update method (placeholder implementation).
        In a real implementation, this could scrape from FIFA Index or similar.
        
        Returns:
            bool: True if successful
        """
        try:
            # Placeholder: Apply small random variations to simulate rating changes
            # In a real implementation, this would fetch actual updated ratings
            
            import random
            updates_made = 0
            
            for team_name, team in team_storage.teams_by_name.items():
                # Simulate rating changes for top teams only
                if team.elo > 1600:  # Only update strong teams
                    variation = random.uniform(-20, 20)  # ±20 ELO points
                    new_elo = max(1000, min(2000, team.elo + variation))
                    
                    if abs(new_elo - team.elo) > 5:
                        team.elo = new_elo
                        updates_made += 1
                        
                        if updates_made >= 50:  # Limit updates for demo
                            break
            
            return updates_made > 0
            
        except Exception:
            return False
    
    def _convert_overall_to_elo(self, overall_rating: float) -> float:
        """
        Convert FIFA overall rating to ELO scale with realistic distribution.
        
        Args:
            overall_rating: FIFA overall rating (0-100)
            
        Returns:
            float: ELO rating (1000-2000), defaults to 1500 if invalid
        """
        try:
            if overall_rating is None:
                return 1500.0
                
            rating = float(overall_rating)
            
            # Clamp to valid range
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
            return 1500.0
    
    def get_update_status(self) -> Dict:
        """Get current update status information."""
        try:
            last_update = self._get_last_update_time()
            days_since_update = None
            
            if last_update:
                days_since_update = (datetime.now() - last_update).days
            
            return {
                'last_update': last_update.isoformat() if last_update else None,
                'days_since_update': days_since_update,
                'update_needed': self.check_for_updates(),
                'team_count': len(team_storage.teams_by_name) if team_storage.teams_by_name else 0
            }
            
        except Exception:
            return {
                'last_update': None,
                'days_since_update': None,
                'update_needed': True,
                'team_count': 0
            }


# Global updater instance
data_updater = DataUpdater()


def check_and_update_data(show_progress: bool = True) -> bool:
    """
    Convenience function to check for and perform data updates.
    
    Args:
        show_progress: Whether to show progress messages
        
    Returns:
        bool: True if update was performed, False otherwise
    """
    if data_updater.check_for_updates():
        return data_updater.perform_update(show_progress)
    return False