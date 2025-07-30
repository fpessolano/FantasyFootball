"""
Tournament Manager
~~~~~~~~~~~~~~~~~~

Module for creating and managing knockout tournaments in the Fantasy Football system.
"""

import math
import random
from typing import List, Optional, Tuple
from models import Tournament, TournamentRound, TournamentMatch, Team, Position
from team_manager import TeamManager
from player_manager import PlayerManager


class TournamentManager:
    """Manages tournament creation and bracket generation."""
    
    def __init__(self, team_manager: TeamManager, player_manager: PlayerManager):
        self.team_manager = team_manager
        self.player_manager = player_manager
    
    def create_tournament(self, name: str, team_names: List[str]) -> Tournament:
        """Create a new knockout tournament with given teams."""
        # Validate team count (must be power of 2)
        if not self._is_power_of_2(len(team_names)):
            # Pad with byes if needed
            team_names = self._pad_teams_for_bracket(team_names)
        
        # Generate bracket structure
        rounds = self._generate_bracket(team_names)
        
        return Tournament(
            name=name,
            teams=team_names.copy(),
            rounds=rounds
        )
    
    def _is_power_of_2(self, n: int) -> bool:
        """Check if a number is a power of 2."""
        return n > 0 and (n & (n - 1)) == 0
    
    def _pad_teams_for_bracket(self, team_names: List[str]) -> List[str]:
        """Pad team list to next power of 2 with byes."""
        if len(team_names) <= 1:
            return team_names
        
        # Find next power of 2
        next_power = 2 ** math.ceil(math.log2(len(team_names)))
        
        # Add byes
        padded_teams = team_names.copy()
        for i in range(len(team_names), next_power):
            padded_teams.append(f"BYE_{i}")
        
        return padded_teams
    
    def _generate_bracket(self, team_names: List[str]) -> List[TournamentRound]:
        """Generate tournament bracket structure."""
        rounds = []
        num_teams = len(team_names)
        
        # Calculate round names
        round_names = self._get_round_names(num_teams)
        
        # Create all rounds structure first
        current_team_count = num_teams
        round_num = 0
        
        while current_team_count > 1:
            matches_in_round = current_team_count // 2
            matches = []
            
            for i in range(matches_in_round):
                match_id = f"R{round_num + 1}M{i + 1}"
                match = TournamentMatch(
                    round_name=round_names[round_num],
                    match_id=match_id,
                    home_team=None,  # Will be filled later
                    away_team=None   # Will be filled later
                )
                matches.append(match)
            
            tournament_round = TournamentRound(
                round_name=round_names[round_num],
                matches=matches
            )
            rounds.append(tournament_round)
            
            current_team_count = matches_in_round
            round_num += 1
        
        # Fill first round with actual teams
        if rounds:
            first_round = rounds[0]
            shuffled_teams = team_names.copy()
            random.shuffle(shuffled_teams)  # Randomize seeding
            
            # Filter out bye teams and assign real teams
            real_teams = [team for team in shuffled_teams if not team.startswith("BYE_")]
            
            match_index = 0
            for i in range(0, len(real_teams), 2):
                if match_index < len(first_round.matches):
                    first_round.matches[match_index].home_team = real_teams[i]
                    if i + 1 < len(real_teams):
                        first_round.matches[match_index].away_team = real_teams[i + 1]
                    match_index += 1
        
        return rounds
    
    def _get_round_names(self, num_teams: int) -> List[str]:
        """Generate round names based on tournament size."""
        num_rounds = int(math.log2(num_teams))
        names = []
        
        for i in range(num_rounds):
            teams_in_round = num_teams // (2 ** i)
            
            if teams_in_round == 2:
                names.append("Final")
            elif teams_in_round == 4:
                names.append("Semi-Final")
            elif teams_in_round == 8:
                names.append("Quarter-Final")
            elif teams_in_round == 16:
                names.append("Round of 16")
            elif teams_in_round == 32:
                names.append("Round of 32")
            else:
                names.append(f"Round {i + 1}")
        
        return names
    
    def simulate_tournament_match(self, tournament: Tournament, match_id: str, 
                                engine) -> Optional[Tuple[TournamentMatch, object]]:
        """Simulate a specific tournament match."""
        current_round = tournament.get_current_round()
        if not current_round:
            return None
        
        # Find the match
        target_match = None
        for match in current_round.matches:
            if match.match_id == match_id:
                target_match = match
                break
        
        if not target_match or target_match.completed:
            return None
        
        # Get team objects
        home_team_obj = self.team_manager.find_team_by_name(target_match.home_team)
        away_team_obj = self.team_manager.find_team_by_name(target_match.away_team)
        
        if not home_team_obj or not away_team_obj:
            return None
        
        # Simulate the match
        result = engine.simulate_match(home_team_obj, away_team_obj, "important_match", tournament.name)
        
        # Update match with results
        target_match.home_score = result.home_score
        target_match.away_score = result.away_score
        target_match.completed = True
        
        # Determine winner
        if result.home_score > result.away_score:
            target_match.winner = target_match.home_team
        elif result.away_score > result.home_score:
            target_match.winner = target_match.away_team
        else:
            # Handle draws in knockout - simulate penalty shootout
            penalty_result = self._simulate_penalty_shootout(
                home_team_obj, away_team_obj, target_match
            )
            target_match.winner = penalty_result[0]
            # Add penalty events to the match result
            if len(penalty_result) > 1 and penalty_result[1]:
                penalty_events = penalty_result[1]
                # Convert penalty events to MatchEvent objects and add to result
                from match_engine import MatchEvent
                for penalty_event in penalty_events:
                    result.events.append(MatchEvent(
                        minute=penalty_event["minute"],
                        event_type=penalty_event["event_type"],
                        team=penalty_event["team"],
                        player=penalty_event["player"],
                        description=penalty_event["description"]
                    ))
        
        # Update Elo ratings
        self.team_manager.update_team_elo(
            target_match.home_team, target_match.away_team,
            (result.home_score, result.away_score)
        )
        
        # Check if round is completed
        if all(match.completed for match in current_round.matches):
            current_round.completed = True
            self._setup_next_round(tournament)
        
        return (target_match, result)
    
    def _simulate_penalty_shootout(self, home_team: Team, away_team: Team, 
                                 match: TournamentMatch) -> Tuple[str, List]:
        """Enhanced penalty shootout with individual player mechanics."""
        
        # Get penalty takers (best shooters who aren't sent off)
        home_takers = self._select_penalty_takers(home_team)
        away_takers = self._select_penalty_takers(away_team)
        
        # Get goalkeepers
        home_gk = self._get_goalkeeper(home_team)
        away_gk = self._get_goalkeeper(away_team)
        
        if not home_takers or not away_takers or not home_gk or not away_gk:
            # Fallback to simple system if can't find players
            return self._simple_penalty_fallback(home_team, away_team, match)
        
        home_score = away_score = 0
        penalty_events = []
        penalty_round = 1
        
        # Regular 5-penalty phase
        for round_num in range(1, 6):
            # Home team penalty
            home_result = self._simulate_individual_penalty(
                home_takers[(round_num-1) % len(home_takers)], 
                away_gk, 
                "penalty_shootout",
                penalty_round
            )
            
            if home_result["scored"]:
                home_score += 1
            
            penalty_events.append({
                "minute": 90 + round_num,
                "event_type": "penalty",
                "team": home_team.name,
                "player": home_result["taker"],
                "description": home_result["description"]
            })
            
            # Away team penalty  
            away_result = self._simulate_individual_penalty(
                away_takers[(round_num-1) % len(away_takers)],
                home_gk,
                "penalty_shootout", 
                penalty_round
            )
            
            if away_result["scored"]:
                away_score += 1
                
            penalty_events.append({
                "minute": 90 + round_num,
                "event_type": "penalty", 
                "team": away_team.name,
                "player": away_result["taker"],
                "description": away_result["description"]
            })
            
            penalty_round += 1
        
        # Sudden death if tied
        sudden_death_round = 1
        while home_score == away_score:
            # Home penalty
            taker_idx = (4 + sudden_death_round - 1) % len(home_takers)
            home_result = self._simulate_individual_penalty(
                home_takers[taker_idx], away_gk, "sudden_death", sudden_death_round + 5
            )
            
            if home_result["scored"]:
                home_score += 1
                
            penalty_events.append({
                "minute": 90 + 5 + sudden_death_round,
                "event_type": "penalty",
                "team": home_team.name, 
                "player": home_result["taker"],
                "description": f"[Sudden Death] {home_result['description']}"
            })
            
            # Away penalty (only if home scored or to equalize)
            if home_result["scored"] or home_score == away_score:
                taker_idx = (4 + sudden_death_round - 1) % len(away_takers)
                away_result = self._simulate_individual_penalty(
                    away_takers[taker_idx], home_gk, "sudden_death", sudden_death_round + 5
                )
                
                if away_result["scored"]:
                    away_score += 1
                    
                penalty_events.append({
                    "minute": 90 + 5 + sudden_death_round,
                    "event_type": "penalty",
                    "team": away_team.name,
                    "player": away_result["taker"], 
                    "description": f"[Sudden Death] {away_result['description']}"
                })
            
            sudden_death_round += 1
            
            # Safety break
            if sudden_death_round > 10:
                break
        
        # Update match description to show penalty result
        winner = home_team.name if home_score > away_score else away_team.name
        match.home_score = f"{match.home_score} ({home_score})"
        match.away_score = f"{match.away_score} ({away_score})"
        
        return winner, penalty_events
    
    def _select_penalty_takers(self, team: Team) -> List:
        """Select best penalty takers from available players."""
        available = team.get_available_players()
        
        # Sort by penalty-taking ability (shooting + composure + pressure_handling)
        def penalty_skill(player):
            base_skill = player.shooting
            mental_bonus = (getattr(player, 'composure', 70) + getattr(player, 'pressure_handling', 70)) / 200 * 20  # Up to 20 point bonus
            return base_skill + mental_bonus
        
        sorted_takers = sorted(available, key=penalty_skill, reverse=True)
        return sorted_takers[:10]  # Top 10 potential takers

    def _simulate_individual_penalty(self, taker, goalkeeper, situation: str, round_num: int) -> dict:
        """Simulate individual penalty with detailed outcomes."""
        
        # Calculate penalty skill vs goalkeeper skill
        penalty_skill = (taker.shooting * 0.6 + 
                        taker.physical * 0.2 +  # For power
                        (getattr(taker, 'composure', 70) + getattr(taker, 'pressure_handling', 70)) / 2 * 0.2)
        
        gk_skill = (goalkeeper.goalkeeping * 0.7 +
                   getattr(goalkeeper, 'concentration', 70) * 0.15 +
                   getattr(goalkeeper, 'pressure_handling', 70) * 0.15)
        
        # Base success rate influenced by skill difference
        base_success = 0.75  # 75% base rate
        skill_modifier = (penalty_skill - gk_skill) / 100 * 0.3  # ±30% based on skill difference
        final_success_rate = max(0.4, min(0.95, base_success + skill_modifier))
        
        # Pressure increases with round number and situation
        pressure_factor = 1.0
        if situation == "sudden_death":
            pressure_factor = 1.3
        elif round_num >= 4:  # Late in regular penalties
            pressure_factor = 1.1
        
        # Apply pressure to success rate
        pressure_adjusted_rate = final_success_rate / pressure_factor
        
        # Determine outcome
        roll = random.random()
        
        if roll < pressure_adjusted_rate:
            # Goal!
            return {
                "scored": True,
                "taker": taker.name,
                "description": f"{taker.name} scores! ({goalkeeper.name} dives the wrong way)"
            }
        else:
            # Miss or save - determine which
            miss_vs_save_threshold = gk_skill / (gk_skill + penalty_skill)
            
            if random.random() < miss_vs_save_threshold:
                # Goalkeeper save
                save_descriptions = [
                    f"{goalkeeper.name} makes a brilliant save!",
                    f"{goalkeeper.name} guesses correctly and saves!",
                    f"{goalkeeper.name} tips it over the bar!",
                    f"{goalkeeper.name} dives and pushes it wide!"
                ]
                return {
                    "scored": False,
                    "taker": taker.name,
                    "description": f"{taker.name} penalty: {random.choice(save_descriptions)}"
                }
            else:
                # Penalty miss
                miss_descriptions = [
                    f"{taker.name} blazes it over the bar!",
                    f"{taker.name} hits the post!",
                    f"{taker.name} shoots wide!",
                    f"{taker.name} scuffs the penalty!"
                ]
                return {
                    "scored": False, 
                    "taker": taker.name,
                    "description": random.choice(miss_descriptions)
                }

    def _get_goalkeeper(self, team: Team):
        """Get the team's goalkeeper."""
        available = team.get_available_players()
        for player in available:
            if player.position == Position.GK:
                return player
        return None

    def _simple_penalty_fallback(self, home_team: Team, away_team: Team, match) -> Tuple[str, List]:
        """Fallback to simple penalty system if enhanced system fails."""
        # Simple penalty simulation based on team shooting ability
        home_shooting = sum(p.shooting for p in home_team.players) / len(home_team.players)
        away_shooting = sum(p.shooting for p in away_team.players) / len(away_team.players)
        
        home_penalties = 0
        away_penalties = 0
        
        # Simulate 5 penalties each
        for i in range(5):
            # Home team penalty
            if random.random() < (home_shooting / 100) * 0.75:  # 75% base success rate
                home_penalties += 1
            
            # Away team penalty
            if random.random() < (away_shooting / 100) * 0.75:
                away_penalties += 1
        
        # If still tied, sudden death
        while home_penalties == away_penalties:
            if random.random() < (home_shooting / 100) * 0.75:
                home_penalties += 1
            if random.random() < (away_shooting / 100) * 0.75:
                away_penalties += 1
        
        # Update match description to show penalty result
        winner = home_team.name if home_penalties > away_penalties else away_team.name
        match.home_score = f"{match.home_score} ({home_penalties})"
        match.away_score = f"{match.away_score} ({away_penalties})"
        
        return winner, []
    
    def _setup_next_round(self, tournament: Tournament):
        """Set up the next round with winners from current round."""
        current_round = tournament.get_current_round()
        if not current_round or not current_round.completed:
            return
        
        # Get winners
        winners = [match.winner for match in current_round.matches if match.winner]
        
        if len(winners) <= 1:
            tournament.completed = True
            if winners:
                tournament.winner = winners[0]
            return
        
        # Advance to next round
        if tournament.advance_round():
            next_round = tournament.get_current_round()
            if next_round:
                # Pair up winners for next round
                match_index = 0
                for i in range(0, len(winners), 2):
                    if match_index < len(next_round.matches):
                        next_round.matches[match_index].home_team = winners[i]
                        if i + 1 < len(winners):
                            next_round.matches[match_index].away_team = winners[i + 1]
                        match_index += 1
    
    def _generate_match_preview(self, home_team_name: str, away_team_name: str) -> str:
        """Generate a descriptive match preview phrase based on team stats."""
        home_team = self.team_manager.find_team_by_name(home_team_name)
        away_team = self.team_manager.find_team_by_name(away_team_name)
        
        if not home_team or not away_team:
            return f"{home_team_name} vs {away_team_name}"
        
        # Calculate strength difference
        elo_diff = abs(home_team.elo_rating - away_team.elo_rating)
        strength_diff = abs(home_team.compute_strength() - away_team.compute_strength())
        
        # Determine stronger team
        if home_team.elo_rating > away_team.elo_rating:
            stronger_team, weaker_team = home_team, away_team
        elif away_team.elo_rating > home_team.elo_rating:
            stronger_team, weaker_team = away_team, home_team
        else:
            stronger_team = weaker_team = None
        
        # Consider streaks (hot/cold streaks affect perception)
        home_hot_streak = home_team.streak_count >= 3
        away_hot_streak = away_team.streak_count >= 3
        home_cold_streak = home_team.streak_count <= -3
        away_cold_streak = away_team.streak_count <= -3
        
        # Generate preview based on various factors
        if elo_diff < 50 and strength_diff < 5:
            if home_hot_streak and not away_hot_streak:
                return f"{home_team.name} riding momentum vs {away_team.name}"
            elif away_hot_streak and not home_hot_streak:
                return f"{away_team.name} on fire vs {home_team.name}"
            elif home_hot_streak and away_hot_streak:
                return f"Clash of titans: {home_team.name} vs {away_team.name}"
            else:
                return f"Evenly matched contest: {home_team.name} vs {away_team.name}"
        
        elif elo_diff < 100 and strength_diff < 10:
            if stronger_team == home_team:
                if home_cold_streak:
                    return f"Struggling {home_team.name} face {away_team.name}"
                elif away_hot_streak:
                    return f"{home_team.name} vs red-hot {away_team.name}"
                else:
                    return f"{home_team.name} slight favourites vs {away_team.name}"
            else:
                if away_cold_streak:
                    return f"{home_team.name} vs out-of-form {away_team.name}"
                elif home_hot_streak:
                    return f"In-form {home_team.name} vs {away_team.name}"
                else:
                    return f"{home_team.name} vs favoured {away_team.name}"
        
        elif elo_diff < 200:
            if stronger_team == home_team:
                if away_hot_streak:
                    return f"{home_team.name} vs dangerous {away_team.name}"
                elif home_cold_streak:
                    return f"Underperforming {home_team.name} vs {away_team.name}"
                else:
                    return f"Strong {home_team.name} vs {away_team.name}"
            else:
                if home_hot_streak:
                    return f"Confident {home_team.name} vs {away_team.name}"
                elif away_cold_streak:
                    return f"{home_team.name} vs struggling giants {away_team.name}"
                else:
                    return f"{home_team.name} vs powerful {away_team.name}"
        
        else:  # Large difference (200+ Elo)
            if stronger_team == home_team:
                if away_hot_streak:
                    return f"Giants {home_team.name} vs resilient {away_team.name}"
                elif home_cold_streak:
                    return f"Faltering {home_team.name} vs underdogs {away_team.name}"
                else:
                    return f"Dominant {home_team.name} vs brave {away_team.name}"
            else:
                if home_hot_streak:
                    return f"Giant-killers {home_team.name} vs {away_team.name}"
                elif away_cold_streak:
                    return f"Underdogs {home_team.name} vs wounded {away_team.name}"
                else:
                    return f"David vs Goliath: {home_team.name} vs {away_team.name}"

    def get_tournament_bracket_display(self, tournament: Tournament) -> str:
        """Generate a visual representation of the tournament bracket."""
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"🏆 {tournament.name.upper()} - TOURNAMENT BRACKET")
        lines.append(f"{'='*70}")
        
        if tournament.completed:
            lines.append(f"\n🥇 CHAMPION: {tournament.winner}")
            lines.append(f"🎉 Tournament completed!")
        else:
            current = tournament.get_current_round()
            if current:
                lines.append(f"\n📍 Current Round: {current.round_name}")
                completed_matches = sum(1 for m in current.matches if m.completed)
                total_matches = len(current.matches)
                lines.append(f"⚽ Matches completed: {completed_matches}/{total_matches}")
        
        lines.append("\n")
        
        for i, round_obj in enumerate(tournament.rounds):
            # Round header with better status indicators
            if i == tournament.current_round and not tournament.completed:
                status = "🔥 ACTIVE"
            elif round_obj.completed:
                status = "✅ COMPLETED"
            else:
                status = "⏳ UPCOMING"
            
            lines.append(f"{status} {round_obj.round_name.upper()}")
            lines.append("─" * 50)
            
            for j, match in enumerate(round_obj.matches, 1):
                if match.completed:
                    score_str = f"{match.home_score} - {match.away_score}"
                    if "(" in str(match.home_score):  # Penalty shootout
                        lines.append(f"   {j}. {match.home_team} vs {match.away_team}")
                        lines.append(f"      {score_str} (Penalties)")
                        lines.append(f"      🥅 Winner: {match.winner}")
                    else:
                        lines.append(f"   {j}. {match.home_team} vs {match.away_team}")
                        lines.append(f"      {score_str}")
                        lines.append(f"      🏆 Winner: {match.winner}")
                else:
                    home = match.home_team or "TBD"
                    away = match.away_team or "TBD"
                    if home == "TBD" or away == "TBD":
                        lines.append(f"   {j}. {home} vs {away}")
                    else:
                        lines.append(f"   {j}. {home} vs {away} (⏳ Pending)")
            lines.append("")
        
        return "\n".join(lines)
    
    def create_random_teams_for_tournament(self, count: int, base_name: str = "Team") -> List[Team]:
        """Create random teams for tournament with option to fill rosters."""
        teams = []
        
        # Ensure we have enough players
        if len(self.player_manager.players) < count * 11:
            needed = count * 11 - len(self.player_manager.players)
            new_players = self.player_manager.generate_player_pool(needed + 20)  # Extra buffer
            for player in new_players:
                self.player_manager.add_player(player)
        
        for i in range(count):
            team_name = f"{base_name} {i + 1}"
            team = self.team_manager.create_random_team(
                team_name, self.player_manager.players
            )
            if team:
                teams.append(team)
                self.team_manager.add_team(team)
        
        return teams