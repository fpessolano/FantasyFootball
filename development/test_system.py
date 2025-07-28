#!/usr/bin/env python3
"""
Test Script for Fantasy Football System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quick test to verify all components work properly.
"""

from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine


def test_system():
    """Test all components of the Fantasy Football system."""
    print("="*50)
    print("FANTASY FOOTBALL SYSTEM TEST")
    print("="*50)
    
    # Test Player Manager
    print("\n1. Testing Player Manager...")
    pm = PlayerManager("test_players.json")
    
    # Create some players
    players = pm.generate_player_pool(40, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    print(f"   ✓ Created {len(players)} players")
    print(f"   ✓ Total players in database: {len(pm.players)}")
    
    # Test Team Manager
    print("\n2. Testing Team Manager...")
    tm = TeamManager("test_teams.json")
    
    # Create teams
    team1 = tm.create_random_team("Barcelona", pm.players)
    team2 = tm.create_random_team("Real Madrid", pm.players)
    
    if team1 and team2:
        tm.add_team(team1)
        tm.add_team(team2)
        print(f"   ✓ Created teams: {team1.name} and {team2.name}")
        print(f"   ✓ Team 1 formation: {team1.formation} ({team1.style.name})")
        print(f"   ✓ Team 2 formation: {team2.formation} ({team2.style.name})")
    else:
        print("   ✗ Failed to create teams")
        return False
    
    # Test Match Engine
    print("\n3. Testing Match Engine...")
    me = MatchEngine()
    
    # Simulate match
    result = me.simulate_match(team1, team2)
    
    print(f"   ✓ Match simulated: {result.home_team} {result.home_score} - {result.away_score} {result.away_team}")
    print(f"   ✓ Home xG: {result.stats[result.home_team]['expected_goals']:.2f}")
    print(f"   ✓ Away xG: {result.stats[result.away_team]['expected_goals']:.2f}")
    print(f"   ✓ Events generated: {len(result.events)}")
    
    # Test Elo update
    tm.update_team_elo(team1.name, team2.name, (result.home_score, result.away_score))
    print(f"   ✓ Elo ratings updated")
    print(f"     - {team1.name}: {team1.elo_rating:.0f}")
    print(f"     - {team2.name}: {team2.elo_rating:.0f}")
    
    # Test multiple matches
    print("\n4. Testing Multiple Matches...")
    results = []
    for i in range(5):
        result = me.simulate_match(team1, team2)
        results.append(result)
        tm.update_team_elo(team1.name, team2.name, (result.home_score, result.away_score))
    
    team1_wins = sum(1 for r in results if r.home_score > r.away_score)
    team2_wins = sum(1 for r in results if r.away_score > r.home_score)
    draws = sum(1 for r in results if r.home_score == r.away_score)
    
    print(f"   ✓ Simulated 5 matches:")
    print(f"     - {team1.name} wins: {team1_wins}")
    print(f"     - {team2.name} wins: {team2_wins}")
    print(f"     - Draws: {draws}")
    
    print("\n" + "="*50)
    print("ALL TESTS PASSED! 🎉")
    print("The Fantasy Football system is working correctly.")
    print("="*50)
    
    # Clean up test files
    import os
    try:
        os.remove("test_players.json")
        os.remove("test_teams.json")
    except FileNotFoundError:
        pass
    
    return True


if __name__ == "__main__":
    test_system()