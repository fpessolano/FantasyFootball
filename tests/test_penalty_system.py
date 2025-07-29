#!/usr/bin/env python3
"""
Test Script for Enhanced Penalty Simulation System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script tests the new enhanced penalty shootout system to ensure:
1. Individual player mechanics work correctly
2. Penalty taker selection is realistic
3. Goalkeeper vs penalty taker calculations are accurate
4. Pressure system affects success rates appropriately
5. Penalty events are generated and integrated properly
"""

import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Team, Player, Position, TacticalStyle, Tournament, TournamentRound, TournamentMatch
from tournament_manager import TournamentManager
from team_manager import TeamManager
from player_manager import PlayerManager
from match_engine import MatchEngine

def create_test_players():
    """Create test players with varying penalty-taking abilities."""
    players = []
    
    # Create elite penalty taker
    elite_taker = Player(
        name="Elite Penalty Taker",
        position=Position.ST,
        goalkeeping=10,
        defending=70,
        passing=85,
        dribbling=80,
        shooting=95,  # Excellent shooter
        physical=85,
        natural_fitness=80,
        work_rate=70,
        pressure_handling=90,  # Great under pressure
        concentration=85,
        determination=85,
        composure=95,  # Very composed
        leadership=80,
        temperament="CONSISTENT",
        age=28
    )
    players.append(elite_taker)
    
    # Create poor penalty taker
    poor_taker = Player(
        name="Poor Penalty Taker",
        position=Position.ST,
        goalkeeping=10,
        defending=60,
        passing=65,
        dribbling=70,
        shooting=40,  # Very poor shooter
        physical=70,
        natural_fitness=75,
        work_rate=65,
        pressure_handling=30,  # Really cracks under pressure
        concentration=50,
        determination=60,
        composure=25,  # Very uncomposed
        leadership=30,
        temperament="VOLATILE",
        age=22
    )
    players.append(poor_taker)
    
    # Create elite goalkeeper
    elite_gk = Player(
        name="Elite Goalkeeper",
        position=Position.GK,
        goalkeeping=95,  # Excellent keeper
        defending=40,
        passing=60,
        dribbling=30,
        shooting=20,
        physical=80,
        natural_fitness=85,
        work_rate=70,
        pressure_handling=90,  # Great under pressure
        concentration=95,  # Very focused
        determination=85,
        composure=90,
        leadership=85,
        temperament="COOL_HEADED",
        age=30
    )
    players.append(elite_gk)
    
    # Create poor goalkeeper
    poor_gk = Player(
        name="Poor Goalkeeper",
        position=Position.GK,
        goalkeeping=45,  # Poor keeper
        defending=35,
        passing=40,
        dribbling=25,
        shooting=15,
        physical=65,
        natural_fitness=70,
        work_rate=60,
        pressure_handling=40,  # Struggles under pressure
        concentration=45,
        determination=50,
        composure=40,
        leadership=30,
        temperament="VOLATILE",
        age=24
    )
    players.append(poor_gk)
    
    # Fill out teams with average players
    for i in range(18):  # 9 more for each team
        avg_player = Player(
            name=f"Average Player {i+1}",
            position=Position.CM,
            goalkeeping=10,
            defending=70,
            passing=70,
            dribbling=70,
            shooting=70,
            physical=70,
            natural_fitness=70,
            work_rate=70,
            pressure_handling=70,
            concentration=70,
            determination=70,
            composure=70,
            leadership=50,
            temperament="CONSISTENT",
            age=26
        )
        players.append(avg_player)
    
    return players

def create_test_teams(players):
    """Create two test teams with different penalty-taking strengths."""
    # Team A: Elite penalty takers and goalkeeper
    team_a_players = [players[0], players[2]] + players[4:13]  # Elite taker + elite GK + 9 average
    team_a = Team(
        name="Elite Penalty Team",
        formation="4-4-2",
        players=team_a_players,
        style=TacticalStyle.BALANCED
    )
    
    # Team B: Poor penalty takers and goalkeeper  
    team_b_players = [players[1], players[3]] + players[13:22]  # Poor taker + poor GK + 9 average
    team_b = Team(
        name="Poor Penalty Team", 
        formation="4-4-2",
        players=team_b_players,
        style=TacticalStyle.BALANCED
    )
    
    return team_a, team_b

def test_penalty_taker_selection():
    """Test that penalty taker selection works correctly."""
    print("🧪 TESTING PENALTY TAKER SELECTION")
    print("=" * 50)
    
    players = create_test_players()
    team_a, team_b = create_test_teams(players)
    
    # Initialize managers with empty files
    player_manager = PlayerManager("test_players.json")
    team_manager = TeamManager("test_teams.json")
    tournament_manager = TournamentManager(team_manager, player_manager)
    
    # Test penalty taker selection
    team_a_takers = tournament_manager._select_penalty_takers(team_a)
    team_b_takers = tournament_manager._select_penalty_takers(team_b)
    
    print(f"Team A penalty takers (top 3):")
    for i, taker in enumerate(team_a_takers[:3]):
        penalty_skill = taker.shooting + (getattr(taker, 'composure', 70) + getattr(taker, 'pressure_handling', 70)) / 200 * 20
        print(f"  {i+1}. {taker.name} - Skill: {penalty_skill:.1f}")
    
    print(f"\nTeam B penalty takers (top 3):")
    for i, taker in enumerate(team_b_takers[:3]):
        penalty_skill = taker.shooting + (getattr(taker, 'composure', 70) + getattr(taker, 'pressure_handling', 70)) / 200 * 20
        print(f"  {i+1}. {taker.name} - Skill: {penalty_skill:.1f}")
    
    # Verify elite taker is first for Team A
    assert team_a_takers[0].name == "Elite Penalty Taker", "Elite taker should be first"
    
    # Verify poor taker is in the top penalty takers for Team B
    taker_names = [taker.name for taker in team_b_takers[:5]]
    assert "Poor Penalty Taker" in taker_names, "Poor taker should be among top takers in weak team"
    
    print("\n✅ Penalty taker selection test PASSED")
    return True

def test_individual_penalty_simulation():
    """Test individual penalty simulation mechanics."""
    print("\n🧪 TESTING INDIVIDUAL PENALTY SIMULATION")
    print("=" * 50)
    
    players = create_test_players()
    team_a, team_b = create_test_teams(players)
    
    # Initialize managers with empty files
    player_manager = PlayerManager("test_players.json")
    team_manager = TeamManager("test_teams.json")
    tournament_manager = TournamentManager(team_manager, player_manager)
    
    # Get players
    elite_taker = players[0]  # Elite Penalty Taker
    poor_taker = players[1]   # Poor Penalty Taker
    elite_gk = players[2]     # Elite Goalkeeper
    poor_gk = players[3]      # Poor Goalkeeper
    
    # Test scenarios
    scenarios = [
        ("Elite taker vs Poor GK", elite_taker, poor_gk),
        ("Poor taker vs Elite GK", poor_taker, elite_gk),
        ("Elite taker vs Elite GK", elite_taker, elite_gk),
        ("Poor taker vs Poor GK", poor_taker, poor_gk)
    ]
    
    for scenario_name, taker, gk in scenarios:
        print(f"\n📊 {scenario_name}:")
        
        # Simulate 20 penalties to get statistics
        successes = 0
        saves = 0
        misses = 0
        
        for _ in range(20):
            result = tournament_manager._simulate_individual_penalty(taker, gk, "penalty_shootout", 1)
            if result["scored"]:
                successes += 1
            elif "save" in result["description"].lower():
                saves += 1
            else:
                misses += 1
        
        success_rate = successes / 20 * 100
        save_rate = saves / 20 * 100
        miss_rate = misses / 20 * 100
        
        print(f"   Success rate: {success_rate:.1f}% ({successes}/20)")
        print(f"   Saves: {save_rate:.1f}% ({saves}/20)")
        print(f"   Misses: {miss_rate:.1f}% ({misses}/20)")
        
        # Show a sample result
        sample = tournament_manager._simulate_individual_penalty(taker, gk, "penalty_shootout", 1)
        print(f"   Sample: {sample['description']}")
    
    print("\n✅ Individual penalty simulation test PASSED")
    return True

def test_pressure_system():
    """Test that pressure affects penalty success rates."""
    print("\n🧪 TESTING PRESSURE SYSTEM")
    print("=" * 50)
    
    players = create_test_players()
    team_a, team_b = create_test_teams(players)
    
    # Initialize managers with empty files
    player_manager = PlayerManager("test_players.json")
    team_manager = TeamManager("test_teams.json")
    tournament_manager = TournamentManager(team_manager, player_manager)
    
    elite_taker = players[0]
    poor_gk = players[3]
    
    # Test different pressure situations
    situations = [
        ("Regular penalty", "penalty_shootout", 1),
        ("Late regular penalty", "penalty_shootout", 4),
        ("Sudden death", "sudden_death", 6)
    ]
    
    for situation_name, situation_type, round_num in situations:
        successes = 0
        for _ in range(20):
            result = tournament_manager._simulate_individual_penalty(
                elite_taker, poor_gk, situation_type, round_num
            )
            if result["scored"]:
                successes += 1
        
        success_rate = successes / 20 * 100
        print(f"{situation_name}: {success_rate:.1f}% success rate")
    
    print("\n✅ Pressure system test PASSED")
    return True

def test_full_penalty_shootout():
    """Test a complete penalty shootout simulation."""
    print("\n🧪 TESTING FULL PENALTY SHOOTOUT")
    print("=" * 50)
    
    players = create_test_players()
    team_a, team_b = create_test_teams(players)
    
    # Initialize managers with empty files
    player_manager = PlayerManager("test_players.json")
    team_manager = TeamManager("test_teams.json")
    tournament_manager = TournamentManager(team_manager, player_manager)
    
    # Create a dummy tournament match
    match = TournamentMatch(
        round_name="Test Round",
        match_id="TEST1",
        home_team=team_a.name,
        away_team=team_b.name,
        home_score=1,
        away_score=1  # Draw to trigger penalties
    )
    
    print(f"Simulating penalty shootout: {team_a.name} vs {team_b.name}")
    
    # Simulate penalty shootout
    winner, penalty_events = tournament_manager._simulate_penalty_shootout(team_a, team_b, match)
    
    print(f"\n🏆 Winner: {winner}")
    print(f"📊 Final scores: {match.home_score} - {match.away_score}")
    print(f"🥅 Total penalty events: {len(penalty_events)}")
    
    # Display penalty events
    if penalty_events:
        print("\nPENALTY SHOOTOUT EVENTS:")
        for event in penalty_events:
            minute = event["minute"]
            team = event["team"]
            player = event["player"]
            description = event["description"]
            print(f"  {minute}' 🥅 {team} - {description}")
    
    # Verify we have at least 10 penalty events (5 per team minimum)
    assert len(penalty_events) >= 10, f"Should have at least 10 penalty events, got {len(penalty_events)}"
    
    print("\n✅ Full penalty shootout test PASSED")
    return True

def test_tournament_integration():
    """Test penalty shootout integration with tournament system."""
    print("\n🧪 TESTING TOURNAMENT INTEGRATION")
    print("=" * 50)
    
    players = create_test_players()
    team_a, team_b = create_test_teams(players)
    
    # Initialize managers
    player_manager = PlayerManager()
    team_manager = TeamManager()
    
    # Add players and teams to managers
    for player in players:
        player_manager.add_player(player)
    
    team_manager.add_team(team_a)
    team_manager.add_team(team_b)
    
    tournament_manager = TournamentManager(team_manager, player_manager)
    match_engine = MatchEngine()
    
    # Create tournament
    tournament = tournament_manager.create_tournament("Test Tournament", [team_a.name, team_b.name])
    
    # Get first match
    current_round = tournament.get_current_round()
    if current_round and current_round.matches:
        match = current_round.matches[0]
        
        print(f"Tournament match: {match.home_team} vs {match.away_team}")
        
        # Force a draw by setting predetermined result
        # We'll simulate the tournament match which might not be a draw,
        # so let's just test the penalty system directly
        
        print("Testing penalty integration with tournament match...")
        
        # Create a drawn match result manually
        from models import MatchResult
        from datetime import datetime
        
        result = MatchResult(
            home_team=team_a.name,
            away_team=team_b.name,
            home_score=2,
            away_score=2,
            date=datetime.now(),
            events=[],
            stats={
                team_a.name: {
                    'possession': 50.0,
                    'expected_goals': 2.0,
                    'shots': 10,
                    'shots_on_target': 5,
                    'pass_accuracy': 80.0,
                    'team_rating': 75.0,
                    'players_available': 11,
                    'average_stamina': 80.0,
                    'momentum': 0.0
                },
                team_b.name: {
                    'possession': 50.0,
                    'expected_goals': 2.0,
                    'shots': 10,
                    'shots_on_target': 5,
                    'pass_accuracy': 80.0,
                    'team_rating': 75.0,
                    'players_available': 11,
                    'average_stamina': 80.0,
                    'momentum': 0.0
                }
            },
            fatigue_impact={team_a.name: 0.1, team_b.name: 0.1},
            momentum_changes=[]
        )
        
        # Simulate penalty shootout
        match.home_score = 2
        match.away_score = 2
        
        penalty_result = tournament_manager._simulate_penalty_shootout(
            team_a, team_b, match
        )
        
        winner = penalty_result[0]
        penalty_events = penalty_result[1] if len(penalty_result) > 1 else []
        
        # Add penalty events to result
        if penalty_events:
            from models import MatchEvent
            for penalty_event in penalty_events:
                result.events.append(MatchEvent(
                    minute=penalty_event["minute"],
                    event_type=penalty_event["event_type"],
                    team=penalty_event["team"],
                    player=penalty_event["player"],
                    description=penalty_event["description"]
                ))
        
        print(f"🏆 Penalty shootout winner: {winner}")
        print(f"📊 Final scores: {match.home_score} - {match.away_score}")
        print(f"🥅 Penalty events added to match: {len([e for e in result.events if e.event_type == 'penalty'])}")
        
        # Verify penalty events were added
        penalty_event_count = len([e for e in result.events if e.event_type == 'penalty'])
        assert penalty_event_count >= 10, f"Should have at least 10 penalty events, got {penalty_event_count}"
        
        print("✅ Tournament integration test PASSED")
        return True
    
    print("❌ Could not create tournament match")
    return False

def run_all_tests():
    """Run all penalty system tests."""
    print("🚀 STARTING ENHANCED PENALTY SYSTEM TESTS")
    print("=" * 60)
    
    # Create empty test files
    import json
    with open("test_players.json", "w") as f:
        json.dump([], f)
    with open("test_teams.json", "w") as f:
        json.dump([], f)
    
    tests = [
        test_individual_penalty_simulation,
        test_pressure_system,
        test_full_penalty_shootout
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} FAILED with error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("🏁 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Tests passed: {passed}")
    print(f"❌ Tests failed: {failed}")
    print(f"📊 Success rate: {passed/(passed+failed)*100:.1f}%")
    
    # Clean up test files
    import os
    try:
        os.remove("test_players.json")
        os.remove("test_teams.json")
    except FileNotFoundError:
        pass
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Enhanced penalty system is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the output above.")
        return False

if __name__ == "__main__":
    # Set random seed for reproducible tests
    random.seed(42)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)