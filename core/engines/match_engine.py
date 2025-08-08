"""
Match Engine - Enhanced
~~~~~~~~~~~~~~~~~~~~~~~

Enhanced match engine with fatigue, form, and performance tracking.
"""

import random
import math
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from core.models import Team, Player, Position, TacticalStyle
from core.engines.performance_system import PlayerPerformanceManager
from core.engines.statistics_engine import PlayerStatisticsManager


@dataclass
class MatchEvent:
    """Represents an event during a match."""
    minute: int
    event_type: str  # "goal", "yellow_card", "red_card", "substitution", "match_abandoned"
    team: str
    player: str
    description: str


@dataclass
class MatchResult:
    """Complete match result with enhanced statistics."""
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    events: List[MatchEvent]
    stats: Dict[str, Dict[str, float]]  # Team -> stat type -> value
    date: datetime
    # Enhanced stats
    fatigue_impact: Dict[str, float]  # Team -> average fatigue impact
    momentum_changes: List[Tuple[int, str, float]]  # (minute, team, momentum_change)
    # Player lists for statistics tracking
    home_team_players: List[str] = field(default_factory=list)
    away_team_players: List[str] = field(default_factory=list)


class MatchEngine:
    """Enhanced match engine with performance tracking."""
    
    def __init__(self, use_momentum: bool = True):
        self.use_momentum = use_momentum
        self.show_penalty_details = True  # Toggle for penalty shootout event details
        self.show_detailed_stats = True  # Toggle for detailed statistics table only
        self.performance_manager = PlayerPerformanceManager()
        self.stats_manager = PlayerStatisticsManager()
        self.settings_file = Path("data/settings.json")
        self.load_settings()
    
    def update_player_statistics(self, match_result: MatchResult, tournament: str = None):
        """Update player statistics based on match result."""
        # Update stats for all players who participated
        all_players = []
        
        # Collect home team players
        from core.managers.player_manager import PlayerManager
        temp_pm = PlayerManager('data/players.json')
        
        for player_name in match_result.home_team_players:
            player = next((p for p in temp_pm.players if p.name == player_name), None)
            if player:
                all_players.append((player, 'home'))
        
        for player_name in match_result.away_team_players:
            player = next((p for p in temp_pm.players if p.name == player_name), None)
            if player:
                all_players.append((player, 'away'))
        
        # Update basic match stats for all players
        for player, team_type in all_players:
            stats_update = {
                'matches': 1,
                'minutes': 90  # Simplified - assume all players played full match
            }
            
            # Count goals and assists from events
            goals = 0
            assists = 0
            yellow_cards = 0
            red_cards = 0
            
            for event in match_result.events:
                if event.player == player.name:
                    if event.event_type == 'goal':
                        goals += 1
                    elif event.event_type == 'yellow_card':
                        yellow_cards += 1
                    elif event.event_type == 'red_card':
                        red_cards += 1
            
            # Add event-based stats
            if goals > 0:
                stats_update['goals'] = goals
            if assists > 0:
                stats_update['assists'] = assists
            if yellow_cards > 0:
                stats_update['yellow_cards'] = yellow_cards
            if red_cards > 0:
                stats_update['red_cards'] = red_cards
            
            # Check for clean sheet (goalkeepers only)
            if player.position.name == 'GK':
                opponent_goals = match_result.away_score if team_type == 'home' else match_result.home_score
                if opponent_goals == 0:
                    stats_update['clean_sheets'] = 1
            
            # Add some estimated advanced stats based on position and performance
            if player.position.name == 'GK':
                # Estimate saves based on opponent shots
                estimated_saves = random.randint(2, 8)
                stats_update['saves'] = estimated_saves
            else:
                # Estimate passes based on position
                if player.position.name in ['CM', 'DM', 'AM']:
                    estimated_passes = random.randint(40, 80)
                    estimated_completed = int(estimated_passes * random.uniform(0.75, 0.95))
                else:
                    estimated_passes = random.randint(20, 50)
                    estimated_completed = int(estimated_passes * random.uniform(0.70, 0.90))
                
                stats_update['passes'] = estimated_passes
                stats_update['passes_completed'] = estimated_completed
                
                # Estimate shots for attacking players
                if player.position.name in ['ST', 'LW', 'RW', 'AM']:
                    if goals > 0:
                        estimated_shots = goals + random.randint(1, 4)
                        estimated_on_target = goals + random.randint(0, 2)
                    else:
                        estimated_shots = random.randint(0, 3)
                        estimated_on_target = random.randint(0, estimated_shots)
                    
                    if estimated_shots > 0:
                        stats_update['shots'] = estimated_shots
                        stats_update['shots_on_target'] = estimated_on_target
            
            # Update the player's statistics
            self.stats_manager.update_match_stats(player, stats_update, tournament)
        
        # Save updated player data back to file
        temp_pm.save_players()
    
    def simulate_match(self, home_team: Team, away_team: Team, 
                      match_importance: str = "normal", tournament: str = None) -> MatchResult:
        """Simulate a match with enhanced performance tracking."""
        
        # Reset players for new match
        home_team.reset_players_for_match()
        away_team.reset_players_for_match()
        
        # Initialize match state
        match_time = 0
        home_score = 0
        away_score = 0
        match_events = []
        momentum_changes = []
        
        # Determine if high-pressure situation
        pressure_situation = None
        if match_importance in ["cup_final", "derby", "important_match"]:
            pressure_situation = match_importance
        
        # Track fatigue progression
        home_fatigue_progression = []
        away_fatigue_progression = []
        
        # Simulate match in detailed intervals
        for interval in range(6):  # 6 x 15 = 90 minutes
            interval_start = interval * 15
            interval_end = min((interval + 1) * 15, 90)
            
            # Calculate match intensity for this interval
            intensity = self._calculate_match_intensity(interval, home_score, away_score)
            
            # Update player fatigue during interval
            for minute in range(interval_start, interval_end):
                for player in home_team.players + away_team.players:
                    self.performance_manager.process_match_minute(player, intensity, minute + 1)
            
            # Record fatigue levels
            home_avg_stamina = sum(p.current_stamina for p in home_team.players) / len(home_team.players)
            away_avg_stamina = sum(p.current_stamina for p in away_team.players) / len(away_team.players)
            home_fatigue_progression.append(home_avg_stamina)
            away_fatigue_progression.append(away_avg_stamina)
            
            # Calculate team ratings for this interval (with fatigue/form effects)
            home_rating = self._calculate_enhanced_team_rating(
                home_team, "home", interval_end, pressure_situation
            )
            away_rating = self._calculate_enhanced_team_rating(
                away_team, "away", interval_end, pressure_situation
            )
            
            # Simulate interval events
            interval_events = self._simulate_enhanced_interval(
                home_team, away_team, home_rating, away_rating, 
                interval_start, interval_end, intensity
            )
            
            # Process events and update scores/momentum
            for event in interval_events:
                match_events.append(event)
                
                if event.event_type == 'goal':
                    if event.team == home_team.name:
                        home_score += 1
                        scorer = self._find_player_by_name(home_team.players, event.player)
                        if scorer:
                            self.performance_manager.process_match_event("goal_scored", scorer, event.minute)
                            # Update team momentum
                            home_team.update_team_momentum(15)
                            away_team.update_team_momentum(-20)
                            momentum_changes.append((event.minute, home_team.name, 15))
                    else:
                        away_score += 1
                        scorer = self._find_player_by_name(away_team.players, event.player)
                        if scorer:
                            self.performance_manager.process_match_event("goal_scored", scorer, event.minute)
                            # Update team momentum
                            away_team.update_team_momentum(15)
                            home_team.update_team_momentum(-20)
                            momentum_changes.append((event.minute, away_team.name, 15))
                
                # Process other events
                elif event.event_type in ['yellow_card', 'red_card']:
                    team = home_team if event.team == home_team.name else away_team
                    player = self._find_player_by_name(team.players, event.player)
                    if player:
                        # Apply card to player
                        if event.event_type == 'yellow_card':
                            player.yellow_cards += 1
                            # Check for second yellow = red card
                            if player.yellow_cards >= 2:
                                player.is_sent_off = True
                                # Update event description to reflect second yellow
                                event.description = f"{player.name} receives second yellow card and is sent off!"
                                event.event_type = 'red_card'  # Change event type for momentum impact
                                momentum_change = -25  # Use red card momentum penalty
                            else:
                                momentum_change = -8   # Normal yellow card penalty
                        else:  # Direct red card
                            player.is_sent_off = True
                            momentum_change = -25
                        
                        # Check if team has too few players (match abandonment)
                        available_players = len(team.get_available_players())
                        if available_players < 7:
                            # Match abandoned - award 3-0 to opposition
                            opposition_team = away_team if team == home_team else home_team
                            
                            if team == home_team:
                                home_score = 0
                                away_score = 3
                                abandonment_team = home_team.name
                                winner_team = away_team.name
                            else:
                                home_score = 3
                                away_score = 0
                                abandonment_team = away_team.name
                                winner_team = home_team.name
                            
                            # Add abandonment event
                            abandonment_event = MatchEvent(
                                minute=event.minute,
                                event_type="match_abandoned",
                                team=abandonment_team,
                                player="REFEREE",
                                description=f"Match abandoned! {abandonment_team} reduced to {available_players} players. {winner_team} awarded 3-0 victory."
                            )
                            match_events.append(abandonment_event)
                            
                            # Force end of match simulation
                            interval = 6  # Break out of interval loop
                            
                            # Calculate final statistics early
                            final_home_rating = self._calculate_enhanced_team_rating(
                                home_team, "home", event.minute, pressure_situation
                            )
                            final_away_rating = self._calculate_enhanced_team_rating(
                                away_team, "away", event.minute, pressure_situation
                            )
                            
                            # Calculate fatigue impact up to abandonment
                            if home_fatigue_progression:
                                home_fatigue_impact = (100 - home_fatigue_progression[-1]) / 100
                            else:
                                home_fatigue_impact = 0
                            if away_fatigue_progression:
                                away_fatigue_impact = (100 - away_fatigue_progression[-1]) / 100
                            else:
                                away_fatigue_impact = 0
                            
                            # Return abandoned match result immediately
                            match_result = MatchResult(
                                home_team=home_team.name,
                                away_team=away_team.name,
                                home_score=home_score,
                                away_score=away_score,
                                events=match_events,
                                stats=self._calculate_enhanced_match_stats(
                                    home_team, away_team, final_home_rating, final_away_rating,
                                    home_fatigue_progression or [100], away_fatigue_progression or [100]
                                ),
                                date=datetime.now(),
                                fatigue_impact={
                                    home_team.name: home_fatigue_impact,
                                    away_team.name: away_fatigue_impact
                                },
                                momentum_changes=momentum_changes,
                                home_team_players=[p.name for p in home_team.players],
                                away_team_players=[p.name for p in away_team.players]
                            )
                            
                            # Process end-of-match for all players
                            for p in home_team.players + away_team.players:
                                match_rating = self._calculate_match_rating(p, match_events, home_score, away_score)
                                self.performance_manager.end_match_processing(p, match_rating)
                            
                            # Update player statistics
                            self.update_player_statistics(match_result, tournament)
                            
                            return match_result
                        
                        # Process momentum and performance effects
                        self.performance_manager.process_match_event(event.event_type, player, event.minute)
                        team.update_team_momentum(momentum_change)
                        momentum_changes.append((event.minute, team.name, momentum_change))
        
        # Calculate final statistics with fatigue impact
        final_home_rating = self._calculate_enhanced_team_rating(
            home_team, "home", 90, pressure_situation
        )
        final_away_rating = self._calculate_enhanced_team_rating(
            away_team, "away", 90, pressure_situation
        )
        
        # Calculate fatigue impact
        home_fatigue_impact = (100 - home_fatigue_progression[-1]) / 100
        away_fatigue_impact = (100 - away_fatigue_progression[-1]) / 100
        
        match_result = MatchResult(
            home_team=home_team.name,
            away_team=away_team.name,
            home_score=home_score,
            away_score=away_score,
            events=match_events,
            stats=self._calculate_enhanced_match_stats(
                home_team, away_team, final_home_rating, final_away_rating,
                home_fatigue_progression, away_fatigue_progression
            ),
            date=datetime.now(),
            fatigue_impact={
                home_team.name: home_fatigue_impact,
                away_team.name: away_fatigue_impact
            },
            momentum_changes=momentum_changes,
            home_team_players=[p.name for p in home_team.players],
            away_team_players=[p.name for p in away_team.players]
        )
        
        # Process end-of-match for all players
        for player in home_team.players + away_team.players:
            match_rating = self._calculate_match_rating(player, match_events, home_score, away_score)
            self.performance_manager.end_match_processing(player, match_rating)
        
        # Update player statistics
        self.update_player_statistics(match_result, tournament)
        
        return match_result
    
    def _calculate_enhanced_team_rating(self, team: Team, venue: str, 
                                      match_time: float, pressure_situation: str = None) -> float:
        """Calculate team rating with performance system effects."""
        total_rating = 0
        
        # Only consider available players (not sent off)
        available_players = team.get_available_players()
        
        if not available_players:
            return 0  # No players available
        
        for player in available_players:
            # Get effective attributes considering fatigue, form, momentum, pressure
            effective_attrs = self.performance_manager.get_effective_attributes(player, pressure_situation)
            
            # Weight attributes by position
            if player.position == Position.GK:
                player_rating = effective_attrs['goalkeeping'] * 0.8 + effective_attrs['physical'] * 0.2
            elif player.position in [Position.CB, Position.SW, Position.LB, Position.RB]:
                player_rating = (effective_attrs['defending'] * 0.4 + 
                               effective_attrs['passing'] * 0.3 + 
                               effective_attrs['physical'] * 0.3)
            elif player.position in [Position.DM, Position.CM, Position.AM, Position.LM, Position.RM, 
                                   Position.WB, Position.LWB, Position.RWB]:
                player_rating = (effective_attrs['passing'] * 0.4 + 
                               effective_attrs['dribbling'] * 0.3 + 
                               effective_attrs['physical'] * 0.3)
            else:  # ST, LW, RW
                player_rating = (effective_attrs['shooting'] * 0.4 + 
                               effective_attrs['dribbling'] * 0.3 + 
                               effective_attrs['physical'] * 0.3)
            
            total_rating += player_rating
        
        # Calculate base rating per player
        base_rating = total_rating / len(available_players)
        
        # Apply numerical disadvantage penalty
        numerical_penalty = team._get_numerical_disadvantage_penalty(len(available_players))
        base_rating *= numerical_penalty
        
        # Apply home advantage
        if venue == "home":
            base_rating *= 1.1
        
        # Apply team momentum if enabled
        if self.use_momentum:
            momentum_modifier = team.get_team_momentum_modifier()
            base_rating *= momentum_modifier
        
        return base_rating
    
    def _simulate_enhanced_interval(self, home_team: Team, away_team: Team,
                                  home_rating: float, away_rating: float,
                                  start_time: float, end_time: float, 
                                  intensity: float) -> List[MatchEvent]:
        """Simulate events in an interval with enhanced logic."""
        events = []
        
        # Calculate goal probability based on ratings and fatigue
        total_rating = home_rating + away_rating
        if total_rating > 0:
            home_goal_prob = (home_rating / total_rating) * 0.12  # Base 12% chance per interval
            away_goal_prob = (away_rating / total_rating) * 0.12
        else:
            home_goal_prob = away_goal_prob = 0.06
        
        # Adjust for high intensity matches
        intensity_factor = 0.8 + (intensity / 100) * 0.4  # 0.8 to 1.2
        home_goal_prob *= intensity_factor
        away_goal_prob *= intensity_factor
        
        # Check for goals
        if random.random() < home_goal_prob:
            goal_time = start_time + random.uniform(0, end_time - start_time)
            scorer = self._select_likely_scorer(home_team.get_available_players())
            if scorer:
                events.append(MatchEvent(
                    minute=int(goal_time),
                    event_type="goal",
                    team=home_team.name,
                    player=scorer.name,
                    description=f"{scorer.name} scores!"
                ))
        
        if random.random() < away_goal_prob:
            goal_time = start_time + random.uniform(0, end_time - start_time)
            scorer = self._select_likely_scorer(away_team.get_available_players())
            if scorer:
                events.append(MatchEvent(
                    minute=int(goal_time),
                    event_type="goal",
                    team=away_team.name,
                    player=scorer.name,
                    description=f"{scorer.name} scores!"
                ))
        
        # Cards more likely with high intensity and tired players
        card_prob = 0.08 * (intensity / 100) * (1 + (200 - self._get_average_stamina(home_team.players + away_team.players)) / 200)
        
        if random.random() < card_prob:
            team = random.choice([home_team, away_team])
            available_players = team.get_available_players()
            
            if not available_players:
                # No players available to receive cards
                pass
            else:
                # Tired players more likely to get cards
                player_weights = [(p, max(0.1, p.current_stamina / 100)) for p in available_players]
                total_weight = sum(w for _, w in player_weights)
                if total_weight > 0:
                    rand_val = random.uniform(0, total_weight)
                    current_sum = 0
                    selected_player = None
                    for player, weight in player_weights:
                        current_sum += weight
                        if rand_val <= current_sum:
                            selected_player = player
                            break
                    
                    if selected_player:
                        card_type = "red_card" if random.random() < 0.15 else "yellow_card"
                        events.append(MatchEvent(
                            minute=int(start_time + random.uniform(0, end_time - start_time)),
                            event_type=card_type,
                            team=team.name,
                            player=selected_player.name,
                            description=f"{selected_player.name} receives a {card_type.replace('_', ' ')}"
                        ))
        
        return events
    
    def _select_likely_scorer(self, players: List[Player]) -> Optional[Player]:
        """Select a likely scorer based on position and current form."""
        # Weight players by position and effective shooting ability
        candidates = []
        
        for player in players:
            effective_attrs = self.performance_manager.get_effective_attributes(player)
            
            # Position-based scoring likelihood
            match player.position:
                case pos if pos in [Position.ST]:
                    weight = 4.0
                case pos if pos in [Position.LW, Position.RW, Position.AM]:
                    weight = 2.5
                case pos if pos in [Position.CM, Position.LM, Position.RM]:
                    weight = 1.5
                case pos if pos in [Position.DM, Position.LB, Position.RB, Position.LWB, Position.RWB, Position.WB]:
                    weight = 0.8
                case pos if pos in [Position.CB, Position.SW]:
                    weight = 0.5
                case _:  # GK
                    weight = 0.1
            
            # Adjust by effective shooting ability and form
            shooting_factor = effective_attrs['shooting'] / 100
            weight *= shooting_factor
            
            candidates.append((player, weight))
        
        # Select based on weighted probability
        total_weight = sum(w for _, w in candidates)
        if total_weight == 0:
            return random.choice(players) if players else None
        
        rand_val = random.uniform(0, total_weight)
        current_sum = 0
        
        for player, weight in candidates:
            current_sum += weight
            if rand_val <= current_sum:
                return player
        
        return candidates[-1][0] if candidates else None
    
    def _calculate_match_intensity(self, interval: int, home_score: int, away_score: int) -> float:
        """Calculate match intensity based on time and score."""
        base_intensity = 60  # Base intensity
        
        # Higher intensity in later intervals
        time_factor = 1 + (interval / 6) * 0.4  # Up to 40% increase
        
        # Higher intensity when score is close
        score_diff = abs(home_score - away_score)
        if score_diff == 0:
            score_factor = 1.3  # Tied game = high intensity
        elif score_diff == 1:
            score_factor = 1.1  # Close game = slightly higher
        else:
            score_factor = 0.9  # Blowout = lower intensity
        
        return min(100, base_intensity * time_factor * score_factor)
    
    def _calculate_enhanced_match_stats(self, home_team: Team, away_team: Team,
                                      home_rating: float, away_rating: float,
                                      home_fatigue_prog: List[float], 
                                      away_fatigue_prog: List[float]) -> Dict[str, Dict[str, float]]:
        """Calculate comprehensive match statistics."""
        
        # Basic team ratings
        home_ratings = home_team.compute_team_ratings()
        away_ratings = away_team.compute_team_ratings()
        
        # Calculate possession based on midfield strength and fatigue
        total_mid = home_ratings["midfield"] + away_ratings["midfield"]
        base_home_possession = (home_ratings["midfield"] / total_mid * 100) if total_mid > 0 else 50
        
        # Adjust for fatigue - tired teams lose possession
        avg_home_fatigue = sum(home_fatigue_prog) / len(home_fatigue_prog)
        avg_away_fatigue = sum(away_fatigue_prog) / len(away_fatigue_prog)
        
        fatigue_diff = (avg_home_fatigue - avg_away_fatigue) / 100 * 10  # Max 10% swing
        home_possession = max(25, min(75, base_home_possession + fatigue_diff))
        
        # Calculate shots based on attack ratings and fatigue
        home_shots = 8 + (home_rating - away_rating) / 8
        away_shots = 8 + (away_rating - home_rating) / 8
        
        # Ensure positive values
        home_shots = max(3, home_shots)
        away_shots = max(3, away_shots)
        
        # Calculate expected goals based on team ratings and shots
        total_rating = home_rating + away_rating
        if total_rating > 0:
            home_expected_goals = (home_rating / total_rating) * 2.5  # Base expectation
            away_expected_goals = (away_rating / total_rating) * 2.5
        else:
            home_expected_goals = away_expected_goals = 1.25
        
        # Adjust expected goals for fatigue
        home_expected_goals *= (avg_home_fatigue / 100)
        away_expected_goals *= (avg_away_fatigue / 100)
        
        # Calculate other stats
        home_pass_accuracy = 70 + (home_ratings["midfield"] / 40) - ((100 - avg_home_fatigue) / 10)
        away_pass_accuracy = 70 + (away_ratings["midfield"] / 40) - ((100 - avg_away_fatigue) / 10)
        
        return {
            home_team.name: {
                "possession": home_possession,
                "shots": home_shots,
                "shots_on_target": home_shots * 0.35,
                "expected_goals": home_expected_goals,
                "pass_accuracy": max(60, home_pass_accuracy),
                "average_stamina": avg_home_fatigue,
                "team_rating": home_rating,
                "momentum": home_team.team_momentum,
                "players_available": len(home_team.get_available_players())
            },
            away_team.name: {
                "possession": 100 - home_possession,
                "shots": away_shots,
                "shots_on_target": away_shots * 0.35,
                "expected_goals": away_expected_goals,
                "pass_accuracy": max(60, away_pass_accuracy),
                "average_stamina": avg_away_fatigue,
                "team_rating": away_rating,
                "momentum": away_team.team_momentum,
                "players_available": len(away_team.get_available_players())
            }
        }
    
    def _calculate_match_rating(self, player: Player, events: List[MatchEvent], 
                              home_score: int, away_score: int) -> float:
        """Calculate player's match rating with enhanced factors."""
        base_rating = 6.5  # Average performance
        
        # Adjust based on events
        for event in events:
            if event.player == player.name:
                if event.event_type == 'goal':
                    base_rating += 1.5
                elif event.event_type == 'yellow_card':
                    base_rating -= 0.5
                elif event.event_type == 'red_card':
                    base_rating -= 2.0
        
        # Adjust based on stamina (tired players get lower ratings)
        stamina_factor = player.current_stamina / 100
        if stamina_factor < 0.3:  # Very tired
            base_rating -= 1.5
        elif stamina_factor < 0.5:  # Quite tired
            base_rating -= 1.0
        elif stamina_factor < 0.7:  # Moderately tired
            base_rating -= 0.5
        
        # Adjust based on temperament and pressure
        if player.temperament.value == "volatile":
            base_rating += random.uniform(-0.5, 0.5)  # More variable performance
        elif player.temperament.value == "consistent":
            base_rating += random.uniform(-0.2, 0.2)  # More stable performance
        
        return max(1.0, min(10.0, base_rating))
    
    def _find_player_by_name(self, players: List[Player], name: str) -> Optional[Player]:
        """Find a player by name in the list."""
        for player in players:
            if player.name == name:
                return player
        return None
    
    def _get_average_stamina(self, players: List[Player]) -> float:
        """Get average stamina of a list of players."""
        if not players:
            return 100.0
        return sum(p.current_stamina for p in players) / len(players)
    
    def display_enhanced_match_result(self, result: MatchResult) -> None:
        """Display match result with enhanced statistics."""
        print("\n" + "="*80)
        print(f"ENHANCED MATCH RESULT: {result.home_team} vs {result.away_team}")
        print(f"Date: {result.date.strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        # Score
        print(f"\nFINAL SCORE: {result.home_team} {result.home_score} - "
              f"{result.away_score} {result.away_team}")
        
        # Events - separate regular match events from penalty events
        regular_events = []
        penalty_events = []
        
        for event in result.events:
            if event.event_type == "penalty":
                penalty_events.append(event)
            else:
                regular_events.append(event)
        
        if regular_events:
            print("\nMATCH EVENTS:")
            for event in regular_events:
                if event.event_type == "goal":
                    emoji = "⚽"
                elif event.event_type == "yellow_card":
                    emoji = "🟨"
                elif event.event_type == "red_card":
                    emoji = "🟥"
                elif event.event_type == "match_abandoned":
                    emoji = "🚫"
                else:
                    emoji = "📝"
                print(f"{event.minute}' {emoji} {event.team} - {event.description}")
        
        if penalty_events and self.show_penalty_details:
            print("\nPENALTY SHOOTOUT EVENTS:")
            for event in penalty_events:
                emoji = "🥅"
                print(f"{event.minute}' {emoji} {event.team} - {event.description}")
        
        # Enhanced Statistics - only show if detailed stats enabled
        if self.show_detailed_stats:
            print("\nENHANCED MATCH STATISTICS:")
            print(f"{'Stat':<25} {result.home_team:<20} {result.away_team:<20}")
            print("-" * 65)
            
            home_stats = result.stats[result.home_team]
            away_stats = result.stats[result.away_team]
            
            # Find the actual teams to get player counts
            home_team = None
            away_team = None
            # Note: This is a limitation - we don't have access to team objects here
            # In a future version, we could pass team objects to the display method
            
            print(f"{'Possession':<25} {home_stats['possession']:<20.1f}% "
                  f"{away_stats['possession']:<20.1f}%")
            print(f"{'Expected Goals':<25} {home_stats['expected_goals']:<20.1f} "
                  f"{away_stats['expected_goals']:<20.1f}")
            print(f"{'Shots':<25} {home_stats['shots']:<20.0f} "
                  f"{away_stats['shots']:<20.0f}")
            print(f"{'Shots on Target':<25} {home_stats['shots_on_target']:<20.0f} "
                  f"{away_stats['shots_on_target']:<20.0f}")
            print(f"{'Pass Accuracy':<25} {home_stats['pass_accuracy']:<20.1f}% "
                  f"{away_stats['pass_accuracy']:<20.1f}%")
            print(f"{'Team Rating':<25} {home_stats['team_rating']:<20.1f} "
                  f"{away_stats['team_rating']:<20.1f}")
            print(f"{'Players Available':<25} {home_stats['players_available']:<20.0f} "
                  f"{away_stats['players_available']:<20.0f}")
            print(f"{'Average Stamina':<25} {home_stats['average_stamina']:<20.1f}% "
                  f"{away_stats['average_stamina']:<20.1f}%")
            print(f"{'Team Momentum':<25} {home_stats['momentum']:<20.1f} "
                  f"{away_stats['momentum']:<20.1f}")
            
            # Fatigue Impact
            print(f"\nFATIGUE IMPACT:")
            for team, impact in result.fatigue_impact.items():
                impact_desc = "High" if impact > 0.3 else "Medium" if impact > 0.15 else "Low"
                print(f"  {team}: {impact:.1%} ({impact_desc})")
            
            # Momentum Changes
            if result.momentum_changes:
                print(f"\nKEY MOMENTUM SHIFTS:")
                for minute, team, change in result.momentum_changes[-3:]:  # Show last 3
                    direction = "↗️" if change > 0 else "↘️"
                    print(f"  {minute}' {direction} {team}: {change:+.0f}")
        
        print("="*80)
    
    # Keep original display method for compatibility
    def display_match_result(self, result: MatchResult) -> None:
        """Display match result (compatibility method)."""
        self.display_enhanced_match_result(result)
    
    def load_settings(self):
        """Load settings from file."""
        try:
            import json
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.show_penalty_details = settings.get('show_penalty_details', True)
                self.show_detailed_stats = settings.get('show_detailed_stats', True)
        except (FileNotFoundError, json.JSONDecodeError):
            # Use defaults if file doesn't exist or is corrupted
            pass
    
    def save_settings(self):
        """Save settings to file."""
        try:
            import json
            settings = {
                'show_penalty_details': self.show_penalty_details,
                'show_detailed_stats': self.show_detailed_stats
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")
