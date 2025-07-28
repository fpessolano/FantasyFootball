#!/usr/bin/env python3
"""
Fantasy Football Demo
~~~~~~~~~~~~~~~~~~~~

Demonstrates the Fantasy Football system capabilities.
"""

from player_manager import PlayerManager
from team_manager import TeamManager
from match_engine import MatchEngine
from models import Position, TacticalStyle


def main():
    """Run a complete demo of the Fantasy Football system."""
    print("="*60)
    print("FANTASY FOOTBALL MANAGER v2.0 - DEMO")
    print("="*60)
    
    # Initialize managers
    pm = PlayerManager("demo_players.json")
    tm = TeamManager("demo_teams.json")
    me = MatchEngine()
    
    # Generate players if needed
    if len(pm.players) < 100:
        print("\n🔄 Generating player pool...")
        players = pm.generate_player_pool(100, ensure_all_positions=True)
        for player in players:
            pm.add_player(player)
        print(f"✅ Generated {len(players)} players")
    
    # Create teams
    print("\n🏗️  Creating teams...")
    
    # Team 1: Barcelona (4-3-3 Attacking)
    barcelona_players = []
    formations = {"4-3-3": {
        Position.GK: 1, Position.CB: 2, Position.LB: 1, Position.RB: 1,
        Position.CM: 3, Position.LW: 1, Position.RW: 1, Position.ST: 1
    }}
    
    # Find best players for Barcelona
    available = pm.players.copy()
    req = formations["4-3-3"]
    
    for pos, count in req.items():
        candidates = [p for p in available if p.position == pos]
        candidates.sort(key=lambda p: p.overall_rating(), reverse=True)
        for i in range(min(count, len(candidates))):
            barcelona_players.append(candidates[i])
            available.remove(candidates[i])
    
    barcelona = tm.create_random_team("FC Barcelona", pm.players, "4-3-3", TacticalStyle.ATTACKING)
    real_madrid = tm.create_random_team("Real Madrid", pm.players, "4-2-3-1", TacticalStyle.BALANCED)
    
    if barcelona and real_madrid:
        tm.add_team(barcelona)
        tm.add_team(real_madrid)
        
        print(f"✅ Created {barcelona.name} ({barcelona.formation}, {barcelona.style.name})")
        print(f"✅ Created {real_madrid.name} ({real_madrid.formation}, {real_madrid.style.name})")
    else:
        print("❌ Failed to create teams")
        return
    
    # Display team summaries
    print(barcelona.summary())
    print(real_madrid.summary())
    
    # Simulate El Clásico
    print("\n⚽ EL CLÁSICO - Barcelona vs Real Madrid")
    print("="*60)
    
    result = me.simulate_match(barcelona, real_madrid)
    me.display_match_result(result)
    
    # Update Elo
    tm.update_team_elo(barcelona.name, real_madrid.name, 
                      (result.home_score, result.away_score))
    
    # Simulate a mini-tournament
    print("\n🏆 MINI TOURNAMENT (5 matches)")
    print("="*60)
    
    results = []
    for i in range(5):
        print(f"\nMatch {i+1}:")
        if i % 2 == 0:
            home, away = barcelona, real_madrid
        else:
            home, away = real_madrid, barcelona
        
        result = me.simulate_match(home, away)
        results.append(result)
        
        print(f"{result.home_team} {result.home_score} - {result.away_score} {result.away_team}")
        
        # Update Elo
        tm.update_team_elo(result.home_team, result.away_team, 
                          (result.home_score, result.away_score))
    
    # Final standings
    print("\n📊 FINAL STANDINGS")
    print("="*60)
    
    bcn_wins = sum(1 for r in results if 
                   (r.home_team == barcelona.name and r.home_score > r.away_score) or
                   (r.away_team == barcelona.name and r.away_score > r.home_score))
    
    rm_wins = sum(1 for r in results if 
                  (r.home_team == real_madrid.name and r.home_score > r.away_score) or
                  (r.away_team == real_madrid.name and r.away_score > r.home_score))
    
    draws = len(results) - bcn_wins - rm_wins
    
    print(f"Barcelona: {bcn_wins} wins, {draws} draws, {rm_wins} losses")
    print(f"Real Madrid: {rm_wins} wins, {draws} draws, {bcn_wins} losses")
    print(f"\nFinal Elo Ratings:")
    print(f"Barcelona: {barcelona.elo_rating:.0f}")
    print(f"Real Madrid: {real_madrid.elo_rating:.0f}")
    
    # Show top players
    print(f"\n⭐ TOP 10 PLAYERS IN DATABASE")
    print("="*60)
    top_players = pm.get_top_players(10)
    
    for i, player in enumerate(top_players, 1):
        print(f"{i:2d}. {player.name:<20} {player.position.name:<4} "
              f"OVR: {player.overall_rating():.0f}")
    
    print("\n" + "="*60)
    print("DEMO COMPLETE! 🎉")
    print("Try running 'python fantasy_football.py' for the full experience!")
    print("="*60)


if __name__ == "__main__":
    main()