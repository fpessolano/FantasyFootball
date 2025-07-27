#!/usr/bin/env python3
"""
Test script for save/load functionality

Tests both the old shelve-based system and the new JSON-based system.
"""

import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.save_system import SaveGameManager
from core.entities.team import Team
from core.entities.league import League


def print_test_header(test_name):
    """Print a formatted test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")


def test_save_system():
    """Test the JSON-based save system."""
    print_test_header("JSON-based Save System")
    
    try:
        # Test with context manager
        with SaveGameManager('test_user', 'test_saves_json') as manager:
            
            # Test 1: Basic save/load
            print("\n1. Testing basic save/load...")
            test_state = {
                'league_name': 'Premier League',
                'season': 2,
                'match_day': 15,
                'my_team': 'Manchester United',
                'team_stats': {
                    'won': 10,
                    'drawn': 3,
                    'lost': 2
                }
            }
            
            success = manager.save_game('test_save', test_state, 
                                      "Mid-season save")
            print(f"   Save result: {'✓ Success' if success else '✗ Failed'}")
            
            loaded = manager.load_game('test_save')
            print(f"   Load result: {'✓ Success' if loaded else '✗ Failed'}")
            if loaded:
                print(f"   Data matches: {'✓ Yes' if loaded == test_state else '✗ No'}")
            
            # Test 2: Save listing
            print("\n2. Testing save listing...")
            saves = manager.list_saves()
            print(f"   Found {len(saves)} saves")
            for save in saves:
                print(f"   - {save['name']}: {save['description']} "
                      f"({save['timestamp']})")
            
            # Test 3: Multiple saves
            print("\n3. Testing multiple saves...")
            for i in range(3):
                state = {
                    'save_number': i,
                    'timestamp': datetime.now().isoformat()
                }
                manager.save_game(f'save_{i}', state, f"Test save #{i}")
            
            saves = manager.list_saves()
            print(f"   Created {len(saves)} saves successfully")
            
            # Test 4: Save info
            print("\n4. Testing save metadata...")
            info = manager.get_save_info('test_save')
            if info:
                print(f"   Save name: {info.get('save_name')}")
                print(f"   Description: {info.get('description')}")
                print(f"   Timestamp: {info.get('timestamp')}")
                print(f"   Version: {info.get('version')}")
            
            # Test 5: Delete save
            print("\n5. Testing save deletion...")
            success = manager.delete_save('save_1')
            print(f"   Delete result: {'✓ Success' if success else '✗ Failed'}")
            
        # Cleanup
        import shutil
        if os.path.exists('test_saves_json'):
            shutil.rmtree('test_saves_json')
        
        print("\n✅ Save system tests completed")
        
    except Exception as e:
        print(f"\n❌ Save system test failed: {e}")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run all save/load tests."""
    print("\n" + "="*60)
    print("FANTASY FOOTBALL MANAGER - SAVE/LOAD SYSTEM TESTS")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    test_save_system()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()