"""
JSON-based Save System for Fantasy Football Manager

A modern, reliable save system that replaces the problematic shelve implementation.
Features compression, data integrity checks, and save metadata.
"""

import json
import os
import time
import hashlib
import gzip
from datetime import datetime
from typing import Optional, Dict, List, Any


class JsonEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles object serialization."""
    
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


class GameData:
    """
    JSON-based save system that's compatible with the existing GameData interface.
    
    This replaces the shelve-based system with a more reliable JSON approach that:
    - Properly handles nested dictionaries
    - Provides data integrity via checksums
    - Compresses saves to reduce disk usage
    - Includes save metadata for better UX
    - Maintains backward compatibility with the existing API
    """
    
    SAVE_VERSION = "1.0"
    
    def __init__(self, user_id: str = 'system', savefile: str = 'gamesaves'):
        """
        Initialize the save system.
        
        Args:
            user_id: User identifier
            savefile: Base name for save directory (for compatibility)
        """
        self.__id = user_id
        self.__save_dir = f"{savefile}_json"
        self.__metadata_file = os.path.join(self.__save_dir, "metadata.json")
        
        # Create save directory if it doesn't exist
        os.makedirs(self.__save_dir, exist_ok=True)
        
        # Load or create metadata
        self._load_metadata()
        
        # Update last login
        self._update_last_login()
    
    def _load_metadata(self):
        """Load or create the metadata file that tracks users and saves."""
        try:
            if os.path.exists(self.__metadata_file):
                with open(self.__metadata_file, 'r') as f:
                    self.__metadata = json.load(f)
            else:
                self.__metadata = {}
                
            # Ensure user exists in metadata
            if self.__id not in self.__metadata:
                self.__metadata[self.__id] = {
                    'saved_games': {},
                    'last_login': int(time.time()),
                    'created': datetime.now().isoformat()
                }
                self._save_metadata()
                
        except Exception as e:
            print(f"Warning: Could not load metadata: {e}")
            self.__metadata = {
                self.__id: {
                    'saved_games': {},
                    'last_login': int(time.time()),
                    'created': datetime.now().isoformat()
                }
            }
    
    def _save_metadata(self):
        """Save metadata to disk."""
        try:
            with open(self.__metadata_file, 'w') as f:
                json.dump(self.__metadata, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save metadata: {e}")
    
    def _update_last_login(self):
        """Update the last login timestamp for the current user."""
        if self.__id and self.__id in self.__metadata:
            self.__metadata[self.__id]['last_login'] = int(time.time())
            self._save_metadata()
    
    def _get_save_path(self, save_name: str) -> str:
        """Get the file path for a specific save."""
        # Sanitize save name to prevent directory traversal
        safe_name = "".join(c for c in save_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return os.path.join(self.__save_dir, f"{self.__id}_{safe_name}.sav.gz")
    
    def save_game(self, name: str, state: Any, force: bool = True) -> bool:
        """
        Save game state to disk.
        
        Args:
            name: Name of the save
            state: Game state to save (will be JSON encoded)
            force: Whether to overwrite existing saves
            
        Returns:
            Success status
        """
        if not self.__id:
            return False
            
        try:
            # Check if save exists and force is False
            if not force and name in self.__metadata[self.__id]['saved_games']:
                return False
            
            # Create save data structure
            save_data = {
                'version': self.SAVE_VERSION,
                'timestamp': datetime.now().isoformat(),
                'user_id': self.__id,
                'save_name': name,
                'game_state': state
            }
            
            # Add progress metadata if available
            if isinstance(state, dict):
                save_data['progress_info'] = {
                    'league_name': state.get('name', 'Unknown League'),
                    'match_day': state.get('week', 0),
                    'my_team': state.get('myTeam', 'Unknown'),
                    'my_position': state.get('myTeamPosition', 0),
                    'season': state.get('season', 1)
                }
            
            # Convert to JSON
            json_data = json.dumps(save_data, cls=JsonEncoder, indent=2)
            
            # Calculate checksum
            checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            # Create final save structure
            final_save = {
                'checksum': checksum,
                'data': json_data
            }
            
            # Get save path
            save_path = self._get_save_path(name)
            
            # Backup existing save if it exists
            if os.path.exists(save_path):
                backup_path = save_path + f".backup_{int(time.time())}"
                os.rename(save_path, backup_path)
                # Keep only last 3 backups
                self._cleanup_old_backups(save_path)
            
            # Write compressed save
            with gzip.open(save_path, 'wt', encoding='utf-8') as f:
                json.dump(final_save, f)
            
            # Update metadata
            self.__metadata[self.__id]['saved_games'][name] = {
                'timestamp': save_data['timestamp'],
                'progress_info': save_data.get('progress_info', {}),
                'file_size': os.path.getsize(save_path)
            }
            self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def read_game(self, name: str) -> Optional[str]:
        """
        Load game state from disk.
        
        Args:
            name: Name of the save to load
            
        Returns:
            JSON-encoded game state or None if not found
        """
        if not self.__id:
            return None
            
        try:
            save_path = self._get_save_path(name)
            
            if not os.path.exists(save_path):
                return None
            
            # Read compressed save
            with gzip.open(save_path, 'rt', encoding='utf-8') as f:
                final_save = json.load(f)
            
            # Verify checksum
            stored_checksum = final_save['checksum']
            json_data = final_save['data']
            calculated_checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            if stored_checksum != calculated_checksum:
                print(f"Warning: Save file '{name}' is corrupted!")
                return None
            
            # Parse save data
            save_data = json.loads(json_data)
            
            # Return just the game state as JSON string (for compatibility)
            return json.dumps(save_data['game_state'])
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def saved_game_list(self) -> List[str]:
        """
        Get list of saved game names.
        
        Returns:
            List of save names
        """
        if not self.__id or self.__id not in self.__metadata:
            return []
            
        return list(self.__metadata[self.__id].get('saved_games', {}).keys())
    
    def delete_saved_game(self, name: str) -> bool:
        """
        Delete a saved game.
        
        Args:
            name: Name of the save to delete
            
        Returns:
            Success status
        """
        if not self.__id:
            return False
            
        try:
            save_path = self._get_save_path(name)
            
            # Delete the save file
            if os.path.exists(save_path):
                os.remove(save_path)
            
            # Delete backups
            for filename in os.listdir(self.__save_dir):
                if filename.startswith(f"{self.__id}_{name}.sav.gz.backup_"):
                    os.remove(os.path.join(self.__save_dir, filename))
            
            # Update metadata
            if name in self.__metadata[self.__id]['saved_games']:
                del self.__metadata[self.__id]['saved_games'][name]
                self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
    
    def save_state(self, name: str, state: Any, force: bool = True) -> bool:
        """
        Save a state value (for compatibility with shelve interface).
        
        Args:
            name: State name
            state: State value
            force: Whether to overwrite
            
        Returns:
            Success status
        """
        if not self.__id:
            return False
            
        try:
            # Store states in metadata
            if not force and name in self.__metadata[self.__id]:
                return False
                
            self.__metadata[self.__id][name] = state
            self._save_metadata()
            return True
            
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
    
    def read_state(self, name: str) -> Any:
        """
        Read a state value.
        
        Args:
            name: State name
            
        Returns:
            State value or None
        """
        if not self.__id or self.__id not in self.__metadata:
            return None
            
        return self.__metadata[self.__id].get(name)
    
    def state_list(self) -> List[str]:
        """Get list of state names."""
        if not self.__id or self.__id not in self.__metadata:
            return []
            
        states = list(self.__metadata[self.__id].keys())
        # Remove internal keys
        for key in ['saved_games', 'last_login', 'created']:
            if key in states:
                states.remove(key)
        return states
    
    def delete_state(self, name: str) -> bool:
        """Delete a state value."""
        if not self.__id or self.__id not in self.__metadata:
            return False
            
        try:
            if name in self.__metadata[self.__id]:
                del self.__metadata[self.__id][name]
                self._save_metadata()
                return True
            return False
            
        except Exception as e:
            print(f"Error deleting state: {e}")
            return False
    
    def kill(self):
        """Remove all data for the current user."""
        if not self.__id:
            return
            
        try:
            # Delete all save files for this user
            for filename in os.listdir(self.__save_dir):
                if filename.startswith(f"{self.__id}_"):
                    os.remove(os.path.join(self.__save_dir, filename))
            
            # Remove from metadata
            if self.__id in self.__metadata:
                del self.__metadata[self.__id]
                self._save_metadata()
                
        except Exception as e:
            print(f"Error removing user data: {e}")
    
    def _cleanup_old_backups(self, save_path: str, keep: int = 3):
        """Keep only the most recent backups."""
        try:
            base_name = os.path.basename(save_path)
            backup_files = []
            
            for filename in os.listdir(self.__save_dir):
                if filename.startswith(f"{base_name}.backup_"):
                    backup_files.append(filename)
            
            # Sort by timestamp (newest first)
            backup_files.sort(reverse=True)
            
            # Delete old backups
            for old_backup in backup_files[keep:]:
                os.remove(os.path.join(self.__save_dir, old_backup))
                
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        # JSON system doesn't need explicit cleanup like shelve
        pass
    
    @classmethod
    def clean(cls, maximum_age_hours: int = 480):
        """
        Clean up old user profiles.
        
        Args:
            maximum_age_hours: Maximum age in hours before cleanup
        """
        # This would be implemented if needed
        pass
    
    # Additional methods for enhanced functionality
    
    def get_save_info(self, name: str) -> Optional[Dict]:
        """
        Get detailed information about a save without loading it.
        
        Args:
            name: Save name
            
        Returns:
            Save information dictionary or None
        """
        if not self.__id or self.__id not in self.__metadata:
            return None
            
        return self.__metadata[self.__id]['saved_games'].get(name)
    
    def list_saves_with_info(self) -> List[Dict]:
        """
        Get list of saves with metadata.
        
        Returns:
            List of save information dictionaries
        """
        if not self.__id or self.__id not in self.__metadata:
            return []
            
        saves = []
        for save_name, save_info in self.__metadata[self.__id]['saved_games'].items():
            save_data = {
                'save_name': save_name,
                'timestamp': save_info.get('timestamp', 'Unknown'),
                'file_size': save_info.get('file_size', 0)
            }
            # Add progress info if available
            if 'progress_info' in save_info:
                save_data.update(save_info['progress_info'])
            saves.append(save_data)
            
        # Sort by timestamp (newest first)
        saves.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return saves