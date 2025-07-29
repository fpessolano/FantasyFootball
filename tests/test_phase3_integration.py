#!/usr/bin/env python3
"""
Phase 3 Test: Faker Name Generator Integration
Tests that PlayerManager correctly uses InternationalNameGenerator for realistic names and nationalities.
"""

import sys
import os
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_player_manager_faker_integration():
    """Test that PlayerManager uses faker for name generation."""
    print("🎭 Testing PlayerManager faker integration...")
    
    try:
        from player_manager import PlayerManager, FAKER_AVAILABLE
        from models import Position
        
        # Verify faker is available
        assert FAKER_AVAILABLE, "Faker should be available for this test"
        print("✅ Faker availability confirmed")
        
        # Create temporary player manager
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')  # Empty player list
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Test that name generator is initialized
            assert pm.name_generator is not None, "Name generator should be initialized"
            print("✅ Name generator initialized")
            
            # Test realistic name generation helper
            name_data = pm._generate_realistic_name()
            assert 'full_name' in name_data, "Name data should contain full_name"
            assert 'nationality' in name_data, "Name data should contain nationality"
            assert name_data['nationality'] != "Unknown", "Should generate real nationality"
            assert len(name_data['full_name']) >= 2, "Should generate realistic name"
            print(f"✅ Realistic name generation: {name_data['full_name']} ({name_data['nationality']})")
            
            # Test nationality-specific generation
            german_data = pm._generate_realistic_name("German")
            assert german_data['nationality'] == "German", f"Expected German, got {german_data['nationality']}"
            print(f"✅ Nationality-specific generation: {german_data['full_name']} (German)")
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ PlayerManager faker integration test failed: {e}")
        return False

def test_random_player_creation():
    """Test that create_random_player uses realistic names."""
    print("\n🎲 Testing random player creation with realistic names...")
    
    try:
        from player_manager import PlayerManager
        from models import Position
        
        # Create temporary player manager
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Create random players
            test_players = []
            for _ in range(5):
                player = pm.create_random_player()
                test_players.append(player)
            
            print("✅ Generated random players:")
            for player in test_players:
                print(f"   {player.get_display_name()} - {player.position.name}")
                
                # Verify realistic attributes
                assert len(player.name) >= 2, f"Player name too short: '{player.name}'"
                assert player.nationality != "Unknown", f"Player should have realistic nationality: {player.nationality}"
                assert player.position in Position, f"Invalid position: {player.position}"
                assert 0 <= player.overall_rating() <= 100, f"Invalid overall rating: {player.overall_rating()}"
            
            print("✅ All generated players have realistic names and nationalities")
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Random player creation test failed: {e}")
        return False

def test_nationality_based_generation():
    """Test nationality-specific player generation methods."""
    print("\n🌍 Testing nationality-based player generation...")
    
    try:
        from player_manager import PlayerManager
        from models import Position
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Test create_player_by_nationality
            brazilian_player = pm.create_player_by_nationality(Position.ST, "Brazilian")
            assert brazilian_player.nationality == "Brazilian", f"Expected Brazilian, got {brazilian_player.nationality}"
            assert brazilian_player.position == Position.ST, f"Expected ST, got {brazilian_player.position}"
            print(f"✅ Brazilian player: {brazilian_player.get_display_name()}")
            
            # Test generate_national_team
            spanish_team = pm.generate_national_team("Spanish", 11)
            assert len(spanish_team) == 11, f"Expected 11 players, got {len(spanish_team)}"
            
            for player in spanish_team:
                assert player.nationality == "Spanish", f"Expected Spanish, got {player.nationality}"
            
            print(f"✅ Spanish national team generated:")
            for i, player in enumerate(spanish_team[:3], 1):  # Show first 3
                print(f"   {i}. {player.get_display_name()} - {player.position.name}")
            print(f"   ... and {len(spanish_team)-3} more players")
            
            # Test generate_international_squad
            international_squad = pm.generate_international_squad(15)
            assert len(international_squad) == 15, f"Expected 15 players, got {len(international_squad)}"
            
            nationalities = set(player.nationality for player in international_squad)
            assert len(nationalities) > 1, "International squad should have multiple nationalities"
            print(f"✅ International squad with {len(nationalities)} nationalities: {sorted(nationalities)}")
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Nationality-based generation test failed: {e}")
        return False

def test_nationality_search_methods():
    """Test nationality search and analysis methods."""
    print("\n🔍 Testing nationality search methods...")
    
    try:
        from player_manager import PlayerManager
        from models import Position
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Add test players with known nationalities
            test_players = [
                pm.create_player_by_nationality(Position.GK, "Brazilian"),
                pm.create_player_by_nationality(Position.CB, "Brazilian"),
                pm.create_player_by_nationality(Position.ST, "Italian"),
                pm.create_player_by_nationality(Position.CM, "French"),
                pm.create_player_by_nationality(Position.LW, "French")
            ]
            
            for player in test_players:
                pm.add_player(player)
            
            # Test find_players_by_nationality
            brazilian_players = pm.find_players_by_nationality("Brazilian")
            assert len(brazilian_players) == 2, f"Expected 2 Brazilian players, got {len(brazilian_players)}"
            
            french_players = pm.find_players_by_nationality("French")
            assert len(french_players) == 2, f"Expected 2 French players, got {len(french_players)}"
            
            italian_players = pm.find_players_by_nationality("Italian")
            assert len(italian_players) == 1, f"Expected 1 Italian player, got {len(italian_players)}"
            
            print("✅ Nationality search working correctly")
            
            # Test nationality distribution
            distribution = pm.get_nationality_distribution()
            expected_distribution = {"Brazilian": 2, "Italian": 1, "French": 2}
            assert distribution == expected_distribution, f"Expected {expected_distribution}, got {distribution}"
            print(f"✅ Nationality distribution: {distribution}")
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Nationality search methods test failed: {e}")
        return False

def test_player_pool_generation():
    """Test enhanced player pool generation with nationalities."""
    print("\n👥 Testing player pool generation...")
    
    try:
        from player_manager import PlayerManager
        from models import Position
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Test generate_player_pool with realistic names
            player_pool = pm.generate_player_pool(20, ensure_all_positions=True)
            assert len(player_pool) == 20, f"Expected 20 players, got {len(player_pool)}"
            
            # Verify all players have realistic attributes
            nationalities = set()
            positions = set()
            
            for player in player_pool:
                assert player.nationality != "Unknown", f"Player {player.name} has Unknown nationality"
                assert len(player.name) >= 2, f"Player name too short: '{player.name}'"
                assert isinstance(player.position, Position), f"Invalid position type: {type(player.position)}"
                
                nationalities.add(player.nationality)
                positions.add(player.position)
            
            print(f"✅ Generated player pool with {len(nationalities)} nationalities")
            print(f"   Nationalities: {sorted(list(nationalities)[:5])}{'...' if len(nationalities) > 5 else ''}")
            print(f"   Positions covered: {len(positions)} / {len(list(Position))}")
            
            # Test that most positions are covered
            assert len(positions) >= 10, f"Should cover most positions, only got {len(positions)}"
            
            # Test that we have international diversity
            assert len(nationalities) > 3, f"Should have diverse nationalities, only got {len(nationalities)}"
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Player pool generation test failed: {e}")
        return False

def test_fallback_without_faker():
    """Test that system works gracefully without faker."""
    print("\n🛡️ Testing fallback behavior without faker...")
    
    try:
        # This test simulates what happens when faker is not available
        # We can't easily mock the import, so we'll just test the fallback logic
        from player_manager import PlayerManager
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_file = f.name
        
        try:
            pm = PlayerManager(temp_file)
            
            # Test fallback name generation (simulate faker unavailable)
            # Temporarily set name_generator to None to test fallback
            original_generator = pm.name_generator
            pm.name_generator = None
            
            try:
                fallback_data = pm._generate_realistic_name()
                assert 'full_name' in fallback_data, "Fallback should provide full_name"
                assert 'nationality' in fallback_data, "Fallback should provide nationality"
                assert fallback_data['nationality'] == 'Unknown', "Fallback nationality should be Unknown"
                print(f"✅ Fallback name generation: {fallback_data['full_name']} ({fallback_data['nationality']})")
                
                # Test creating player with fallback
                fallback_player = pm.create_random_player()
                assert fallback_player.nationality == 'Unknown', "Fallback player should have Unknown nationality"
                print(f"✅ Fallback player creation: {fallback_player.name}")
                
            finally:
                # Restore original generator
                pm.name_generator = original_generator
            
            return True
            
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Fallback behavior test failed: {e}")
        return False

def main():
    """Run all Phase 3 tests."""
    print("🧪 Phase 3: Faker Name Generator Integration Test")
    print("=" * 60)
    
    tests = [
        ("PlayerManager Faker Integration", test_player_manager_faker_integration),
        ("Random Player Creation", test_random_player_creation),
        ("Nationality-Based Generation", test_nationality_based_generation),
        ("Nationality Search Methods", test_nationality_search_methods),
        ("Player Pool Generation", test_player_pool_generation),
        ("Fallback Without Faker", test_fallback_without_faker)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        print("-" * 45)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PHASE 3 TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 Phase 3 Complete! Faker name generator successfully integrated.")
        print("   PlayerManager now generates realistic international names and nationalities.")
        print("   Ready to proceed to Phase 4: Create Data Migration System.")
        return True
    else:
        print("\n⚠️  Phase 3 has issues. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)