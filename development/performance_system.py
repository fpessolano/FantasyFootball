"""
Performance Management System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multi-model system for handling player fatigue, form, momentum, and pressure effects.
"""

import math
import random
from typing import Dict, List, Optional, Tuple
from models import Player, Position, TemperamentType


class FatigueModel:
    """Multi-layered fatigue system with different accumulation models."""
    
    def __init__(self):
        # Position-based fatigue multipliers
        self.position_fatigue_rates = {
            Position.GK: 0.3,    # Goalkeepers tire least
            Position.CB: 0.6,    # Center backs moderate
            Position.SW: 0.6,    # Sweepers moderate
            Position.LB: 0.9,    # Fullbacks run a lot
            Position.RB: 0.9,
            Position.DM: 0.8,    # Defensive mids
            Position.CM: 1.0,    # Central mids tire most
            Position.AM: 0.9,    # Attacking mids
            Position.LM: 0.95,   # Side midfielders
            Position.RM: 0.95,
            Position.LW: 0.95,   # Wingers
            Position.RW: 0.95,
            Position.ST: 0.7,    # Strikers moderate
            Position.WB: 0.9,    # Wing backs
            Position.LWB: 0.95,  # Wing backs run most
            Position.RWB: 0.95
        }
        
        # Attribute-specific fatigue sensitivity
        self.attribute_fatigue_impact = {
            'goalkeeping': 0.05,  # 5% max reduction
            'defending': 0.15,    # 15% max reduction
            'passing': 0.12,      # 12% max reduction
            'dribbling': 0.20,    # 20% max reduction
            'shooting': 0.18,     # 18% max reduction
            'physical': 0.35      # 35% max reduction (most affected)
        }
    
    def calculate_multi_phase_fatigue(self, player: Player, match_time: float, base_intensity: float) -> float:
        """Multi-phase fatigue with different rates per match period."""
        # Determine current phase multiplier
        if match_time <= 15:      # Fresh start
            phase_multiplier = 0.8
        elif match_time <= 45:    # First half progression
            phase_multiplier = 1.0
        elif match_time <= 60:    # Post-halftime adjustment
            phase_multiplier = 1.2
        elif match_time <= 75:    # Second half fatigue
            phase_multiplier = 1.4
        else:                     # Final exhaustion
            phase_multiplier = 1.8
        
        # Calculate fatigue with phase adjustment
        base_rate = 0.8 * (1 - player.natural_fitness / 150)  # Base rate 0.27 to 0.8
        position_rate = self.position_fatigue_rates.get(player.position, 1.0)
        work_rate_impact = 0.8 + (player.work_rate / 100) * 0.6  # 0.8 to 1.4
        intensity_impact = 0.6 + (base_intensity / 100) * 0.8   # 0.6 to 1.4
        
        total_rate = base_rate * position_rate * work_rate_impact * intensity_impact * phase_multiplier
        
        # Apply discrete time step fatigue
        time_step = 1.0  # 1 minute
        stamina_multiplier = (1 - total_rate * 0.01) ** time_step
        return player.current_stamina * stamina_multiplier
    
    def apply_fatigue_to_attributes(self, player: Player) -> Dict[str, float]:
        """Apply fatigue effects to all player attributes."""
        fatigue_level = 1 - (player.current_stamina / 100)  # 0 = fresh, 1 = exhausted
        
        # Concentration helps maintain performance when tired
        concentration_help = player.concentration / 100 * 0.3  # Up to 30% fatigue resistance
        effective_fatigue = fatigue_level * (1 - concentration_help)
        
        modified_attributes = {}
        base_attributes = {
            'goalkeeping': player.goalkeeping,
            'defending': player.defending,
            'passing': player.passing,
            'dribbling': player.dribbling,
            'shooting': player.shooting,
            'physical': player.physical
        }
        
        for attr_name, base_value in base_attributes.items():
            max_reduction = self.attribute_fatigue_impact[attr_name]
            fatigue_modifier = 1 - (effective_fatigue * max_reduction)
            modified_attributes[attr_name] = base_value * fatigue_modifier
            
        return modified_attributes
    
    def update_stamina(self, player: Player, minutes_played: float, intensity: float) -> float:
        """Update player stamina using multi-phase model."""
        new_stamina = self.calculate_multi_phase_fatigue(player, minutes_played, intensity)
        player.current_stamina = max(0, new_stamina)
        player.minutes_played_today += 1.0
        player.match_intensity = intensity
        return player.current_stamina


class MomentumSystem:
    """Event-based momentum and form tracking."""
    
    def __init__(self):
        self.team_momentum = 0  # -100 to +100
        self.player_momentum = {}  # Individual player momentum
        
        # Event impact values
        self.event_impacts = {
            'goal_scored': 15,
            'goal_conceded': -20,
            'assist': 8,
            'key_pass': 5,
            'successful_tackle': 3,
            'successful_dribble': 2,
            'save': 5,
            'missed_penalty': -15,
            'missed_easy_chance': -8,
            'turnover': -3,
            'foul_committed': -2,
            'yellow_card': -8,
            'red_card': -25
        }
    
    def process_event(self, event_type: str, player: Player, match_time: float):
        """Process match event and update momentum."""
        base_impact = self.event_impacts.get(event_type, 0)
        
        # Late events have more impact
        time_factor = 1 + (match_time / 90) * 0.5
        
        # Temperament affects momentum sensitivity
        temperament_multiplier = {
            TemperamentType.COOL_HEADED: 0.7,
            TemperamentType.PASSIONATE: 1.5,
            TemperamentType.CONSISTENT: 0.9,
            TemperamentType.VOLATILE: 1.3
        }
        
        multiplier = temperament_multiplier[player.temperament] * time_factor
        final_impact = base_impact * multiplier
        
        # Update team momentum
        self.team_momentum = max(-100, min(100, self.team_momentum + final_impact))
        
        # Update individual player momentum
        player_id = player.name
        if player_id not in self.player_momentum:
            self.player_momentum[player_id] = 0
            
        self.player_momentum[player_id] = max(-50, min(50, 
            self.player_momentum[player_id] + final_impact * 1.5))
    
    def decay_momentum(self, decay_rate: float = 0.02):
        """Apply momentum decay over time."""
        self.team_momentum *= (1 - decay_rate)
        for player_id in self.player_momentum:
            self.player_momentum[player_id] *= (1 - decay_rate)
    
    def get_momentum_modifier(self, player: Player) -> float:
        """Get performance modifier from momentum with realistic bounds."""
        # Reduced momentum impact
        team_boost = self.team_momentum / 100 * 0.10  # Max 10% instead of 15%
        individual_boost = self.player_momentum.get(player.name, 0) / 100 * 0.05  # Max 5% instead of 10%
        
        # Leadership amplifies but with limits
        leadership_factor = 1 + (player.leadership / 100) * 0.3  # Reduced from 0.5
        team_boost *= leadership_factor
        
        # Clamp total momentum effect
        total_momentum = team_boost + individual_boost
        clamped_momentum = max(-0.12, min(0.12, total_momentum))  # ±12% maximum
        
        return 1 + clamped_momentum


class PressureSystem:
    """Handle high-pressure situations."""
    
    def __init__(self):
        self.pressure_situations = {
            'penalty': 1.0,
            'last_minute': 0.8,
            'important_match': 0.6,
            'derby': 0.7,
            'cup_final': 1.2
        }
    
    def apply_pressure_modifier(self, player: Player, situation: str) -> float:
        """Apply pressure modifier with realistic bounds."""
        base_pressure = self.pressure_situations.get(situation, 0)
        
        # Player's pressure handling ability
        handling_factor = player.pressure_handling / 100
        composure_factor = player.composure / 100
        
        # Reduced pressure impact
        pressure_impact = base_pressure * (1 - handling_factor) * (1 - composure_factor * 0.5)
        
        # Temperament affects but with limits
        temperament_modifier = {
            TemperamentType.COOL_HEADED: 0.4,  # Reduced from 0.5
            TemperamentType.PASSIONATE: 1.0,   # Reduced from 1.2
            TemperamentType.CONSISTENT: 0.7,   # Reduced from 0.8
            TemperamentType.VOLATILE: 1.2      # Reduced from 1.5
        }
        
        final_impact = pressure_impact * temperament_modifier[player.temperament]
        
        # Clamp pressure effects to ±8%
        if player.pressure_handling > 70:
            modifier = 1 + min(0.08, final_impact * 0.08)  # Small boost, max 8%
        else:
            modifier = 1 - min(0.08, final_impact * 0.10)  # Performance drop, max 8%
        
        return modifier


class RecoverySystem:
    """Stamina recovery and rest management."""
    
    def calculate_recovery(self, player: Player, hours_rested: float, activity_type: str = "full_rest") -> float:
        """Calculate stamina recovery over time."""
        # Recovery rates by activity
        recovery_rates = {
            'full_rest': 1.0,
            'light_training': 0.6,
            'normal_training': 0.3,
            'intense_training': 0.1,
            'match': -0.5  # Playing causes fatigue
        }
        
        base_rate = recovery_rates.get(activity_type, 1.0)
        
        # Natural fitness affects recovery speed
        fitness_bonus = (player.natural_fitness / 100) * 0.5  # Up to 50% bonus
        total_rate = base_rate * (1 + fitness_bonus)
        
        # Age affects recovery (peak at 23-27)
        age_factor = 1.0
        if player.age < 23:
            age_factor = 0.85 + (player.age - 18) * 0.03  # Young players recover slower
        elif player.age > 27:
            age_factor = 1.0 - (player.age - 27) * 0.02   # Older players recover slower
        
        total_rate *= age_factor
        
        # Exponential recovery - faster when more fatigued
        stamina_deficit = 100 - player.current_stamina
        recovery_rate = 0.015 * total_rate
        recovered = stamina_deficit * (1 - math.exp(-recovery_rate * hours_rested))
        
        new_stamina = min(100, player.current_stamina + recovered)
        player.current_stamina = new_stamina
        
        return new_stamina


class PlayerPerformanceManager:
    """Master class that coordinates all performance systems."""
    
    def __init__(self):
        self.fatigue_model = FatigueModel()
        self.momentum_system = MomentumSystem()
        self.pressure_system = PressureSystem()
        self.recovery_system = RecoverySystem()
    
    def get_player_consistency(self, player: Player) -> float:
        """Calculate player consistency from existing attributes."""
        # Elite players are more consistent
        base_consistency = player.overall_rating()
        
        # Mental attributes affect consistency
        mental_factor = (player.concentration + player.composure + player.determination) / 3
        
        # Experience (age) affects consistency - peak at 27-30
        if 27 <= player.age <= 30:
            age_factor = 1.0  # Peak consistency
        elif player.age < 27:
            age_factor = 0.85 + (player.age - 18) * 0.15 / 9  # Improving consistency
        else:
            age_factor = 1.0 - (player.age - 30) * 0.02  # Declining consistency
        
        # Temperament affects consistency 
        temperament_factor = {
            TemperamentType.CONSISTENT: 1.2,
            TemperamentType.COOL_HEADED: 1.1,
            TemperamentType.PASSIONATE: 0.9,
            TemperamentType.VOLATILE: 0.7
        }[player.temperament]
        
        # Final consistency score (0-100)
        consistency = (base_consistency * 0.6 + mental_factor * 0.4) * age_factor * temperament_factor
        return min(100, max(20, consistency))
    
    def _get_player_tier(self, player: Player) -> str:
        """Determine player tier for bounds calculation."""
        overall = player.overall_rating()
        if overall >= 85:
            return "elite"
        elif overall >= 70:
            return "good"
        elif overall >= 60:
            return "average"
        else:
            return "poor"
    
    def _apply_consistency_based_bounds(self, player: Player, raw_modifier: float) -> float:
        """Apply consistency-based performance bounds."""
        import math
        
        # Calculate player's consistency (20-100 scale)
        consistency = self.get_player_consistency(player)
        
        # Convert consistency to variation allowance
        # High consistency (90+) = ±8% max variation
        # Low consistency (30-) = ±25% max variation
        max_variation = 0.30 - (consistency / 100) * 0.22  # 0.08 to 0.30 range
        
        # Elite players also have higher performance floors
        if player.overall_rating() >= 85:
            min_modifier = 1 - max_variation * 0.7  # Elite players don't drop as much
            max_modifier = 1 + max_variation * 0.8
        elif player.overall_rating() >= 70:
            min_modifier = 1 - max_variation * 0.85
            max_modifier = 1 + max_variation * 0.9
        else:
            min_modifier = 1 - max_variation
            max_modifier = 1 + max_variation * 0.7  # Average players can't boost as much
        
        # Apply sigmoid with consistency-based bounds
        normalized = math.tanh((raw_modifier - 1) * 3)
        
        if normalized >= 0:
            final_modifier = 1 + normalized * (max_modifier - 1)
        else:
            final_modifier = 1 + normalized * (1 - min_modifier)
        
        return final_modifier
    
    def get_effective_attributes(self, player: Player, 
                               match_situation: Optional[str] = None) -> Dict[str, float]:
        """Get player's effective attributes with realistic bounds."""
        
        # Start with fatigue-modified base attributes
        fatigued_attrs = self.fatigue_model.apply_fatigue_to_attributes(player)
        
        # Get individual modifiers (now with reduced ranges)
        form_modifier = player.form.get_form_modifier()  # 0.9-1.15 range
        momentum_modifier = self.momentum_system.get_momentum_modifier(player)  # ±12% max
        pressure_modifier = 1.0
        if match_situation:
            pressure_modifier = self.pressure_system.apply_pressure_modifier(player, match_situation)  # ±8% max
        
        # Calculate combined raw modifier
        raw_total_modifier = form_modifier * momentum_modifier * pressure_modifier
        
        # Apply consistency-based bounds to each attribute
        bounded_modifier = self._apply_consistency_based_bounds(player, raw_total_modifier)
        
        # Apply to all attributes
        final_attributes = {}
        for attr_name, fatigued_value in fatigued_attrs.items():
            final_attributes[attr_name] = fatigued_value * bounded_modifier
            
        return final_attributes
    
    def process_match_minute(self, player: Player, intensity: float, match_time: float):
        """Process one minute of match time."""
        # Update fatigue
        self.fatigue_model.update_stamina(player, match_time, intensity)
        
        # Decay momentum slightly
        self.momentum_system.decay_momentum(0.002)  # 0.2% per minute
    
    def process_match_event(self, event_type: str, player: Player, match_time: float):
        """Process a match event (goal, tackle, etc.)."""
        self.momentum_system.process_event(event_type, player, match_time)
    
    def end_match_processing(self, player: Player, match_rating: float):
        """Process end-of-match updates."""
        player.form.update_form(match_rating, player.temperament)
        player.minutes_played_today = 0
        player.match_intensity = 50.0
    
    def process_rest_period(self, player: Player, hours: float, activity: str = "full_rest"):
        """Process recovery during rest periods."""
        self.recovery_system.calculate_recovery(player, hours, activity)
    
    def get_player_status_summary(self, player: Player) -> Dict[str, float]:
        """Get comprehensive player status for display."""
        effective_attrs = self.get_effective_attributes(player)
        return {
            'stamina': player.current_stamina,
            'form_rating': player.form.base_form,
            'confidence': player.form.confidence,
            'consistency': self.get_player_consistency(player),
            'momentum': self.momentum_system.player_momentum.get(player.name, 0),
            'effective_overall': sum(effective_attrs.values()) / 6,
            'tier': self._get_player_tier(player)
        }
