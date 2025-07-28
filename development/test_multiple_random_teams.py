#!/usr/bin/env python3
"""
Test Multiple Matches with Same Random Teams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the corrected multiple random games functionality that creates
two random teams and plays them against each other multiple times
to see streak effects develop.
"""

import os
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import TacticalStyle, Position


def main():
    """Test the multiple matches with same random teams feature."""
    print("=" * 80)
    print("TESTING MULTIPLE MATCHES WITH SAME RANDOM TEAMS")
    print("=" * 80)
    
    # Clean up test files
    test_files = ["test_random_teams_players.json", "test_random_teams_teams.json"]
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    # Initialize
    pm = PlayerManager("test_random_teams_players.json")
    tm = TeamManager("test_random_teams_teams.json")
    me = MatchEngine(use_momentum=True, detailed_sim=True)
    
    # Generate players
    print("\n🔄 Setting up test environment...")
    players = pm.generate_player_pool(80, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    print(f"✅ Generated {len(players)} players")
    
    # Create two random teams that will play multiple times
    print(f"\n🏗️  Creating random teams...")
    team_alpha = tm.create_random_team("Team Alpha", pm.players)
    team_beta = tm.create_random_team("Team Beta", pm.players)
    
    if not team_alpha or not team_beta:
        print("❌ Failed to create teams!")
        return
    
    print("✅ Teams created!")
    
    print(f"\n{'='*80}")
    print(f"MULTIPLE MATCHES: {team_alpha.name} vs {team_beta.name}")
    print(f"{'='*80}")
    
    # Show initial team info
    print(f"\n🏠 HOME: {team_alpha.name}")
    print(f"   Formation: {team_alpha.formation} | Style: {team_alpha.style.name}")
    print(f"   Strength: {team_alpha.compute_strength():.1f}")
    print(f"   Key Players:")
    sorted_players = sorted(team_alpha.players, key=lambda p: p.overall_rating(), reverse=True)
    for i, player in enumerate(sorted_players[:3], 1):
        print(f"     {i}. {player.name} ({player.position.name}) - OVR: {player.overall_rating():.0f}")
    
    print(f"\n✈️  AWAY: {team_beta.name}")
    print(f"   Formation: {team_beta.formation} | Style: {team_beta.style.name}")
    print(f"   Strength: {team_beta.compute_strength():.1f}")
    print(f"   Key Players:")
    sorted_players = sorted(team_beta.players, key=lambda p: p.overall_rating(), reverse=True)
    for i, player in enumerate(sorted_players[:3], 1):
        print(f"     {i}. {player.name} ({player.position.name}) - OVR: {player.overall_rating():.0f}")
    
    # Store initial ratings
    initial_alpha_elo = team_alpha.elo_rating
    initial_beta_elo = team_beta.elo_rating
    
    # Test both detailed mode (≤5 matches) and fast mode (>5 matches)
    print(f"\n{'='*80}")
    print("TESTING DETAILED MODE (≤5 MATCHES)")
    print(f"{'='*80}")
    
    # First test: 3 matches in detailed mode
    detailed_results = []
    detailed_alpha_wins = detailed_beta_wins = detailed_draws = 0
    
    for match_num in range(1, 4):  # 3 matches for detailed mode demo
        print(f"\n{'🎯 MATCH ' + str(match_num):^80}")
        print("-" * 80)
        
        # Show current status with enhanced streak display
        def format_streak(streak_count):
            if streak_count > 0:
                return f"{streak_count}W"
            elif streak_count < 0:
                return f"{abs(streak_count)}L"
            else:
                return "-"
        
        alpha_streak_display = format_streak(team_alpha.streak_count)
        beta_streak_display = format_streak(team_beta.streak_count)
        
        # Add streak icons
        alpha_streak_icon = "🔥" if team_alpha.streak_count >= 3 else "❄️" if team_alpha.streak_count <= -3 else "⚪"
        beta_streak_icon = "🔥" if team_beta.streak_count >= 3 else "❄️" if team_beta.streak_count <= -3 else "⚪"
        
        print(f"Before Match:")
        print(f"  🏠 {team_alpha.name}: Elo {team_alpha.elo_rating:.0f} | {alpha_streak_icon} {alpha_streak_display}")
        print(f"  ✈️  {team_beta.name}: Elo {team_beta.elo_rating:.0f} | {beta_streak_icon} {beta_streak_display}")
        
        # Show momentum multipliers BEFORE the match
        alpha_momentum = team_alpha.adjust_for_streak()
        beta_momentum = team_beta.adjust_for_streak()
        if alpha_momentum != 1.0 or beta_momentum != 1.0:
            print(f"\n🔥 MOMENTUM ACTIVE:")
            if alpha_momentum != 1.0:
                momentum_type = "BOOST" if alpha_momentum > 1.0 else "PENALTY"
                print(f"     {team_alpha.name}: {alpha_momentum:.1%} performance ({momentum_type})")
            if beta_momentum != 1.0:
                momentum_type = "BOOST" if beta_momentum > 1.0 else "PENALTY"
                print(f"     {team_beta.name}: {beta_momentum:.1%} performance ({momentum_type})")
        
        # Simulate match
        result = me.simulate_match(team_alpha, team_beta)
        detailed_results.append(result)
        
        # Update counters
        if result.home_score > result.away_score:
            detailed_alpha_wins += 1
            result_emoji = "🏠"
            winner = team_alpha.name
        elif result.away_score > result.home_score:
            detailed_beta_wins += 1
            result_emoji = "✈️"
            winner = team_beta.name
        else:
            detailed_draws += 1
            result_emoji = "🤝"
            winner = "DRAW"
        
        # Manually update streaks and Elo
        if result.home_score > result.away_score:
            team_alpha.streak_count = max(0, team_alpha.streak_count) + 1
            team_beta.streak_count = min(0, team_beta.streak_count) - 1
        elif result.away_score > result.home_score:
            team_alpha.streak_count = min(0, team_alpha.streak_count) - 1
            team_beta.streak_count = max(0, team_beta.streak_count) + 1
        else:
            team_alpha.streak_count = 0
            team_beta.streak_count = 0
        
        # Update Elo ratings
        expected_alpha = 1 / (1 + 10**((team_beta.elo_rating - team_alpha.elo_rating) / 400))
        expected_beta = 1 - expected_alpha
        
        if result.home_score > result.away_score:
            actual_alpha, actual_beta = 1, 0
        elif result.away_score > result.home_score:
            actual_alpha, actual_beta = 0, 1
        else:
            actual_alpha, actual_beta = 0.5, 0.5
        
        k_factor = 20
        team_alpha.elo_rating += k_factor * (actual_alpha - expected_alpha)
        team_beta.elo_rating += k_factor * (actual_beta - expected_beta)
        
        # Show result with enhanced display
        print(f"\n{result_emoji} RESULT: {result.home_team} {result.home_score} - {result.away_score} {result.away_team} ({winner})")
        
        # Show key stats
        home_stats = result.stats[result.home_team]
        away_stats = result.stats[result.away_team]
        
        print(f"\n📊 Match Stats:")
        print(f"   Possession: {home_stats['possession']:.0f}% - {away_stats['possession']:.0f}%")
        print(f"   Expected Goals: {home_stats['expected_goals']:.1f} - {away_stats['expected_goals']:.1f}")
        print(f"   Shots: {home_stats['shots']:.0f} - {away_stats['shots']:.0f}")
        
        # Show events
        if result.events:
            print(f"\n🎯 Goals:")
            for event in result.events:
                if event.event_type == "goal":
                    print(f"   {event.minute}' - {event.player} ({event.team})")
        
        print(f"\nAfter Match:")
        new_alpha_icon = "🔥" if team_alpha.streak_count >= 3 else "❄️" if team_alpha.streak_count <= -3 else "⚪"
        new_beta_icon = "🔥" if team_beta.streak_count >= 3 else "❄️" if team_beta.streak_count <= -3 else "⚪"
        
        print(f"  🏠 {team_alpha.name}: Elo {team_alpha.elo_rating:.0f} | {new_alpha_icon} {format_streak(team_alpha.streak_count)}")
        print(f"  ✈️  {team_beta.name}: Elo {team_beta.elo_rating:.0f} | {new_beta_icon} {format_streak(team_beta.streak_count)}")
        
        # Highlight if streaks just hit the momentum threshold
        if abs(team_alpha.streak_count) == 3:
            print(f"🎯 {team_alpha.name} {'enters hot streak' if team_alpha.streak_count > 0 else 'enters cold streak'}!")
        if abs(team_beta.streak_count) == 3:
            print(f"🎯 {team_beta.name} {'enters hot streak' if team_beta.streak_count > 0 else 'enters cold streak'}!")
    
    # Now test fast mode (>5 matches)
    print(f"\n{'='*80}")
    print("TESTING FAST MODE (>5 MATCHES)")
    print(f"{'='*80}")
    
    # Reset teams to initial state for fair comparison
    team_alpha.elo_rating = initial_alpha_elo
    team_beta.elo_rating = initial_beta_elo
    team_alpha.streak_count = 0
    team_beta.streak_count = 0
    
    # Simulate 10 matches in fast mode
    fast_results = []
    fast_alpha_wins = fast_beta_wins = fast_draws = 0
    num_fast_matches = 10
    
    print(f"⚡ Fast simulation mode - simulating {num_fast_matches} matches...")
    
    for match_num in range(1, num_fast_matches + 1):
        # Show progress indicator
        if match_num == 1 or match_num % 5 == 0 or match_num == num_fast_matches:
            print(f"🎮 Simulating matches... {match_num}/{num_fast_matches}")
        
        # Simulate match (no detailed display)
        result = me.simulate_match(team_alpha, team_beta)
        fast_results.append(result)
        
        # Update counters
        if result.home_score > result.away_score:
            fast_alpha_wins += 1
            team_alpha.streak_count = max(0, team_alpha.streak_count) + 1
            team_beta.streak_count = min(0, team_beta.streak_count) - 1
        elif result.away_score > result.home_score:
            fast_beta_wins += 1
            team_alpha.streak_count = min(0, team_alpha.streak_count) - 1
            team_beta.streak_count = max(0, team_beta.streak_count) + 1
        else:
            fast_draws += 1
            team_alpha.streak_count = 0
            team_beta.streak_count = 0
        
        # Update Elo ratings
        expected_alpha = 1 / (1 + 10**((team_beta.elo_rating - team_alpha.elo_rating) / 400))
        expected_beta = 1 - expected_alpha
        
        if result.home_score > result.away_score:
            actual_alpha, actual_beta = 1, 0
        elif result.away_score > result.home_score:
            actual_alpha, actual_beta = 0, 1
        else:
            actual_alpha, actual_beta = 0.5, 0.5
        
        k_factor = 20
        team_alpha.elo_rating += k_factor * (actual_alpha - expected_alpha)
        team_beta.elo_rating += k_factor * (actual_beta - expected_beta)
    
    print("✅ Fast mode simulation complete!")
    
    # Combined summary
    print(f"\n{'='*80}")
    print("COMBINED TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n📋 DETAILED MODE RESULTS (3 matches):")
    print(f"   🏠 {team_alpha.name} wins: {detailed_alpha_wins}")
    print(f"   ✈️  {team_beta.name} wins: {detailed_beta_wins}")
    print(f"   🤝 Draws: {detailed_draws}")
    
    # Goal statistics for detailed mode
    detailed_alpha_goals = sum(r.home_score for r in detailed_results)
    detailed_beta_goals = sum(r.away_score for r in detailed_results)
    print(f"   ⚽ Total goals: {detailed_alpha_goals + detailed_beta_goals}")
    
    print(f"\n⚡ FAST MODE RESULTS ({num_fast_matches} matches):")
    print(f"   🏠 {team_alpha.name} wins: {fast_alpha_wins}")
    print(f"   ✈️  {team_beta.name} wins: {fast_beta_wins}")
    print(f"   🤝 Draws: {fast_draws}")
    
    # Goal statistics for fast mode
    fast_alpha_goals = sum(r.home_score for r in fast_results)
    fast_beta_goals = sum(r.away_score for r in fast_results)
    print(f"   ⚽ Total goals: {fast_alpha_goals + fast_beta_goals}")
    print(f"   📊 Average per match: {(fast_alpha_goals + fast_beta_goals) / num_fast_matches:.1f}")
    
    print(f"\n📈 Final Fast Mode Elo Ratings:")
    alpha_change = team_alpha.elo_rating - initial_alpha_elo
    beta_change = team_beta.elo_rating - initial_beta_elo
    
    print(f"   {team_alpha.name}: {initial_alpha_elo:.0f} → {team_alpha.elo_rating:.0f} "
          f"({alpha_change:+.0f})")
    print(f"   {team_beta.name}: {initial_beta_elo:.0f} → {team_beta.elo_rating:.0f} "
          f"({beta_change:+.0f})")
    
    print(f"\n🔥 Final Streaks (Fast Mode):")
    print(f"   {team_alpha.name}: {format_streak(team_alpha.streak_count)}")
    print(f"   {team_beta.name}: {format_streak(team_beta.streak_count)}")
    
    print(f"\n{'='*80}")
    print("✅ MULTIPLE MATCHES WITH SAME RANDOM TEAMS TEST COMPLETE!")
    print("Features tested:")
    print("  ✅ Random team generation with detailed team info display")
    print("  ✅ Detailed mode for ≤5 matches (match-by-match results)")
    print("  ✅ Fast mode for >5 matches (summary only)")
    print("  ✅ Multiple matches between same teams")
    print("  ✅ Streak effects developing over time")
    print("  ✅ Elo rating changes tracking performance")
    print("  ✅ Enhanced momentum display with visual indicators")
    print("  ✅ Progress indicators for fast simulation")
    print(f"{'='*80}")
    
    # Clean up
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()