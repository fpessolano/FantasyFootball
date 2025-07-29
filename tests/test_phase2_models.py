#!/usr/bin/env python3
"""
Phase 2 Test: Enhanced Data Models
Tests that Player and Team models correctly handle nationality information.
"""

import sys
import os
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_player_nationality_field():
    """Test that Player class has nationality field."""
    print("🧑‍⚽ Testing Player nationality field...")
    
    try:
        from models import Player, Position, TemperamentType
        
        # Test creating player with nationality
        player = Player(
            name="João Silva",
            position=Position.ST,
            nationality="Brazilian",
            goalkeeping=20,
            defending=30,
            passing=70,
            dribbling=85,
            shooting=90,
            physical=80
        )
        
        assert player.nationality == "Brazilian", f"Expected 'Brazilian', got '{player.nationality}'"
        print("✅ Player nationality field working")
        
        # Test default nationality
        player_default = Player(
            name="Test Player",
            position=Position.GK,
            goalkeeping=80,
            defending=40,
            passing=60,
            dribbling=30,
            shooting=20,
            physical=70
        )
        
        assert player_default.nationality == "Unknown", f"Expected 'Unknown', got '{player_default.nationality}'"
        print("✅ Default nationality working")
        
        return True
        
    except Exception as e:
        print(f"❌ Player nationality field test failed: {e}")
        return False

def test_player_serialization():
    """Test Player serialization/deserialization with nationality."""
    print("\n💾 Testing Player serialization with nationality...")
    
    try:
        from models import Player, Position, TemperamentType
        
        # Create test player
        original_player = Player(
            name="Marco Rossi",
            position=Position.CM,
            nationality="Italian",
            goalkeeping=25,
            defending=75,
            passing=85,
            dribbling=70,
            shooting=65,
            physical=80,
            age=28,
            temperament=TemperamentType.CONSISTENT
        )
        
        # Test serialization
        player_dict = original_player.to_dict()
        assert "nationality" in player_dict, "nationality missing from serialized data"
        assert player_dict["nationality"] == "Italian", f"Expected 'Italian', got '{player_dict['nationality']}'"
        print("✅ Player serialization includes nationality")
        
        # Test deserialization
        restored_player = Player.from_dict(player_dict)
        assert restored_player.nationality == "Italian", f"Expected 'Italian', got '{restored_player.nationality}'"
        assert restored_player.name == "Marco Rossi", f"Expected 'Marco Rossi', got '{restored_player.name}'"
        print("✅ Player deserialization preserves nationality")
        
        # Test legacy data handling (without nationality)
        legacy_data = {
            "name": "Legacy Player",
            "position": "ST",
            "goalkeeping": 20,
            "defending": 30,
            "passing": 60,
            "dribbling": 70,
            "shooting": 85,
            "physical": 75
        }
        
        legacy_player = Player.from_dict(legacy_data)
        assert legacy_player.nationality == "Unknown", f"Expected 'Unknown', got '{legacy_player.nationality}'"
        print("✅ Legacy data handling working (defaults to 'Unknown')")
        
        return True
        
    except Exception as e:
        print(f"❌ Player serialization test failed: {e}")
        return False

def test_player_display_methods():
    """Test Player display methods with nationality."""
    print("\n🎭 Testing Player display methods...")
    
    try:
        from models import Player, Position
        
        # Test player with nationality
        player_with_nationality = Player(
            name="Pierre Dubois",
            position=Position.LW,
            nationality="French",
            goalkeeping=15,
            defending=40,
            passing=75,
            dribbling=90,
            shooting=80,
            physical=70
        )
        
        # Test display name
        display_name = player_with_nationality.get_display_name()
        expected = "Pierre Dubois (French)"
        assert display_name == expected, f"Expected '{expected}', got '{display_name}'"
        print("✅ Player display name with nationality working")
        
        # Test nationality flag
        nationality_flag = player_with_nationality.get_nationality_flag()
        assert "🇫🇷" in nationality_flag, f"Expected French flag in '{nationality_flag}'"
        assert "French" in nationality_flag, f"Expected 'French' in '{nationality_flag}'"
        print("✅ Player nationality flag working")
        
        # Test string representation
        str_repr = str(player_with_nationality)
        assert "Pierre Dubois (French)" in str_repr, f"Expected nationality in string representation: '{str_repr}'"
        assert "LW" in str_repr, f"Expected position in string representation: '{str_repr}'"
        print("✅ Player string representation working")
        
        # Test player without nationality
        player_unknown = Player(
            name="Unknown Player",
            position=Position.CB,
            nationality="Unknown",
            goalkeeping=25,
            defending=85,
            passing=60,
            dribbling=40,
            shooting=25,
            physical=80
        )
        
        display_name_unknown = player_unknown.get_display_name()
        assert display_name_unknown == "Unknown Player", f"Expected 'Unknown Player', got '{display_name_unknown}'"
        print("✅ Player display for unknown nationality working")
        
        return True
        
    except Exception as e:
        print(f"❌ Player display methods test failed: {e}")
        return False

def test_team_nationality_methods():
    """Test Team nationality analysis methods."""
    print("\n🏟️ Testing Team nationality methods...")
    
    try:
        from models import Player, Team, Position, TacticalStyle
        
        # Create players with different nationalities
        players = [
            Player("João Silva", Position.GK, 90, 20, 40, 30, 20, 75, "Brazilian"),
            Player("Marco Rossi", Position.CB, 20, 85, 60, 40, 30, 80, "Italian"),
            Player("Pierre Dubois", Position.CB, 25, 80, 65, 45, 35, 78, "French"),
            Player("Hans Mueller", Position.CM, 30, 60, 85, 70, 65, 75, "German"),
            Player("Carlos Rodriguez", Position.CM, 25, 55, 80, 75, 70, 70, "Spanish"),
            Player("Sergio Santos", Position.AM, 20, 40, 75, 85, 80, 65, "Brazilian"),
            Player("Giuseppe Bianchi", Position.LW, 15, 35, 70, 90, 85, 60, "Italian"),
            Player("Antoine Leroy", Position.RW, 20, 30, 65, 88, 82, 62, "French"),
            Player("Luis Fernandez", Position.ST, 18, 25, 60, 75, 92, 70, "Spanish"),
            Player("Dieter Schmidt", Position.ST, 22, 30, 55, 70, 88, 75, "German"),
            Player("Andrea Conti", Position.LB, 25, 75, 70, 60, 40, 72, "Italian")
        ]
        
        team = Team(
            name="International FC",
            formation="4-3-3",
            players=players,
            style=TacticalStyle.ATTACKING
        )
        
        # Test nationality distribution
        distribution = team.get_nationality_distribution()
        expected_distribution = {"Brazilian": 2, "Italian": 3, "French": 2, "German": 2, "Spanish": 2}
        assert distribution == expected_distribution, f"Expected {expected_distribution}, got {distribution}"
        print("✅ Team nationality distribution working")
        
        # Test most common nationality
        most_common = team.get_most_common_nationality()
        assert most_common == "Italian", f"Expected 'Italian', got '{most_common}'"
        print("✅ Team most common nationality working")
        
        # Test international team check
        is_international = team.is_international_team()
        assert is_international == True, f"Expected True, got {is_international}"
        print("✅ Team international check working")
        
        # Test international summary
        summary = team.get_international_summary()
        assert "International team" in summary, f"Expected 'International team' in summary: '{summary}'"
        assert "Italian: 3" in summary, f"Expected 'Italian: 3' in summary: '{summary}'"
        print("✅ Team international summary working")
        
        # Test domestic team
        domestic_players = [
            Player("Player 1", Position.GK, 80, 20, 40, 30, 20, 75, "German"),
            Player("Player 2", Position.CB, 20, 85, 60, 40, 30, 80, "German"),
            Player("Player 3", Position.ST, 18, 25, 60, 75, 92, 70, "German")
        ]
        
        domestic_team = Team(
            name="German FC",
            formation="4-4-2",
            players=domestic_players
        )
        
        domestic_summary = domestic_team.get_international_summary()
        assert "Domestic team (German)" in domestic_summary, f"Expected domestic team summary, got: '{domestic_summary}'"
        print("✅ Team domestic summary working")
        
        return True
        
    except Exception as e:
        print(f"❌ Team nationality methods test failed: {e}")
        return False

def test_integration_with_faker():
    """Test integration between models and name generator."""
    print("\n🔗 Testing integration with name generator...")
    
    try:
        from models import Player, Position
        from name_generator import InternationalNameGenerator
        
        generator = InternationalNameGenerator(seed=789)
        
        # Generate players using faker
        test_players = []
        locales_to_test = ['pt_BR', 'it_IT', 'fr_FR', 'de_DE', 'es_ES']
        
        for i, locale in enumerate(locales_to_test):
            name_data = generator.generate_name(locale)
            player = Player(
                name=name_data['full_name'],
                position=list(Position)[i % len(Position)],
                nationality=name_data['nationality'],
                goalkeeping=50 + i * 5,
                defending=60 + i * 2,
                passing=70 + i,
                dribbling=65 + i * 2,
                shooting=55 + i * 3,
                physical=75 + i
            )
            test_players.append(player)
        
        print("✅ Created players from faker data:")
        for player in test_players:
            print(f"   {player.get_display_name()} - {player.position.name}")
        
        # Test that all have realistic nationalities
        for player in test_players:
            assert player.nationality != "Unknown", f"Player {player.name} has Unknown nationality"
            assert len(player.nationality) > 2, f"Player {player.name} has invalid nationality: '{player.nationality}'"
        
        print("✅ All generated players have valid nationalities")
        
        # Test serialization round-trip with faker data
        for player in test_players:
            serialized = player.to_dict()
            restored = Player.from_dict(serialized)
            assert restored.nationality == player.nationality, f"Nationality lost in serialization for {player.name}"
        
        print("✅ Faker-generated players serialize correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration with faker test failed: {e}")
        return False

def main():
    """Run all Phase 2 tests."""
    print("🧪 Phase 2: Enhanced Data Models Test")
    print("=" * 50)
    
    tests = [
        ("Player Nationality Field", test_player_nationality_field),
        ("Player Serialization", test_player_serialization),
        ("Player Display Methods", test_player_display_methods),
        ("Team Nationality Methods", test_team_nationality_methods),
        ("Integration with Faker", test_integration_with_faker)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PHASE 2 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 Phase 2 Complete! Data models enhanced with nationality support.")
        print("   Ready to proceed to Phase 3: Integrate Faker Name Generator.")
        return True
    else:
        print("\n⚠️  Phase 2 has issues. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)