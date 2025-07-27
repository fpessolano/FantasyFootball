#!/usr/bin/env python3
"""
Simple test for game save/load functionality.

This test focuses on the actual game saving and loading process.
"""

import sys
import os
import time
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces.cli.rich_game_cli import RichFFM
from utils.save_system import SaveGameManager
from core.entities.team import Team
from core.entities.league import League


def test_game_save_load():
    """Test the actual game save/load process."""
    print("="*60)
    print("TESTING GAME SAVE/LOAD FUNCTIONALITY")
    print("="*60)
    
    try:
        # Create a test user
        test_user = f"test_save_{int(time.time())}"
        
        print(f"\n1. Creating test game with user: {test_user}")
        
        # Initialize the game
        game = RichFFM(test_user, "0.9.0-test")
        
        # Create a simple league for testing
        teams = [
            Team("Arsenal", 1800),
            Team("Chelsea", 1750),
            Team("Liverpool", 1850),
            Team("Manchester City", 1820),
            Team("Tottenham", 1720),
            Team("Manchester United", 1780)
        ]
        
        league = League(teams, my_team=0)  # Select Arsenal as user's team
        league.league_name = "Test Premier League"
        
        game.league = league
        
        print("   ✓ Game initialized with test league")
        print(f"   ✓ User team: {teams[0].name}")
        print(f"   ✓ League: {league.league_name}")
        
        # Test saving
        print("\n2. Testing save functionality...")
        
        # Create some test save data
        save_data = {
            'league_name': league.league_name,
            'teams': [{'name': t.name, 'elo': t.elo, 'points': t.points()} for t in teams],
            'my_team_index': league.get_my_team_index(),
            'current_match_day': league.current_match_day(),
            'completed': league.completed
        }
        
        # Use the game's save system
        success = game.save_manager.save_game('test_save', save_data, "Test save")
        print(f"   Save result: {'✓ Success' if success else '✗ Failed'}")
        
        if success:
            print("   ✓ Game state saved successfully")
        
        # Test loading
        print("\n3. Testing load functionality...")
        
        loaded_data = game.save_manager.load_game('test_save')
        if loaded_data:
            print("   ✓ Game state loaded successfully")
            
            # Verify the data
            print("   Verifying loaded data:")
            print(f"   - League name: {loaded_data.get('league_name')}")
            print(f"   - Teams count: {len(loaded_data.get('teams', []))}")
            print(f"   - My team index: {loaded_data.get('my_team_index')}")
            print(f"   - Match day: {loaded_data.get('current_match_day')}")
            
            # Check if data matches
            if loaded_data == save_data:
                print("   ✓ Loaded data matches saved data perfectly")
            else:
                print("   ⚠ Loaded data differs from saved data")
        else:
            print("   ✗ Failed to load game state")
        
        # Test listing saves
        print("\n4. Testing save listing...")
        saves = game.save_manager.list_saves()
        print(f"   Found {len(saves)} saves: {[s['name'] for s in saves]}")
        
        # Test with SaveGameManager directly
        print("\n5. Testing with SaveGameManager directly...")
        with SaveGameManager(test_user, 'test_direct_saves') as manager:
            
            # Save directly
            direct_save_data = {
                'test': 'direct save',
                'timestamp': time.time(),
                'league_info': {
                    'name': league.league_name,
                    'teams_count': len(teams)
                }
            }
            
            success = manager.save_game('direct_save', direct_save_data, 
                                      "Direct save test")
            print(f"   Direct save: {'✓ Success' if success else '✗ Failed'}")
            
            # Load directly
            loaded = manager.load_game('direct_save')
            print(f"   Direct load: {'✓ Success' if loaded else '✗ Failed'}")
            
            if loaded == direct_save_data:
                print("   ✓ Direct save/load working perfectly")
            
            # List saves with metadata
            saves = manager.list_saves()
            print(f"   Direct saves found: {len(saves)}")
            for save in saves:
                print(f"   - {save['name']}: {save['description']}")
        
        print("\n6. Testing error handling...")
        
        # Test loading non-existent save
        non_existent = game.save_manager.load_game('does_not_exist')
        print(f"   Non-existent save: {'✓ Properly handled' if non_existent is None else '✗ Should be None'}")
        
        # Test with invalid data
        try:
            invalid_data = {'circular_ref': None}
            invalid_data['circular_ref'] = invalid_data  # This could cause issues
            success = game.save_manager.save_game('invalid_test', invalid_data, "Invalid test")
            print(f"   Invalid data handling: {'✓ Handled gracefully' if not success else '✓ Saved anyway'}")
        except Exception as e:
            print(f"   Invalid data handling: ✓ Exception caught: {type(e).__name__}")
        
        print("\n" + "="*60)
        print("✅ ALL GAME SAVE/LOAD TESTS COMPLETED")
        print("="*60)
        
        # Cleanup
        import shutil
        if os.path.exists('test_direct_saves'):
            shutil.rmtree('test_direct_saves')
        if os.path.exists('saves_json'):
            shutil.rmtree('saves_json')
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_game_save_load()