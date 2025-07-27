"""
ELO Estimation System for Fantasy Football Manager

This module estimates missing ELO scores using similarity matching with teams that have known ELO scores.
It uses multiple metrics and fallback systems to provide accurate estimates.

Key Features:
- Multi-metric similarity analysis
- Hierarchical fallback system
- League-aware estimation
- Historical data integration
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class TeamMetrics:
    """Container for team performance metrics used in ELO estimation."""
    overall: Optional[float] = None
    attack: Optional[float] = None
    midfield: Optional[float] = None
    defence: Optional[float] = None
    international_prestige: Optional[float] = None
    domestic_prestige: Optional[float] = None
    club_worth_eur: Optional[float] = None
    transfer_budget_eur: Optional[float] = None
    league_level: Optional[int] = None
    team_name: str = ""
    league_name: str = ""
    country: str = ""


class ELOEstimator:
    """Advanced ELO estimation using similarity matching and multiple metrics."""
    
    def __init__(self):
        self.known_teams: Dict[str, Tuple[float, TeamMetrics]] = {}  # team_name -> (elo, metrics)
        self.metric_weights = {
            'overall': 0.35,           # Primary metric
            'attack': 0.15,            # Offensive capability
            'midfield': 0.15,          # Midfield strength
            'defence': 0.15,           # Defensive capability
            'international_prestige': 0.08,  # Global recognition
            'domestic_prestige': 0.07, # National recognition
            'club_worth': 0.03,        # Financial indicator
            'league_level': 0.02       # Competition level
        }
        
    def add_known_team(self, team_name: str, elo: float, metrics: TeamMetrics):
        """Add a team with known ELO and metrics to the reference database."""
        if elo and 1000 <= elo <= 2000:  # Only add valid ELO scores
            self.known_teams[team_name] = (elo, metrics)
    
    def estimate_elo(self, target_metrics: TeamMetrics, league_context: bool = True) -> float:
        """
        Estimate ELO for a team based on similarity to known teams.
        
        Args:
            target_metrics: Metrics for the team needing ELO estimation
            league_context: Whether to prioritize teams from same league/country
            
        Returns:
            float: Estimated ELO score (1000-2000)
        """
        if not self.known_teams:
            return self._get_fallback_elo(target_metrics)
        
        # Try multiple estimation methods in order of preference
        methods = [
            self._estimate_by_overall_similarity,
            self._estimate_by_multi_metric_similarity,
            self._estimate_by_league_context,
            self._estimate_by_prestige_similarity
        ]
        
        for method in methods:
            try:
                estimated_elo = method(target_metrics, league_context)
                if estimated_elo and 1000 <= estimated_elo <= 2000:
                    return estimated_elo
            except Exception:
                continue
        
        # Final fallback
        return self._get_fallback_elo(target_metrics)
    
    def _estimate_by_overall_similarity(self, target_metrics: TeamMetrics, league_context: bool) -> Optional[float]:
        """Estimate ELO based on overall rating similarity."""
        if not target_metrics.overall:
            return None
        
        similar_teams = []
        target_overall = float(target_metrics.overall)
        
        for team_name, (elo, metrics) in self.known_teams.items():
            if not metrics.overall:
                continue
            
            similarity = self._calculate_overall_similarity(target_overall, float(metrics.overall))
            
            # Boost similarity for same league/country if enabled
            if league_context and self._is_same_context(target_metrics, metrics):
                similarity *= 1.2
            
            similar_teams.append((similarity, elo))
        
        if not similar_teams:
            return None
        
        # Use weighted average of most similar teams
        similar_teams.sort(key=lambda x: x[0], reverse=True)
        top_matches = similar_teams[:5]  # Top 5 most similar
        
        total_weight = sum(sim for sim, _ in top_matches)
        if total_weight == 0:
            return None
        
        weighted_elo = sum(sim * elo for sim, elo in top_matches) / total_weight
        return max(1000, min(2000, weighted_elo))
    
    def _estimate_by_multi_metric_similarity(self, target_metrics: TeamMetrics, league_context: bool) -> Optional[float]:
        """Estimate ELO using comprehensive multi-metric similarity."""
        similar_teams = []
        
        for team_name, (elo, metrics) in self.known_teams.items():
            similarity_score = self._calculate_multi_metric_similarity(target_metrics, metrics)
            
            if similarity_score > 0:
                # Boost for same league/country
                if league_context and self._is_same_context(target_metrics, metrics):
                    similarity_score *= 1.15
                
                similar_teams.append((similarity_score, elo))
        
        if not similar_teams:
            return None
        
        # Weight by similarity and use top matches
        similar_teams.sort(key=lambda x: x[0], reverse=True)
        top_matches = similar_teams[:7]  # Top 7 for more stability
        
        total_weight = sum(sim for sim, _ in top_matches)
        if total_weight == 0:
            return None
        
        weighted_elo = sum(sim * elo for sim, elo in top_matches) / total_weight
        return max(1000, min(2000, weighted_elo))
    
    def _estimate_by_league_context(self, target_metrics: TeamMetrics, league_context: bool) -> Optional[float]:
        """Estimate ELO based on league average and position within league."""
        if not league_context or not target_metrics.league_name:
            return None
        
        # Find teams from same league
        league_teams = []
        for team_name, (elo, metrics) in self.known_teams.items():
            if (metrics.league_name == target_metrics.league_name and 
                metrics.country == target_metrics.country):
                league_teams.append((elo, metrics))
        
        if len(league_teams) < 3:  # Need enough sample size
            return None
        
        # Calculate league average
        league_avg_elo = sum(elo for elo, _ in league_teams) / len(league_teams)
        
        # Adjust based on target team's relative strength within league
        if target_metrics.overall:
            league_overall_values = [float(m.overall) for _, m in league_teams if m.overall]
            if league_overall_values:
                league_avg_overall = sum(league_overall_values) / len(league_overall_values)
                relative_strength = float(target_metrics.overall) / league_avg_overall
                
                # Adjust ELO based on relative strength
                adjustment = (relative_strength - 1) * 100  # ±100 ELO adjustment range
                estimated_elo = league_avg_elo + adjustment
                
                return max(1000, min(2000, estimated_elo))
        
        return league_avg_elo
    
    def _estimate_by_prestige_similarity(self, target_metrics: TeamMetrics, league_context: bool) -> Optional[float]:
        """Estimate ELO based on prestige and financial metrics."""
        if (not target_metrics.international_prestige and 
            not target_metrics.domestic_prestige and 
            not target_metrics.club_worth_eur):
            return None
        
        similar_teams = []
        
        for team_name, (elo, metrics) in self.known_teams.items():
            similarity = self._calculate_prestige_similarity(target_metrics, metrics)
            
            if similarity > 0:
                similar_teams.append((similarity, elo))
        
        if not similar_teams:
            return None
        
        # Use weighted average
        similar_teams.sort(key=lambda x: x[0], reverse=True)
        top_matches = similar_teams[:6]
        
        total_weight = sum(sim for sim, _ in top_matches)
        if total_weight == 0:
            return None
        
        weighted_elo = sum(sim * elo for sim, elo in top_matches) / total_weight
        return max(1000, min(2000, weighted_elo))
    
    def _calculate_overall_similarity(self, target: float, reference: float) -> float:
        """Calculate similarity based on overall rating."""
        if target == 0 or reference == 0:
            return 0
        
        difference = abs(target - reference)
        # Exponential decay similarity (closer = much higher similarity)
        similarity = math.exp(-difference / 10)  # Decay factor of 10
        return similarity
    
    def _calculate_multi_metric_similarity(self, target: TeamMetrics, reference: TeamMetrics) -> float:
        """Calculate comprehensive similarity using multiple metrics."""
        total_similarity = 0
        total_weight = 0
        
        metric_pairs = [
            ('overall', target.overall, reference.overall, self.metric_weights['overall']),
            ('attack', target.attack, reference.attack, self.metric_weights['attack']),
            ('midfield', target.midfield, reference.midfield, self.metric_weights['midfield']),
            ('defence', target.defence, reference.defence, self.metric_weights['defence']),
            ('international_prestige', target.international_prestige, reference.international_prestige, self.metric_weights['international_prestige']),
            ('domestic_prestige', target.domestic_prestige, reference.domestic_prestige, self.metric_weights['domestic_prestige'])
        ]
        
        for metric_name, target_val, ref_val, weight in metric_pairs:
            if target_val is not None and ref_val is not None:
                try:
                    target_float = float(target_val)
                    ref_float = float(ref_val)
                    
                    if target_float > 0 and ref_float > 0:
                        difference = abs(target_float - ref_float)
                        # Scale difference based on metric type
                        scale_factor = 15 if metric_name in ['overall', 'attack', 'midfield', 'defence'] else 5
                        similarity = math.exp(-difference / scale_factor)
                        
                        total_similarity += similarity * weight
                        total_weight += weight
                except (ValueError, TypeError):
                    continue
        
        # Add club worth similarity if available
        if target.club_worth_eur and reference.club_worth_eur:
            try:
                target_worth = float(target.club_worth_eur)
                ref_worth = float(reference.club_worth_eur)
                
                if target_worth > 0 and ref_worth > 0:
                    # Use log scale for financial values
                    log_diff = abs(math.log10(target_worth) - math.log10(ref_worth))
                    worth_similarity = math.exp(-log_diff / 2)
                    total_similarity += worth_similarity * self.metric_weights['club_worth']
                    total_weight += self.metric_weights['club_worth']
            except (ValueError, TypeError, ZeroDivisionError):
                pass
        
        return total_similarity / total_weight if total_weight > 0 else 0
    
    def _calculate_prestige_similarity(self, target: TeamMetrics, reference: TeamMetrics) -> float:
        """Calculate similarity based on prestige and financial metrics."""
        total_similarity = 0
        total_weight = 0
        
        # International prestige
        if target.international_prestige and reference.international_prestige:
            try:
                diff = abs(float(target.international_prestige) - float(reference.international_prestige))
                sim = math.exp(-diff / 3)
                total_similarity += sim * 0.4
                total_weight += 0.4
            except (ValueError, TypeError):
                pass
        
        # Domestic prestige
        if target.domestic_prestige and reference.domestic_prestige:
            try:
                diff = abs(float(target.domestic_prestige) - float(reference.domestic_prestige))
                sim = math.exp(-diff / 3)
                total_similarity += sim * 0.3
                total_weight += 0.3
            except (ValueError, TypeError):
                pass
        
        # Club worth
        if target.club_worth_eur and reference.club_worth_eur:
            try:
                target_worth = float(target.club_worth_eur)
                ref_worth = float(reference.club_worth_eur)
                
                if target_worth > 0 and ref_worth > 0:
                    log_diff = abs(math.log10(target_worth) - math.log10(ref_worth))
                    worth_sim = math.exp(-log_diff / 2)
                    total_similarity += worth_sim * 0.3
                    total_weight += 0.3
            except (ValueError, TypeError, ZeroDivisionError):
                pass
        
        return total_similarity / total_weight if total_weight > 0 else 0
    
    def _is_same_context(self, target: TeamMetrics, reference: TeamMetrics) -> bool:
        """Check if teams are from same league/country context."""
        return (target.league_name == reference.league_name and 
                target.country == reference.country)
    
    def _get_fallback_elo(self, metrics: TeamMetrics) -> float:
        """Get fallback ELO when similarity matching fails - more conservative estimates."""
        # Use hierarchical fallback based on available metrics
        
        # 1. Overall rating fallback (using realistic conversion)
        if metrics.overall:
            try:
                overall = float(metrics.overall)
                return self._realistic_overall_to_elo(overall)
            except (ValueError, TypeError):
                pass
        
        # 2. Average of attack/midfield/defence (more conservative)
        individual_ratings = []
        for rating in [metrics.attack, metrics.midfield, metrics.defence]:
            if rating:
                try:
                    individual_ratings.append(float(rating))
                except (ValueError, TypeError):
                    pass
        
        if individual_ratings:
            avg_rating = sum(individual_ratings) / len(individual_ratings)
            # Apply penalty for incomplete data
            penalty = (3 - len(individual_ratings)) * 2  # -2 to -4 overall points
            adjusted_rating = max(0, avg_rating - penalty)
            return self._realistic_overall_to_elo(adjusted_rating)
        
        # 3. Prestige-based fallback (more conservative)
        if metrics.international_prestige:
            try:
                prestige = float(metrics.international_prestige)
                # Prestige scale: 1-10, map to ELO 1150-1650 (more conservative)
                if prestige <= 1:
                    elo = 1150
                elif prestige >= 10:
                    elo = 1650
                else:
                    elo = 1150 + (prestige - 1) * 55.56  # (1650-1150)/(10-1)
                return max(1000, min(2000, elo))
            except (ValueError, TypeError):
                pass
        
        # 4. League level fallback (more conservative)
        if metrics.league_level:
            try:
                level = int(metrics.league_level)
                # League level 1 = top tier, higher levels = lower tiers
                # More conservative: Level 1 = 1450, Level 2 = 1350, etc.
                base_elo = max(1200, 1450 - (level - 1) * 100)
                return max(1000, min(2000, base_elo))
            except (ValueError, TypeError):
                pass
        
        # 5. Final fallback - more conservative for unknown teams
        return 1350.0  # Below average instead of average
    
    def _realistic_overall_to_elo(self, overall_rating: float) -> float:
        """Convert overall rating to ELO using realistic distribution."""
        try:
            rating = float(overall_rating)
            
            # Clamp to valid range
            if rating < 0:
                rating = 0
            elif rating > 100:
                rating = 100
            
            # More realistic ELO conversion with bell curve distribution
            if rating <= 45:
                # Very weak teams: 0-45 overall → 1000-1200 ELO
                elo = 1000 + (rating / 45) * 200
            elif rating <= 85:
                # Normal distribution: 45-85 overall → 1200-1800 ELO  
                normalized = (rating - 45) / 40  # 0-1 range
                elo = 1200 + normalized * 600
            else:
                # Elite teams: 85-100 overall → 1800-2000 ELO
                normalized = (rating - 85) / 15  # 0-1 range
                elo = 1800 + normalized * 200
            
            return float(elo)
            
        except (ValueError, TypeError, OverflowError):
            return 1350.0
    
    def get_estimation_confidence(self, target_metrics: TeamMetrics) -> str:
        """Get confidence level for ELO estimation."""
        if not self.known_teams:
            return "low"
        
        # Check what metrics are available
        available_metrics = sum([
            1 if target_metrics.overall else 0,
            1 if target_metrics.attack else 0,
            1 if target_metrics.midfield else 0,
            1 if target_metrics.defence else 0,
            1 if target_metrics.international_prestige else 0,
            1 if target_metrics.domestic_prestige else 0
        ])
        
        # Check if same league teams exist
        same_league_count = sum(
            1 for _, (_, metrics) in self.known_teams.items()
            if (metrics.league_name == target_metrics.league_name and 
                metrics.country == target_metrics.country)
        )
        
        if available_metrics >= 4 and same_league_count >= 3:
            return "high"
        elif available_metrics >= 2 and len(self.known_teams) >= 10:
            return "medium"
        else:
            return "low"


# Global ELO estimator instance
elo_estimator = ELOEstimator()