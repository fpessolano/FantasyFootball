#!/usr/bin/env python3
"""
Team Regeneration Script
~~~~~~~~~~~~~~~~~~~~~~~~

Regenerates existing teams using the new migrated player pool while preserving:
- Team names, formations, tactical styles
- ELO ratings and team characteristics
- Similar team strength/balance
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import our components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from team_manager import TeamManager
from player_manager import PlayerManager
from models import Team, Player, Position, TacticalStyle, FORMATIONS

def backup_teams():
    """Create timestamped backup of existing teams."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    import shutil
    try:
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        shutil.copy(os.path.join(parent_dir, 'teams.json'), f'teams_backup_regen_{timestamp}.json')
        print(f"✅ Created team backup: teams_backup_regen_{timestamp}.json")
        return True
    except FileNotFoundError as e:
        print(f"⚠️  Backup warning: {e}")
        return False

def analyze_existing_teams():
    """Analyze existing teams to understand their characteristics."""
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(parent_dir, 'teams.json'), 'r') as f:
        teams_data = json.load(f)
    
    print(f"📊 Analyzing {len(teams_data)} existing teams...")
    
    team_info = []
    for team_data in teams_data:
        info = {
            'name': team_data['name'],
            'formation': team_data['formation'],
            'style': team_data.get('style', 'BALANCED'),
            'elo_rating': team_data.get('elo_rating', 1500),
            'team_momentum': team_data.get('team_momentum', 0),
            'streak_count': team_data.get('streak_count', 0),
            'player_count': len(team_data.get('players', []))
        }
        team_info.append(info)
        print(f"  {info['name']}: {info['formation']} ({info['style']}) - ELO: {info['elo_rating']:.0f}")
    
    return team_info

def regenerate_team_with_new_players(team_info: Dict, available_players: List[Player]) -> Optional[Team]:
    """Regenerate a single team using new players while preserving characteristics."""
    
    # Check if we have enough players for this formation
    formation = team_info['formation']
    if formation not in FORMATIONS:
        print(f"❌ Unknown formation {formation} for team {team_info['name']}")
        return None
    
    requirements = FORMATIONS[formation]
    total_needed = sum(requirements.values())
    
    if len(available_players) < total_needed:
        print(f"❌ Not enough available players for {team_info['name']} (need {total_needed}, have {len(available_players)})")
        return None
    
    # Select players for each position requirement
    selected_players = []
    temp_available = available_players.copy()
    
    print(f"  🔨 Building {team_info['name']} ({formation})...")
    
    for position, count in requirements.items():
        # Find candidates for this position
        candidates = [p for p in temp_available if p.position == position]
        
        # Add compatible positions if needed
        if len(candidates) < count:
            if position in [Position.LB, Position.RB]:
                candidates.extend([p for p in temp_available 
                                if p.position in [Position.WB, Position.LWB, Position.RWB] 
                                and p not in candidates])
            elif position in [Position.LWB, Position.RWB]:
                candidates.extend([p for p in temp_available 
                                if p.position in [Position.LB, Position.RB, Position.WB] 
                                and p not in candidates])
            elif position == Position.DM:
                candidates.extend([p for p in temp_available 
                                if p.position == Position.CM and p not in candidates])
            elif position == Position.AM:
                candidates.extend([p for p in temp_available 
                                if p.position == Position.CM and p not in candidates])
        
        if len(candidates) < count:
            print(f"    ⚠️  Only {len(candidates)} candidates for {position.name} (need {count})")
            # Try any remaining players as last resort
            candidates = temp_available[:count]
        
        # Sort by overall rating and select the best available
        candidates.sort(key=lambda p: p.overall_rating(), reverse=True)
        
        for i in range(min(count, len(candidates))):
            selected_players.append(candidates[i])
            temp_available.remove(candidates[i])
            print(f"    ✓ {position.name}: {candidates[i].name} ({candidates[i].nationality})")
    
    # Create the new team
    try:
        style = TacticalStyle[team_info['style']]
    except KeyError:
        style = TacticalStyle.BALANCED
    
    team = Team(
        name=team_info['name'],
        formation=formation,
        players=selected_players,
        style=style
    )
    
    # Restore team characteristics
    team.elo_rating = team_info['elo_rating']
    team.team_momentum = team_info['team_momentum']
    team.streak_count = team_info['streak_count']
    
    # Remove selected players from available pool
    for player in selected_players:
        if player in available_players:
            available_players.remove(player)
    
    return team

def regenerate_all_teams():
    """Main function to regenerate all teams."""
    print("🚀 Team Regeneration with New Migrated Players")
    print("=" * 60)
    
    # Create backup
    print("\n1️⃣ Creating backup...")
    backup_teams()
    
    # Analyze existing teams
    print("\n2️⃣ Analyzing existing teams...")
    team_info_list = analyze_existing_teams()
    
    # Load current player pool
    print("\n3️⃣ Loading migrated player pool...")
    pm = PlayerManager()
    available_players = pm.players.copy()
    print(f"✅ Loaded {len(available_players)} migrated players")
    
    # Show sample of new players
    print("📋 Sample migrated players:")
    for player in available_players[:5]:
        print(f"   {player.name} ({player.nationality}) - {player.position.name}")
    
    # Regenerate each team
    print(f"\n4️⃣ Regenerating {len(team_info_list)} teams...")
    new_teams = []
    
    for i, team_info in enumerate(team_info_list, 1):
        print(f"\n[{i}/{len(team_info_list)}] Regenerating {team_info['name']}...")
        
        new_team = regenerate_team_with_new_players(team_info, available_players)
        if new_team:
            new_teams.append(new_team)
            print(f"✅ Successfully regenerated {new_team.name}")
            print(f"   Players: {len(new_team.players)}, Available remaining: {len(available_players)}")
        else:
            print(f"❌ Failed to regenerate {team_info['name']}")
    
    # Save new teams
    print(f"\n5️⃣ Saving regenerated teams...")
    if new_teams:
        # Save to teams.json
        teams_data = [team.to_dict() for team in new_teams]
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(parent_dir, 'teams.json'), 'w') as f:
            json.dump(teams_data, f, indent=2)
        
        print(f"✅ Saved {len(new_teams)} regenerated teams")
        
        # Verify no duplicate players
        print("\n6️⃣ Verifying no duplicate players...")
        all_player_names = []
        for team in new_teams:
            for player in team.players:
                all_player_names.append(player.name)
        
        unique_names = set(all_player_names)
        if len(all_player_names) == len(unique_names):
            print(f"✅ No duplicates found! {len(all_player_names)} unique players across all teams")
        else:
            duplicates = len(all_player_names) - len(unique_names)
            print(f"❌ Found {duplicates} duplicate players!")
        
        # Summary
        print(f"\n🎉 Team Regeneration Complete!")
        print(f"   • {len(new_teams)} teams regenerated with new players")
        print(f"   • {len(all_player_names)} total players assigned")
        print(f"   • {len(available_players)} players remaining in pool")
        print(f"   • Original team characteristics preserved")
        
        return True
    else:
        print("❌ No teams were successfully regenerated!")
        return False

if __name__ == "__main__":
    success = regenerate_all_teams()
    exit(0 if success else 1)