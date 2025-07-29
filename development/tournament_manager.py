"""
Tournament Manager
~~~~~~~~~~~~~~~~~~

Module for creating and managing knockout tournaments in the Fantasy Football system.
"""

import math
import random
from typing import List, Optional, Tuple
from models import Tournament, TournamentRound, TournamentMatch, Team
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
        result = engine.simulate_match(home_team_obj, away_team_obj, "important_match")
        
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
            target_match.winner = self._simulate_penalty_shootout(
                home_team_obj, away_team_obj, target_match
            )
        
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
                                 match: TournamentMatch) -> str:
        """Simulate penalty shootout for drawn matches."""
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
        
        return winner
    
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