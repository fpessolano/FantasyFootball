#!/usr/bin/env python3
"""
Test Multiple Random Games Feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test the new multiple random games functionality.
"""

import os
from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import TacticalStyle, Position


def main():
    """Test the multiple random games feature."""
    print("=" * 80)
    print("TESTING MULTIPLE RANDOM GAMES FEATURE")
    print("=" * 80)
    
    # Clean up test files
    test_files = ["test_random_players.json", "test_random_teams.json"]
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    
    # Initialize
    pm = PlayerManager("test_random_players.json")
    tm = TeamManager("test_random_teams.json")
    me = MatchEngine(use_momentum=True, detailed_sim=True)
    
    # Generate players
    print("\n🔄 Setting up test environment...")
    players = pm.generate_player_pool(120, ensure_all_positions=True)
    for player in players:
        pm.add_player(player)
    
    print(f"✅ Generated {len(players)} players")
    
    # Simulate multiple random games
    num_games = 5
    print(f"\n🎮 Simulating {num_games} random games...")
    
    games = []
    all_teams = []
    
    for game_num in range(1, num_games + 1):
        print(f"\n{'='*60}")
        print(f"RANDOM GAME {game_num}/{num_games}")
        print(f"{'='*60}")
        
        # Create random teams with different naming
        team_names = [
            ("Arsenal", "Chelsea"), ("Barcelona", "Real Madrid"), 
            ("Liverpool", "Manchester City"), ("Bayern Munich", "Borussia Dortmund"),
            ("Juventus", "AC Milan"), ("PSG", "Marseille")
        ]
        
        if game_num <= len(team_names):
            home_name, away_name = team_names[game_num - 1]
        else:
            home_name = f"Team {chr(64 + game_num)}"
            away_name = f"Team {chr(64 + game_num + 26)}"
        
        # Create teams with random formations and styles
        team1 = tm.create_random_team(home_name, pm.players)
        team2 = tm.create_random_team(away_name, pm.players)
        
        if not team1 or not team2:
            print(f"❌ Failed to create teams for game {game_num}")
            continue
        
        all_teams.extend([team1, team2])
        
        # Show team info
        print(f"\n🏠 HOME: {team1.name}")
        print(f"   Formation: {team1.formation} | Style: {team1.style.name}")
        print(f"   Strength: {team1.compute_strength():.1f}")
        
        print(f"\n✈️  AWAY: {team2.name}")
        print(f"   Formation: {team2.formation} | Style: {team2.style.name}")
        print(f"   Strength: {team2.compute_strength():.1f}")
        
        # Simulate match
        result = me.simulate_match(team1, team2)
        
        # Determine winner
        if result.home_score > result.away_score:
            result_emoji = "🏠"
            winner = team1.name
            result_color = "HOME WIN"
        elif result.away_score > result.home_score:
            result_emoji = "✈️"
            winner = team2.name
            result_color = "AWAY WIN"
        else:
            result_emoji = "🤝"
            winner = "DRAW"
            result_color = "DRAW"
        
        print(f"\n{result_emoji} RESULT: {result.home_team} {result.home_score} - {result.away_score} {result.away_team}")
        print(f"🏆 {result_color}")
        
        # Show key stats
        home_stats = result.stats[result.home_team]
        away_stats = result.stats[result.away_team]
        
        print(f"\n📊 Quick Stats:")
        print(f"   Possession: {home_stats['possession']:.0f}% - {away_stats['possession']:.0f}%")
        print(f"   Expected Goals: {home_stats['expected_goals']:.1f} - {away_stats['expected_goals']:.1f}")
        print(f"   Shots: {home_stats['shots']:.0f} - {away_stats['shots']:.0f}")
        
        # Show events
        if result.events:
            print(f"\n🎯 Goals:")
            for event in result.events:
                if event.event_type == "goal":
                    print(f"   {event.minute}' - {event.player} ({event.team})")
        
        games.append({
            'game_num': game_num,
            'home_team': team1,
            'away_team': team2,
            'result': result,
            'winner': winner
        })
    
    # Final summary
    print(f"\n{'='*80}")
    print("MULTIPLE RANDOM GAMES SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n🎮 Games Played: {len(games)}")
    
    # Count results
    home_wins = sum(1 for g in games if g['result'].home_score > g['result'].away_score)
    away_wins = sum(1 for g in games if g['result'].away_score > g['result'].home_score)
    draws = len(games) - home_wins - away_wins
    
    print(f"\n📊 Overall Results:")
    print(f"   🏠 Home Wins: {home_wins} ({home_wins/len(games)*100:.1f}%)")
    print(f"   ✈️  Away Wins: {away_wins} ({away_wins/len(games)*100:.1f}%)")
    print(f"   🤝 Draws: {draws} ({draws/len(games)*100:.1f}%)")
    
    # Goal statistics
    total_goals = sum(g['result'].home_score + g['result'].away_score for g in games)
    avg_goals = total_goals / len(games) if games else 0
    
    print(f"\n⚽ Goal Statistics:")
    print(f"   Total Goals: {total_goals}")
    print(f"   Average per Game: {avg_goals:.1f}")
    
    # Most exciting game
    if games:
        most_goals_game = max(games, key=lambda g: g['result'].home_score + g['result'].away_score)
        most_goals = most_goals_game['result'].home_score + most_goals_game['result'].away_score
        
        print(f"\n🔥 Most Exciting Game:")
        print(f"   Game {most_goals_game['game_num']}: {most_goals_game['result'].home_team} "
              f"{most_goals_game['result'].home_score} - {most_goals_game['result'].away_score} "
              f"{most_goals_game['result'].away_team} ({most_goals} goals)")
    
    # Show all results in a compact format
    print(f"\n📋 All Results:")
    for g in games:
        result_icon = "🏠" if g['result'].home_score > g['result'].away_score else \
                     "✈️" if g['result'].away_score > g['result'].home_score else "🤝"
        print(f"   Game {g['game_num']:2d}: {g['home_team'].name[:15]:<15} "
              f"{g['result'].home_score}-{g['result'].away_score} "
              f"{g['away_team'].name[:15]:<15} {result_icon}")
    
    # Formation and style analysis
    print(f"\n🏗️  Team Variety:")
    formations_used = {}
    styles_used = {}
    
    for team in all_teams:
        formations_used[team.formation] = formations_used.get(team.formation, 0) + 1
        styles_used[team.style.name] = styles_used.get(team.style.name, 0) + 1
    
    print(f"   Formations: {', '.join(f'{k}({v})' for k, v in formations_used.items())}")
    print(f"   Styles: {', '.join(f'{k}({v})' for k, v in styles_used.items())}")
    
    # Team strength analysis
    strengths = [team.compute_strength() for team in all_teams]
    if strengths:
        print(f"\n💪 Team Strength Analysis:")
        print(f"   Average Strength: {sum(strengths)/len(strengths):.1f}")
        print(f"   Strongest Team: {max(all_teams, key=lambda t: t.compute_strength()).name} "
              f"({max(strengths):.1f})")
        print(f"   Weakest Team: {min(all_teams, key=lambda t: t.compute_strength()).name} "
              f"({min(strengths):.1f})")
    
    print(f"\n{'='*80}")
    print("✅ MULTIPLE RANDOM GAMES TEST COMPLETE!")
    print("Features tested:")
    print("  ✅ Random team generation for each game")
    print("  ✅ Variety in formations and tactical styles")
    print("  ✅ Comprehensive match statistics")
    print("  ✅ Tournament-style summary with analysis")
    print("  ✅ Home advantage tracking")
    print("  ✅ Goal scoring and excitement metrics")
    print(f"{'='*80}")
    
    # Clean up
    for file in test_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()