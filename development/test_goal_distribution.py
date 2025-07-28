#!/usr/bin/env python3
"""
Test Goal Distribution Fix
~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the improved goal generation to verify it reduces excessive draws.
"""

import os
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from collections import defaultdict


def main():
    """Test the improved goal distribution."""
    print("=" * 80)
    print("TESTING IMPROVED GOAL DISTRIBUTION")
    print("=" * 80)
    
    # Clean up test files
    test_files = ["test_goals_players.json", "test_goals_teams.json"]
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    # Initialize
    pm = PlayerManager("test_goals_players.json")
    tm = TeamManager("test_goals_teams.json")
    me = MatchEngine(use_momentum=True, detailed_sim=False)  # Fast simulation
    
    # Generate players and teams
    print("\n🔄 Setting up test environment...")
    players = pm.generate_player_pool(50, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    # Create two balanced teams
    team_a = tm.create_random_team("Team A", pm.players)
    team_b = tm.create_random_team("Team B", pm.players)
    
    if not team_a or not team_b:
        print("❌ Failed to create teams!")
        return
    
    print(f"✅ Created teams: {team_a.name} vs {team_b.name}")
    print(f"   {team_a.name} strength: {team_a.compute_strength():.1f}")
    print(f"   {team_b.name} strength: {team_b.compute_strength():.1f}")
    
    # Simulate many matches to test distribution
    num_matches = 100
    print(f"\n🎮 Simulating {num_matches} matches to test goal distribution...")
    
    results = defaultdict(int)  # (home_goals, away_goals) -> count
    draws = 0
    total_goals = 0
    home_wins = away_wins = 0
    
    for i in range(num_matches):
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i + 1}/{num_matches} matches")
        
        result = me.simulate_match(team_a, team_b)
        
        score_key = (result.home_score, result.away_score)
        results[score_key] += 1
        
        total_goals += result.home_score + result.away_score
        
        if result.home_score > result.away_score:
            home_wins += 1
        elif result.away_score > result.home_score:
            away_wins += 1
        else:
            draws += 1
    
    print(f"\n{'='*80}")
    print("GOAL DISTRIBUTION ANALYSIS")
    print(f"{'='*80}")
    
    # Overall statistics
    print(f"\n📊 Overall Results ({num_matches} matches):")
    print(f"   🏠 {team_a.name} wins: {home_wins} ({home_wins/num_matches*100:.1f}%)")
    print(f"   ✈️  {team_b.name} wins: {away_wins} ({away_wins/num_matches*100:.1f}%)")
    print(f"   🤝 Draws: {draws} ({draws/num_matches*100:.1f}%)")
    
    avg_goals = total_goals / num_matches
    print(f"\n⚽ Goal Statistics:")
    print(f"   Total goals: {total_goals}")
    print(f"   Average per match: {avg_goals:.2f}")
    print(f"   Goals per team per match: {avg_goals/2:.2f}")
    
    # Score distribution
    print(f"\n📋 Most Common Scorelines:")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    for i, ((home, away), count) in enumerate(sorted_results[:10], 1):
        percentage = count / num_matches * 100
        result_type = "DRAW" if home == away else f"{team_a.name if home > away else team_b.name} WIN"
        print(f"   {i:2d}. {home}-{away}: {count:2d} times ({percentage:4.1f}%) [{result_type}]")
    
    # Analysis
    print(f"\n🔍 Analysis:")
    draw_percentage = draws / num_matches * 100
    
    if draw_percentage > 35:
        print(f"   ⚠️  High draw rate: {draw_percentage:.1f}% (still problematic)")
    elif draw_percentage > 25:
        print(f"   ⚡ Moderate draw rate: {draw_percentage:.1f}% (acceptable)")
    else:
        print(f"   ✅ Good draw rate: {draw_percentage:.1f}% (realistic)")
    
    if avg_goals < 1.5:
        print(f"   ⚠️  Low scoring: {avg_goals:.2f} goals per match")
    elif avg_goals > 4.0:
        print(f"   ⚠️  High scoring: {avg_goals:.2f} goals per match")
    else:
        print(f"   ✅ Realistic scoring: {avg_goals:.2f} goals per match")
    
    # Check for variety in scores
    unique_scores = len(results)
    print(f"   📈 Score variety: {unique_scores} different scorelines")
    
    zero_zero_count = results.get((0, 0), 0)
    zero_zero_pct = zero_zero_count / num_matches * 100
    print(f"   🥅 0-0 draws: {zero_zero_count} ({zero_zero_pct:.1f}%)")
    
    print(f"\n{'='*80}")
    print("✅ GOAL DISTRIBUTION TEST COMPLETE!")
    
    if draw_percentage <= 30 and 1.8 <= avg_goals <= 3.5:
        print("🎉 SUCCESS: Goal distribution looks much more realistic!")
    else:
        print("⚠️  REVIEW NEEDED: Distribution may still need adjustment")
    
    print(f"{'='*80}")
    
    # Clean up
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()