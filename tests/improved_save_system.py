#!/usr/bin/env python3
"""
Improved Save System Design

This module demonstrates a better save/load system for the Fantasy Football Manager.
It addresses the current issues with shelve and provides a more robust solution.
"""

import json
import os
import time
import hashlib
import gzip
from datetime import datetime
from typing import Optional, Dict, List
import sqlite3

class ImprovedSaveSystem:
    """
    Improved save system with better reliability and features.
    
    Features:
    - JSON-based for readability and compatibility
    - Compression to reduce file size
    - Save metadata and versioning
    - Data integrity checks
    - Multiple save slots with info
    - Automatic backups
    """
    
    SAVE_VERSION = "1.0"
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
    def save_game(self, user_id: str, save_name: str, game_data: dict) -> bool:
        """
        Save game with metadata and compression.
        
        Args:
            user_id: User identifier
            save_name: Name of the save
            game_data: League/game state data
            
        Returns:
            Success status
        """
        try:
            # Create save metadata
            save_metadata = {
                "version": self.SAVE_VERSION,
                "user_id": user_id,
                "save_name": save_name,
                "timestamp": datetime.now().isoformat(),
                "game_data": game_data
            }
            
            # Add game progress info for quick display
            if isinstance(game_data, dict):
                save_metadata["progress_info"] = {
                    "league_name": game_data.get("name", "Unknown"),
                    "match_day": game_data.get("week", 0),
                    "my_team": game_data.get("myTeam", "Unknown"),
                    "position": game_data.get("myTeamPosition", 0)
                }
            
            # Convert to JSON
            json_data = json.dumps(save_metadata, indent=2)
            
            # Calculate checksum for integrity
            checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            # Create final save structure
            final_save = {
                "checksum": checksum,
                "data": json_data
            }
            
            # Compress and save
            save_path = os.path.join(self.save_dir, f"{user_id}_{save_name}.sav")
            
            # Backup existing save if it exists
            if os.path.exists(save_path):
                backup_path = save_path + f".backup_{int(time.time())}"
                os.rename(save_path, backup_path)
                # Keep only last 3 backups
                self._cleanup_old_backups(save_path)
            
            # Write compressed save
            with gzip.open(save_path, 'wt', encoding='utf-8') as f:
                json.dump(final_save, f)
                
            return True
            
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def load_game(self, user_id: str, save_name: str) -> Optional[dict]:
        """
        Load game with integrity verification.
        
        Args:
            user_id: User identifier
            save_name: Name of the save
            
        Returns:
            Game data or None if failed
        """
        try:
            save_path = os.path.join(self.save_dir, f"{user_id}_{save_name}.sav")
            
            if not os.path.exists(save_path):
                return None
                
            # Read compressed save
            with gzip.open(save_path, 'rt', encoding='utf-8') as f:
                final_save = json.load(f)
                
            # Verify checksum
            stored_checksum = final_save["checksum"]
            json_data = final_save["data"]
            
            calculated_checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            if stored_checksum != calculated_checksum:
                print("Save file corrupted - checksum mismatch!")
                return None
                
            # Parse save data
            save_metadata = json.loads(json_data)
            
            # Check version compatibility
            if save_metadata["version"] != self.SAVE_VERSION:
                print(f"Save version mismatch: {save_metadata['version']} vs {self.SAVE_VERSION}")
                # In a real system, you'd have migration logic here
                
            return save_metadata["game_data"]
            
        except Exception as e:
            print(f"Load failed: {e}")
            return None
    
    def list_saves(self, user_id: str) -> List[Dict]:
        """
        List all saves for a user with metadata.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of save information
        """
        saves = []
        
        try:
            for filename in os.listdir(self.save_dir):
                if filename.startswith(f"{user_id}_") and filename.endswith(".sav"):
                    # Extract save name
                    save_name = filename[len(user_id)+1:-4]
                    
                    # Try to load metadata without full game data
                    save_path = os.path.join(self.save_dir, filename)
                    
                    try:
                        with gzip.open(save_path, 'rt', encoding='utf-8') as f:
                            final_save = json.load(f)
                            save_metadata = json.loads(final_save["data"])
                            
                        save_info = {
                            "save_name": save_name,
                            "timestamp": save_metadata["timestamp"],
                            "progress_info": save_metadata.get("progress_info", {}),
                            "file_size": os.path.getsize(save_path)
                        }
                        saves.append(save_info)
                        
                    except Exception:
                        # Skip corrupted saves
                        continue
                        
            # Sort by timestamp (newest first)
            saves.sort(key=lambda x: x["timestamp"], reverse=True)
            
        except Exception as e:
            print(f"Failed to list saves: {e}")
            
        return saves
    
    def delete_save(self, user_id: str, save_name: str) -> bool:
        """Delete a save file and its backups."""
        try:
            save_path = os.path.join(self.save_dir, f"{user_id}_{save_name}.sav")
            
            # Delete main save
            if os.path.exists(save_path):
                os.remove(save_path)
                
            # Delete backups
            for filename in os.listdir(self.save_dir):
                if filename.startswith(f"{user_id}_{save_name}.sav.backup_"):
                    os.remove(os.path.join(self.save_dir, filename))
                    
            return True
            
        except Exception as e:
            print(f"Delete failed: {e}")
            return False
    
    def _cleanup_old_backups(self, save_path: str, keep: int = 3):
        """Keep only the most recent backups."""
        backup_files = []
        base_name = os.path.basename(save_path)
        
        for filename in os.listdir(self.save_dir):
            if filename.startswith(f"{base_name}.backup_"):
                backup_files.append(filename)
                
        # Sort by timestamp (newest first)
        backup_files.sort(reverse=True)
        
        # Delete old backups
        for old_backup in backup_files[keep:]:
            os.remove(os.path.join(self.save_dir, old_backup))


class SQLiteSaveSystem:
    """
    Alternative implementation using SQLite for better performance
    and concurrent access.
    """
    
    def __init__(self, db_path: str = "saves.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize the SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS saves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    save_name TEXT NOT NULL,
                    game_data TEXT NOT NULL,
                    league_name TEXT,
                    match_day INTEGER,
                    my_team TEXT,
                    my_position INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    checksum TEXT,
                    UNIQUE(user_id, save_name)
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_saves 
                ON saves(user_id, timestamp DESC)
            """)
    
    def save_game(self, user_id: str, save_name: str, game_data: dict) -> bool:
        """Save game to SQLite database."""
        try:
            json_data = json.dumps(game_data)
            checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            # Extract progress info
            league_name = game_data.get("name", "")
            match_day = game_data.get("week", 0)
            my_team = game_data.get("myTeam", "")
            my_position = game_data.get("myTeamPosition", 0)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO saves 
                    (user_id, save_name, game_data, league_name, 
                     match_day, my_team, my_position, checksum)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, save_name, json_data, league_name,
                      match_day, my_team, my_position, checksum))
                
            return True
            
        except Exception as e:
            print(f"SQLite save failed: {e}")
            return False
    
    def load_game(self, user_id: str, save_name: str) -> Optional[dict]:
        """Load game from SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT game_data, checksum FROM saves
                    WHERE user_id = ? AND save_name = ?
                """, (user_id, save_name))
                
                row = cursor.fetchone()
                if not row:
                    return None
                    
                json_data, stored_checksum = row
                
                # Verify integrity
                calculated_checksum = hashlib.sha256(json_data.encode()).hexdigest()
                if stored_checksum != calculated_checksum:
                    print("Save corrupted!")
                    return None
                    
                return json.loads(json_data)
                
        except Exception as e:
            print(f"SQLite load failed: {e}")
            return None
    
    def list_saves(self, user_id: str) -> List[Dict]:
        """List all saves with metadata."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT save_name, league_name, match_day, 
                           my_team, my_position, timestamp
                    FROM saves
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                """, (user_id,))
                
                saves = []
                for row in cursor:
                    saves.append({
                        "save_name": row[0],
                        "league_name": row[1],
                        "match_day": row[2],
                        "my_team": row[3],
                        "my_position": row[4],
                        "timestamp": row[5]
                    })
                    
                return saves
                
        except Exception as e:
            print(f"SQLite list failed: {e}")
            return []


# Example usage and comparison
if __name__ == "__main__":
    print("🔧 IMPROVED SAVE SYSTEM EXAMPLES\n")
    
    # Test data
    test_game_data = {
        "name": "Premier League",
        "week": 15,
        "myTeam": "Arsenal",
        "myTeamPosition": 3,
        "teams": ["Arsenal", "Chelsea", "Liverpool"],
        "standings": [{"team": "Arsenal", "points": 35}]
    }
    
    print("1️⃣ JSON-BASED SYSTEM:")
    json_system = ImprovedSaveSystem("test_saves_json")
    
    # Save
    success = json_system.save_game("test_user", "mysave", test_game_data)
    print(f"   Save: {'✅' if success else '❌'}")
    
    # List
    saves = json_system.list_saves("test_user")
    for save in saves:
        print(f"   Found: {save['save_name']} - {save['progress_info']}")
    
    # Load
    loaded = json_system.load_game("test_user", "mysave")
    print(f"   Load: {'✅' if loaded else '❌'}")
    
    print("\n2️⃣ SQLITE-BASED SYSTEM:")
    sqlite_system = SQLiteSaveSystem("test_saves.db")
    
    # Save
    success = sqlite_system.save_game("test_user", "mysave", test_game_data)
    print(f"   Save: {'✅' if success else '❌'}")
    
    # List with metadata
    saves = sqlite_system.list_saves("test_user")
    for save in saves:
        print(f"   Found: {save['save_name']} - {save['league_name']} Day {save['match_day']}")
    
    # Load
    loaded = sqlite_system.load_game("test_user", "mysave")
    print(f"   Load: {'✅' if loaded else '❌'}")