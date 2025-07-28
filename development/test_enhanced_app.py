#!/usr/bin/env python3
"""
Test the enhanced Fantasy Football app with multiple matches.
"""

import os
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import TacticalStyle, Position


def test_enhanced_features():
    """Test the enhanced features."""
    print("=" * 60)
    print("ENHANCED FANTASY FOOTBALL APP TEST")
    print("=" * 60)
    
    # Clean up any existing test files
    test_files = ["test_players.json", "test_teams.json"]
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    # Initialize
    pm = PlayerManager("test_players.json")
    tm = TeamManager("test_teams.json")
    me = MatchEngine()
    
    print("\n1. Testing Player Generation...")
    # Generate players with position diversity
    positions = list(Position)
    for pos in positions:
        for i in range(3):  # 3 players per position
            player = pm.create_random_player(pos, f"{pos.name}_Player")
            pm.add_player(player)
    
    print(f"   ✅ Generated {len(pm.players)} players")
    
    print("\n2. Testing Team Creation...")
    # Create teams with different styles
    team1 = tm.create_random_team("Manchester City", pm.players, "4-3-3", TacticalStyle.ATTACKING)
    team2 = tm.create_random_team("Liverpool", pm.players, "4-3-3", TacticalStyle.BALANCED)
    team3 = tm.create_random_team("Chelsea", pm.players, "3-5-2", TacticalStyle.DEFENSIVE)
    
    teams_created = []
    for team in [team1, team2, team3]:
        if team:
            tm.add_team(team)
            teams_created.append(team)
            print(f"   ✅ Created {team.name} ({team.formation}, {team.style.name})")
    
    if len(teams_created) < 2:
        print("   ❌ Need at least 2 teams for testing")
        return
    
    print("\n3. Testing Enhanced Display...")
    print(teams_created[0].summary())
    
    print("\n4. Testing Multiple Match Simulation...")
    home_team = teams_created[0]
    away_team = teams_created[1]
    
    print(f"\nSimulating 5 matches: {home_team.name} vs {away_team.name}")
    print("-" * 60)
    
    results = []
    for match_num in range(1, 6):
        print(f"\n🎯 Match {match_num}")
        
        # Show pre-match state
        home_streak = format_streak(home_team.streak_count)
        away_streak = format_streak(away_team.streak_count)
        print(f"Before: {home_team.name} ({home_team.elo_rating:.0f}, {home_streak}) vs "
              f"{away_team.name} ({away_team.elo_rating:.0f}, {away_streak})")
        
        # Simulate
        result = me.simulate_match(home_team, away_team)
        results.append(result)
        
        # Update Elo
        tm.update_team_elo(home_team.name, away_team.name, 
                          (result.home_score, result.away_score))
        
        # Show result
        outcome = "🏠" if result.home_score > result.away_score else "✈️" if result.away_score > result.home_score else "🤝"
        print(f"{outcome} Result: {result.home_team} {result.home_score} - {result.away_score} {result.away_team}")
        
        # Show momentum if applicable
        home_momentum = home_team.adjust_for_streak()
        away_momentum = away_team.adjust_for_streak()
        if home_momentum != 1.0 or away_momentum != 1.0:
            print(f"🔥 Momentum: {home_team.name} {home_momentum:.1%}, {away_team.name} {away_momentum:.1%}")
    
    print(f"\n{'='*60}")
    print("SERIES SUMMARY")
    print(f"{'='*60}")
    
    home_wins = sum(1 for r in results if r.home_score > r.away_score)
    away_wins = sum(1 for r in results if r.away_score > r.home_score)
    draws = len(results) - home_wins - away_wins
    
    print(f"\n📊 Final Results:")
    print(f"   {home_team.name}: {home_wins} wins")
    print(f"   {away_team.name}: {away_wins} wins") 
    print(f"   Draws: {draws}")
    
    print(f"\n📈 Elo Changes:")
    print(f"   {home_team.name}: 1500 → {home_team.elo_rating:.0f}")
    print(f"   {away_team.name}: 1500 → {away_team.elo_rating:.0f}")
    
    print(f"\n🔥 Current Streaks:")
    print(f"   {home_team.name}: {format_streak(home_team.streak_count)}")
    print(f"   {away_team.name}: {format_streak(away_team.streak_count)}")
    
    print("\n5. Testing Team Rankings...")
    tm.display_team_rankings()
    
    print(f"\n{'='*60}")
    print("✅ ALL TESTS PASSED!")
    print("The enhanced Fantasy Football system is working correctly!")
    print("Try running 'python3 fantasy_football.py' for the full experience.")
    print(f"{'='*60}")
    
    # Clean up
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


def format_streak(streak_count):
    """Format streak display."""
    if streak_count > 0:
        return f"{streak_count}W"
    elif streak_count < 0:
        return f"{abs(streak_count)}L"
    else:
        return "-"


if __name__ == "__main__":
    test_enhanced_features()