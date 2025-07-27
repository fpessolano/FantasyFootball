"""
Improved save/load system for Fantasy Football Manager

Features:
- JSON-based storage (more portable than shelve)
- Atomic saves to prevent corruption
- Better error handling
- Context manager support
- Save metadata (timestamps, versions)
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil


class SaveGameManager:
    """Modern save game management system using JSON storage."""
    
    def __init__(self, user_id: str = 'system', save_dir: str = 'saves_json'):
        """
        Initialize save game manager.
        
        Args:
            user_id: User identifier
            save_dir: Directory to store save files
        """
        self.user_id = user_id
        self.save_dir = Path(save_dir)
        self.user_dir = self.save_dir / user_id
        
        # Create directories if they don't exist
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        # Update metadata
        self._update_metadata()
    
    def _update_metadata(self):
        """Update user metadata file."""
        metadata_file = self.user_dir / 'metadata.json'
        metadata = {}
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            except:
                metadata = {}
        
        metadata['last_login'] = datetime.now().isoformat()
        metadata['user_id'] = self.user_id
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def save_game(self, save_name: str, game_state: Dict[str, Any], 
                  description: str = "") -> bool:
        """
        Save game state to file.
        
        Args:
            save_name: Name of the save
            game_state: Game state dictionary
            description: Optional save description
            
        Returns:
            True if successful, False otherwise
        """
        try:
            save_file = self.user_dir / f"{save_name}.json"
            temp_file = self.user_dir / f"{save_name}.tmp"
            
            # Prepare save data with metadata
            save_data = {
                'metadata': {
                    'save_name': save_name,
                    'timestamp': datetime.now().isoformat(),
                    'description': description,
                    'version': '0.9.0'
                },
                'game_state': game_state
            }
            
            # Write to temporary file first (atomic save)
            with open(temp_file, 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
            
            # Move temp file to actual save file
            shutil.move(str(temp_file), str(save_file))
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                temp_file.unlink()
            return False
    
    def load_game(self, save_name: str) -> Optional[Dict[str, Any]]:
        """
        Load game state from file.
        
        Args:
            save_name: Name of the save to load
            
        Returns:
            Game state dictionary or None if not found/error
        """
        try:
            save_file = self.user_dir / f"{save_name}.json"
            
            if not save_file.exists():
                return None
            
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            return save_data.get('game_state', save_data)
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def list_saves(self) -> List[Dict[str, str]]:
        """
        List all saved games with metadata.
        
        Returns:
            List of save information dictionaries
        """
        saves = []
        
        for save_file in self.user_dir.glob("*.json"):
            if save_file.name == 'metadata.json':
                continue
                
            try:
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                
                metadata = save_data.get('metadata', {})
                saves.append({
                    'name': save_file.stem,
                    'timestamp': metadata.get('timestamp', 'Unknown'),
                    'description': metadata.get('description', ''),
                    'file': str(save_file)
                })
            except:
                # If can't read metadata, just add basic info
                saves.append({
                    'name': save_file.stem,
                    'timestamp': 'Unknown',
                    'description': '',
                    'file': str(save_file)
                })
        
        # Sort by timestamp (newest first)
        saves.sort(key=lambda x: x['timestamp'], reverse=True)
        return saves
    
    def delete_save(self, save_name: str) -> bool:
        """
        Delete a saved game.
        
        Args:
            save_name: Name of the save to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            save_file = self.user_dir / f"{save_name}.json"
            if save_file.exists():
                save_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
    
    def save_exists(self, save_name: str) -> bool:
        """Check if a save exists."""
        return (self.user_dir / f"{save_name}.json").exists()
    
    def get_save_info(self, save_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific save."""
        try:
            save_file = self.user_dir / f"{save_name}.json"
            if not save_file.exists():
                return None
                
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            return save_data.get('metadata', {})
        except:
            return None
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        pass


