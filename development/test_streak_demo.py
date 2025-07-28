#!/usr/bin/env python3
"""
Streak Demo
~~~~~~~~~~~

Demonstrates the streak/momentum system in action.
"""

from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import TacticalStyle


def main():
    """Demo the streak system."""
    print("=" * 80)
    print("FANTASY FOOTBALL - STREAK SYSTEM DEMO")
    print("=" * 80)
    
    # Initialize managers
    pm = PlayerManager("streak_demo_players.json")
    tm = TeamManager("streak_demo_teams.json")
    me = MatchEngine(use_momentum=True)
    
    # Generate players
    print("\n🔄 Setting up demo...")
    players = pm.generate_player_pool(60, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    # Create two teams
    chelsea = tm.create_random_team("Chelsea", pm.players, "4-3-3", TacticalStyle.ATTACKING)
    arsenal = tm.create_random_team("Arsenal", pm.players, "4-2-3-1", TacticalStyle.BALANCED)
    
    if not chelsea or not arsenal:
        print("❌ Failed to create teams!")
        return
    
    tm.add_team(chelsea)
    tm.add_team(arsenal)
    
    print(f"✅ Created {chelsea.name} vs {arsenal.name}")
    print(f"Initial ratings: {chelsea.name} ({chelsea.elo_rating:.0f}) vs {arsenal.name} ({arsenal.elo_rating:.0f})")
    
    # Simulate 10 matches to build streaks
    print(f"\n{'='*80}")
    print("SIMULATING 10 MATCHES TO DEMONSTRATE STREAK EFFECTS")
    print(f"{'='*80}")
    
    results = []
    for match_num in range(1, 11):
        print(f"\n🎯 MATCH {match_num}")
        print("-" * 40)
        
        # Show pre-match status
        print(f"Before: {chelsea.name} (Elo: {chelsea.elo_rating:.0f}, Streak: {format_streak(chelsea.streak_count)}) vs "
              f"{arsenal.name} (Elo: {arsenal.elo_rating:.0f}, Streak: {format_streak(arsenal.streak_count)})")
        
        # Show momentum multipliers
        chelsea_momentum = chelsea.adjust_for_streak()
        arsenal_momentum = arsenal.adjust_for_streak()
        if chelsea_momentum != 1.0 or arsenal_momentum != 1.0:
            print(f"🔥 Momentum: {chelsea.name} {chelsea_momentum:.1%}, {arsenal.name} {arsenal_momentum:.1%}")
        
        # Simulate match
        result = me.simulate_match(chelsea, arsenal)
        results.append(result)
        
        # Update Elo
        tm.update_team_elo(chelsea.name, arsenal.name, (result.home_score, result.away_score))
        
        # Show result
        if result.home_score > result.away_score:
            result_emoji = "🏠"
            winner = chelsea.name
        elif result.away_score > result.home_score:
            result_emoji = "✈️"
            winner = arsenal.name
        else:
            result_emoji = "🤝"
            winner = "Draw"
        
        print(f"{result_emoji} Result: {result.home_team} {result.home_score} - {result.away_score} {result.away_team} ({winner})")
        print(f"After:  {chelsea.name} (Elo: {chelsea.elo_rating:.0f}, Streak: {format_streak(chelsea.streak_count)}) vs "
              f"{arsenal.name} (Elo: {arsenal.elo_rating:.0f}, Streak: {format_streak(arsenal.streak_count)})")
        
        # Highlight significant streaks
        if abs(chelsea.streak_count) >= 3:
            print(f"🔥 {chelsea.name} is on a {format_streak(chelsea.streak_count)} streak!")
        if abs(arsenal.streak_count) >= 3:
            print(f"🔥 {arsenal.name} is on a {format_streak(arsenal.streak_count)} streak!")
    
    # Final analysis
    print(f"\n{'='*80}")
    print("FINAL ANALYSIS")
    print(f"{'='*80}")
    
    chelsea_wins = sum(1 for r in results if r.home_score > r.away_score)
    arsenal_wins = sum(1 for r in results if r.away_score > r.home_score)
    draws = len(results) - chelsea_wins - arsenal_wins
    
    print(f"\n📊 Match Results:")
    print(f"   🏠 {chelsea.name} wins: {chelsea_wins}")
    print(f"   ✈️  {arsenal.name} wins: {arsenal_wins}")
    print(f"   🤝 Draws: {draws}")
    
    print(f"\n📈 Rating Changes:")
    print(f"   {chelsea.name}: 1500 → {chelsea.elo_rating:.0f} ({chelsea.elo_rating-1500:+.0f})")
    print(f"   {arsenal.name}: 1500 → {arsenal.elo_rating:.0f} ({arsenal.elo_rating-1500:+.0f})")
    
    print(f"\n🔥 Final Streaks:")
    print(f"   {chelsea.name}: {format_streak(chelsea.streak_count)}")
    print(f"   {arsenal.name}: {format_streak(arsenal.streak_count)}")
    
    # Show momentum effects
    final_chelsea_momentum = chelsea.adjust_for_streak()
    final_arsenal_momentum = arsenal.adjust_for_streak()
    
    if final_chelsea_momentum != 1.0 or final_arsenal_momentum != 1.0:
        print(f"\n⚡ Current Momentum Effects:")
        print(f"   {chelsea.name}: {final_chelsea_momentum:.1%} performance")
        print(f"   {arsenal.name}: {final_arsenal_momentum:.1%} performance")
    
    print(f"\n{'='*80}")
    print("DEMO COMPLETE!")
    print("Notice how teams on winning streaks get momentum bonuses,")
    print("while teams on losing streaks get penalties.")
    print("This creates realistic hot/cold streaks in performance!")
    print(f"{'='*80}")
    
    # Clean up
    import os
    try:
        os.remove("streak_demo_players.json")
        os.remove("streak_demo_teams.json")
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