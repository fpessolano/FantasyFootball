#!/usr/bin/env python3
"""
Data Migration Script
~~~~~~~~~~~~~~~~~~~

Migrates existing players and teams to use realistic names and nationalities.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any

# Import our components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from name_generator import InternationalNameGenerator
from models import Player, Team, Position, TacticalStyle, TemperamentType

def backup_files():
    """Create timestamped backups of existing data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    import shutil
    try:
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        shutil.copy(os.path.join(parent_dir, 'players.json'), f'players_backup_{timestamp}.json')
        shutil.copy(os.path.join(parent_dir, 'teams.json'), f'teams_backup_{timestamp}.json')
        print(f"✅ Created backups with timestamp {timestamp}")
        return True
    except FileNotFoundError as e:
        print(f"⚠️  Backup warning: {e}")
        return False

def load_existing_data():
    """Load existing players and teams data."""
    players_data = []
    teams_data = []
    
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    
    try:
        with open(os.path.join(parent_dir, 'players.json'), 'r') as f:
            players_data = json.load(f)
        print(f"✅ Loaded {len(players_data)} existing players")
    except FileNotFoundError:
        print("ℹ️  No existing players.json found")
    
    try:
        with open(os.path.join(parent_dir, 'teams.json'), 'r') as f:
            teams_data = json.load(f)
        print(f"✅ Loaded {len(teams_data)} existing teams")
    except FileNotFoundError:
        print("ℹ️  No existing teams.json found")
    
    return players_data, teams_data

def migrate_players(players_data: List[Dict[str, Any]], name_generator: InternationalNameGenerator) -> List[Dict[str, Any]]:
    """Migrate players to have realistic names and nationalities."""
    print(f"\n🧑‍⚽ Migrating {len(players_data)} players...")
    
    migrated_players = []
    name_count = {}  # Track name usage to avoid duplicates
    
    for i, player_data in enumerate(players_data):
        # Generate unique realistic male name (for football players)
        attempts = 0
        while attempts < 10:  # Max 10 attempts to find unique name
            name_data = name_generator.generate_male_name(random.choice(list(name_generator.popular_locales.keys())))
            full_name = name_data['full_name']
            nationality = name_data['nationality']
            
            if full_name not in name_count:
                name_count[full_name] = 1
                break
            attempts += 1
        else:
            # If we can't find unique name, append number
            base_name = name_data['full_name']
            counter = name_count.get(base_name, 0) + 1
            full_name = f"{base_name} {counter}"
            nationality = name_data['nationality']
            name_count[base_name] = counter
        
        # Update player data with new name and nationality
        updated_player = player_data.copy()
        old_name = updated_player.get('name', 'Unknown')
        updated_player['name'] = full_name
        updated_player['nationality'] = nationality
        
        # Ensure all required fields exist (for legacy compatibility)
        defaults = {
            'natural_fitness': 70,
            'work_rate': 50,
            'injury_proneness': 30,
            'pressure_handling': 60,
            'concentration': 60,
            'determination': 60,
            'composure': 60,
            'leadership': 30,
            'temperament': 'consistent',
            'preferred_foot': 'right',
            'age': 25,
            'current_stamina': 100.0,
            'form_base': 7.0,
            'form_confidence': 50.0
        }
        
        for key, default_value in defaults.items():
            if key not in updated_player:
                updated_player[key] = default_value
        
        migrated_players.append(updated_player)
        
        if (i + 1) % 10 == 0 or i == len(players_data) - 1:
            print(f"   Migrated {i + 1}/{len(players_data)} players")
    
    print(f"✅ Player migration complete!")
    print(f"   Sample migrations:")
    for player in migrated_players[:3]:
        print(f"   → {player['name']} ({player['nationality']}) - {player['position']}")
    
    return migrated_players

def migrate_teams(teams_data: List[Dict[str, Any]], name_generator: InternationalNameGenerator) -> List[Dict[str, Any]]:
    """Migrate teams to have realistic player names and nationalities."""
    print(f"\n🏟️ Migrating {len(teams_data)} teams...")
    
    migrated_teams = []
    
    for i, team_data in enumerate(teams_data):
        updated_team = team_data.copy()
        
        # Migrate players within each team
        if 'players' in updated_team:
            team_players = updated_team['players']
            name_count = {}  # Track names within this team
            
            for j, player_data in enumerate(team_players):
                # Generate unique realistic male name for this team (for football players)
                attempts = 0
                while attempts < 10:
                    name_data = name_generator.generate_male_name(random.choice(list(name_generator.popular_locales.keys())))
                    full_name = name_data['full_name']
                    nationality = name_data['nationality']
                    
                    if full_name not in name_count:
                        name_count[full_name] = 1
                        break
                    attempts += 1
                else:
                    # Fallback with counter
                    base_name = name_data['full_name']
                    counter = name_count.get(base_name, 0) + 1
                    full_name = f"{base_name} {counter}"
                    nationality = name_data['nationality']
                    name_count[base_name] = counter
                
                # Update player data
                old_name = player_data.get('name', 'Unknown')
                player_data['name'] = full_name
                player_data['nationality'] = nationality
                
                # Add missing fields for legacy compatibility
                defaults = {
                    'natural_fitness': 70,
                    'work_rate': 50,
                    'injury_proneness': 30,
                    'pressure_handling': 60,
                    'concentration': 60,
                    'determination': 60,
                    'composure': 60,
                    'leadership': 30,
                    'temperament': 'consistent',
                    'preferred_foot': 'right',
                    'age': 25,
                    'current_stamina': 100.0,
                    'form_base': 7.0,
                    'form_confidence': 50.0
                }
                
                for key, default_value in defaults.items():
                    if key not in player_data:
                        player_data[key] = default_value
        
        migrated_teams.append(updated_team)
        print(f"   Migrated team: {updated_team['name']} ({len(updated_team.get('players', []))} players)")
    
    print(f"✅ Team migration complete!")
    return migrated_teams

def save_migrated_data(players_data: List[Dict[str, Any]], teams_data: List[Dict[str, Any]]):
    """Save migrated data back to files."""
    print(f"\n💾 Saving migrated data...")
    
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    
    with open(os.path.join(parent_dir, 'players.json'), 'w') as f:
        json.dump(players_data, f, indent=2)
    print(f"✅ Saved {len(players_data)} players to players.json")
    
    with open(os.path.join(parent_dir, 'teams.json'), 'w') as f:
        json.dump(teams_data, f, indent=2)
    print(f"✅ Saved {len(teams_data)} teams to teams.json")

def verify_migration():
    """Quick verification that migration worked correctly."""
    print(f"\n🔍 Verifying migration...")
    
    try:
        # Test loading with PlayerManager
        from player_manager import PlayerManager
        from team_manager import TeamManager
        
        pm = PlayerManager()
        tm = TeamManager()
        
        print(f"✅ PlayerManager loaded {len(pm.players)} players successfully")
        print(f"✅ TeamManager loaded {len(tm.teams)} teams successfully")
        
        # Check nationality distribution
        if pm.players:
            nationalities = set(p.nationality for p in pm.players)
            print(f"✅ Found {len(nationalities)} different nationalities")
            
            # Show sample of realistic names
            print(f"📋 Sample migrated players:")
            for player in pm.players[:5]:
                print(f"   {player.get_display_name()} - {player.position.name}")
        
        if tm.teams:
            print(f"📋 Sample migrated teams:")
            for team in tm.teams[:3]:
                if team.players:
                    sample_player = team.players[0]
                    print(f"   {team.name}: {sample_player.get_display_name()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main migration function."""
    print("🚀 Fantasy Football Data Migration")
    print("=" * 50)
    print("This will update existing players and teams with realistic names and nationalities.")
    
    # Initialize name generator with Latin alphabet only
    try:
        name_generator = InternationalNameGenerator(seed=42)  # Fixed seed for reproducible results
        name_generator.use_latin_alphabet_only(True)  # Use only Latin alphabet names
        print("✅ Name generator initialized (Latin alphabet only)")
    except Exception as e:
        print(f"❌ Failed to initialize name generator: {e}")
        print("Make sure faker is installed: pip install faker")
        return False
    
    # Create backups
    print(f"\n1️⃣ Creating backups...")
    backup_files()
    
    # Load existing data
    print(f"\n2️⃣ Loading existing data...")
    players_data, teams_data = load_existing_data()
    
    if not players_data and not teams_data:
        print("ℹ️  No existing data to migrate.")
        return True
    
    # Migrate players
    if players_data:
        print(f"\n3️⃣ Migrating players...")
        migrated_players = migrate_players(players_data, name_generator)
    else:
        migrated_players = []
    
    # Migrate teams
    if teams_data:
        print(f"\n4️⃣ Migrating teams...")
        migrated_teams = migrate_teams(teams_data, name_generator)
    else:
        migrated_teams = []
    
    # Save migrated data
    print(f"\n5️⃣ Saving migrated data...")
    save_migrated_data(migrated_players, migrated_teams)
    
    # Verify migration
    print(f"\n6️⃣ Verifying migration...")
    if verify_migration():
        print(f"\n🎉 Migration completed successfully!")
        print(f"   • {len(migrated_players)} players updated")
        print(f"   • {len(migrated_teams)} teams updated")
        print(f"   • All players now have realistic names and nationalities")
        print(f"   • Original data backed up")
        return True
    else:
        print(f"\n⚠️  Migration completed but verification failed.")
        print(f"   Check the data manually or restore from backup if needed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)