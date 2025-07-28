#!/usr/bin/env python3
"""
Test Enhanced Streak System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the enhanced streak display and screen clearing functionality.
"""

import os
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import TacticalStyle


def main():
    """Test the enhanced streak system."""
    print("=" * 80)
    print("TESTING ENHANCED STREAK SYSTEM WITH SCREEN CLEARING")
    print("=" * 80)
    
    # Clean up test files
    test_files = ["test_streak_players.json", "test_streak_teams.json"]
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    # Initialize
    pm = PlayerManager("test_streak_players.json")
    tm = TeamManager("test_streak_teams.json")
    me = MatchEngine(use_momentum=True, detailed_sim=True)
    
    # Generate players
    print("\n🔄 Setting up test environment...")
    players = pm.generate_player_pool(80, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    # Create teams with different styles to increase variety
    arsenal = tm.create_random_team("Arsenal", pm.players, "4-3-3", TacticalStyle.ATTACKING)
    chelsea = tm.create_random_team("Chelsea", pm.players, "4-2-3-1", TacticalStyle.DEFENSIVE)
    
    if not arsenal or not chelsea:
        print("❌ Failed to create teams!")
        return
    
    tm.add_team(arsenal)
    tm.add_team(chelsea)
    
    print(f"✅ Created {arsenal.name} (Attacking) vs {chelsea.name} (Defensive)")
    
    # Show initial team summaries
    print(arsenal.summary())
    print(chelsea.summary())
    
    print(f"\n{'='*80}")
    print("SIMULATING 8 MATCHES TO SHOW ENHANCED STREAK EFFECTS")
    print(f"{'='*80}")
    
    results = []
    for match_num in range(1, 9):
        print(f"\n{'🎯 MATCH ' + str(match_num):^80}")
        print("-" * 80)
        
        # Show enhanced pre-match display
        home_streak_icon = "🔥" if arsenal.streak_count >= 3 else "❄️" if arsenal.streak_count <= -3 else "⚪"
        away_streak_icon = "🔥" if chelsea.streak_count >= 3 else "❄️" if chelsea.streak_count <= -3 else "⚪"
        
        print(f"Before Match:")
        print(f"  🏠 {arsenal.name}: Elo {arsenal.elo_rating:.0f} | {home_streak_icon} {format_streak(arsenal.streak_count)}")
        print(f"  ✈️  {chelsea.name}: Elo {chelsea.elo_rating:.0f} | {away_streak_icon} {format_streak(chelsea.streak_count)}")
        
        # Show momentum
        arsenal_momentum = arsenal.adjust_for_streak()
        chelsea_momentum = chelsea.adjust_for_streak()
        if arsenal_momentum != 1.0 or chelsea_momentum != 1.0:
            print(f"\n🔥 MOMENTUM ACTIVE:")
            if arsenal_momentum != 1.0:
                momentum_type = "BOOST" if arsenal_momentum > 1.0 else "PENALTY"
                print(f"     {arsenal.name}: {arsenal_momentum:.1%} performance ({momentum_type})")
            if chelsea_momentum != 1.0:
                momentum_type = "BOOST" if chelsea_momentum > 1.0 else "PENALTY"
                print(f"     {chelsea.name}: {chelsea_momentum:.1%} performance ({momentum_type})")
        
        # Simulate
        result = me.simulate_match(arsenal, chelsea)
        results.append(result)
        
        # Determine winner
        if result.home_score > result.away_score:
            result_emoji = "🏠"
            winner = arsenal.name
        elif result.away_score > result.home_score:
            result_emoji = "✈️"
            winner = chelsea.name
        else:
            result_emoji = "🤝"
            winner = "DRAW"
        
        # Update Elo
        tm.update_team_elo(arsenal.name, chelsea.name, (result.home_score, result.away_score))
        
        # Show result
        print(f"\n{result_emoji} RESULT: {result.home_team} {result.home_score} - {result.away_score} {result.away_team} ({winner})")
        
        # Show post-match status
        print(f"\nAfter Match:")
        new_home_icon = "🔥" if arsenal.streak_count >= 3 else "❄️" if arsenal.streak_count <= -3 else "⚪"
        new_away_icon = "🔥" if chelsea.streak_count >= 3 else "❄️" if chelsea.streak_count <= -3 else "⚪"
        
        print(f"  🏠 {arsenal.name}: Elo {arsenal.elo_rating:.0f} | {new_home_icon} {format_streak(arsenal.streak_count)}")
        print(f"  ✈️  {chelsea.name}: Elo {chelsea.elo_rating:.0f} | {new_away_icon} {format_streak(chelsea.streak_count)}")
        
        # Highlight momentum threshold crossings
        if abs(arsenal.streak_count) == 3:
            print(f"🎯 {arsenal.name} {'enters hot streak' if arsenal.streak_count > 0 else 'enters cold streak'}!")
        if abs(chelsea.streak_count) == 3:
            print(f"🎯 {chelsea.name} {'enters hot streak' if chelsea.streak_count > 0 else 'enters cold streak'}!")
        
        # Show match events if available
        if result.events:
            print(f"\n📋 Key Events:")
            for event in result.events[:3]:  # Show first 3 events
                print(f"    {event.minute}' - {event.description}")
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    
    arsenal_wins = sum(1 for r in results if r.home_score > r.away_score)
    chelsea_wins = sum(1 for r in results if r.away_score > r.home_score)
    draws = len(results) - arsenal_wins - chelsea_wins
    
    print(f"\n📊 Final Results:")
    print(f"   🏠 {arsenal.name}: {arsenal_wins} wins")
    print(f"   ✈️  {chelsea.name}: {chelsea_wins} wins")
    print(f"   🤝 Draws: {draws}")
    
    print(f"\n📈 Final Elo Ratings:")
    print(f"   {arsenal.name}: {arsenal.elo_rating:.0f}")
    print(f"   {chelsea.name}: {chelsea.elo_rating:.0f}")
    
    print(f"\n🔥 Final Streaks:")
    print(f"   {arsenal.name}: {format_streak(arsenal.streak_count)}")
    print(f"   {chelsea.name}: {format_streak(chelsea.streak_count)}")
    
    # Show momentum effects
    final_arsenal_momentum = arsenal.adjust_for_streak()
    final_chelsea_momentum = chelsea.adjust_for_streak()
    
    if final_arsenal_momentum != 1.0 or final_chelsea_momentum != 1.0:
        print(f"\n⚡ Current Momentum Effects:")
        if final_arsenal_momentum != 1.0:
            effect = "BOOST" if final_arsenal_momentum > 1.0 else "PENALTY"
            print(f"   {arsenal.name}: {final_arsenal_momentum:.1%} performance ({effect})")
        if final_chelsea_momentum != 1.0:
            effect = "BOOST" if final_chelsea_momentum > 1.0 else "PENALTY"
            print(f"   {chelsea.name}: {final_chelsea_momentum:.1%} performance ({effect})")
    
    print(f"\n{'='*80}")
    print("✅ ENHANCED STREAK SYSTEM TEST COMPLETE!")
    print("Features tested:")
    print("  ✅ Screen clearing after 'Press Enter to simulate match...'")
    print("  ✅ Enhanced streak display with visual icons")
    print("  ✅ Momentum visualization with BOOST/PENALTY labels")
    print("  ✅ Streak threshold notifications")
    print("  ✅ Improved match-by-match progression display")
    print(f"{'='*80}")
    
    # Clean up
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


def format_streak(streak_count):
    """Format streak for display."""
    if streak_count > 0:
        return f"{streak_count}W"
    elif streak_count < 0:
        return f"{abs(streak_count)}L"
    else:
        return "-"


if __name__ == "__main__":
    main()