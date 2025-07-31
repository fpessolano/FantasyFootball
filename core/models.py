"""
Fantasy Football Models - Extended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enhanced data models with fatigue, form, and performance tracking.
"""

from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import json
import math
from collections import deque, defaultdict


class Position(Enum):
    """Player positions with their abbreviations."""
    GK = "GK"   # Goalkeeper
    CB = "CB"   # Center Back
    SW = "SW"   # Sweeper / Libero
    LB = "LB"   # Left Back
    RB = "RB"   # Right Back
    CM = "CM"   # Central Midfielder
    DM = "DM"   # Defensive Midfielder
    WB = "WB"   # Wing Back (generic)
    LWB = "LWB" # Left Wing Back
    RWB = "RWB" # Right Wing Back
    AM = "AM"   # Attacking Midfielder
    LM = "LM"   # Left Midfielder
    RM = "RM"   # Right Midfielder
    ST = "ST"   # Striker
    LW = "LW"   # Left Winger
    RW = "RW"   # Right Winger


class TacticalStyle(Enum):
    """Team tactical styles with their effect multipliers."""
    BALANCED = (1.0, 1.0, 1.0)  # (attack_mult, defence_mult, midfield_mult)
    ATTACKING = (1.2, 0.9, 1.0)
    DEFENSIVE = (0.8, 1.2, 1.0)
    WIDE = (1.0, 1.0, 1.1)      # emphasises side flows
    CENTRAL = (1.0, 1.0, 0.9)   # emphasises central play
    
    def multipliers(self) -> Tuple[float, float, float]:
        return self.value


class TemperamentType(Enum):
    """Player temperament types affecting performance variation."""
    COOL_HEADED = "cool_headed"    # Less affected by pressure, slower momentum swings
    PASSIONATE = "passionate"      # Higher momentum swings, more affected by events
    CONSISTENT = "consistent"      # Stable performance, less form variation
    VOLATILE = "volatile"         # High performance variation, big form swings


@dataclass
class PlayerForm:
    """Tracks individual player form and confidence."""
    performance_history: deque = field(default_factory=lambda: deque(maxlen=5))
    base_form: float = 7.0  # 1-10 scale
    confidence: float = 50.0  # 0-100 scale
    
    def update_form(self, match_rating: float, temperament: TemperamentType):
        """Update form based on match performance."""
        self.performance_history.append(match_rating)
        
        # Weighted average favoring recent matches
        weights = [0.1, 0.15, 0.2, 0.25, 0.3]  # Most recent weighs more
        weighted_sum = sum(p * w for p, w in zip(reversed(self.performance_history), weights))
        weight_total = sum(weights[:len(self.performance_history)])
        
        new_form = weighted_sum / weight_total if weight_total > 0 else self.base_form
        
        # Temperament affects form stability
        change_rate = {
            TemperamentType.COOL_HEADED: 0.2,
            TemperamentType.PASSIONATE: 0.4,
            TemperamentType.CONSISTENT: 0.15,
            TemperamentType.VOLATILE: 0.5
        }
        
        rate = change_rate[temperament]
        self.base_form += (new_form - self.base_form) * rate
        
        # Update confidence based on recent performance
        if match_rating >= 7.5:
            self.confidence = min(100, self.confidence + 5)
        elif match_rating <= 5.5:
            self.confidence = max(0, self.confidence - 8)
        else:
            self.confidence += (match_rating - 6.5) * 0.5
    
    def get_form_modifier(self) -> float:
        """Convert form to performance modifier with realistic bounds."""
        # Clamp form to reasonable range first
        clamped_form = max(3.0, min(9.0, self.base_form))  # 3-9 range instead of 1-10
        
        # Form scale: 3-9 -> modifier: 0.9-1.15 (instead of 0.8-1.2)
        form_mod = 0.9 + (clamped_form - 3.0) / 6.0 * 0.25  # Max ±12.5%
        
        # Confidence adds smaller modifier
        confidence_mod = 0.97 + (self.confidence / 100) * 0.06  # Max ±3%
        
        return form_mod * confidence_mod


@dataclass
class PlayerStats:
    """
    Comprehensive player statistics tracking.
    Tracks both career totals and per-tournament stats.
    """
    # Career totals
    career_matches: int = 0
    career_minutes: int = 0
    career_goals: int = 0
    career_assists: int = 0
    career_saves: int = 0
    career_clean_sheets: int = 0
    career_yellow_cards: int = 0
    career_red_cards: int = 0
    career_motm: int = 0  # Man of the Match awards
    
    # Advanced stats
    career_shots: int = 0
    career_shots_on_target: int = 0
    career_passes: int = 0
    career_passes_completed: int = 0
    career_tackles: int = 0
    career_tackles_won: int = 0
    career_interceptions: int = 0
    career_dribbles: int = 0
    career_dribbles_successful: int = 0
    career_fouls_committed: int = 0
    career_fouls_suffered: int = 0
    
    # Per-tournament tracking (tournament_name -> stats)
    tournament_stats: Dict[str, Dict[str, int]] = field(default_factory=dict)
    
    def add_tournament_stat(self, tournament: str, stat_name: str, value: int = 1):
        """Add to a specific tournament stat."""
        if tournament not in self.tournament_stats:
            self.tournament_stats[tournament] = defaultdict(int)
        self.tournament_stats[tournament][stat_name] += value
    
    def get_tournament_stat(self, tournament: str, stat_name: str) -> int:
        """Get a specific tournament stat."""
        return self.tournament_stats.get(tournament, {}).get(stat_name, 0)
    
    def get_goals_per_game(self) -> float:
        """Calculate career goals per game."""
        return self.career_goals / self.career_matches if self.career_matches > 0 else 0.0
    
    def get_assists_per_game(self) -> float:
        """Calculate career assists per game."""
        return self.career_assists / self.career_matches if self.career_matches > 0 else 0.0
    
    def get_pass_accuracy(self) -> float:
        """Calculate career pass accuracy percentage."""
        return (self.career_passes_completed / self.career_passes * 100) if self.career_passes > 0 else 0.0
    
    def get_tackle_success_rate(self) -> float:
        """Calculate career tackle success rate percentage."""
        return (self.career_tackles_won / self.career_tackles * 100) if self.career_tackles > 0 else 0.0
    
    def get_shot_accuracy(self) -> float:
        """Calculate career shot accuracy percentage."""
        return (self.career_shots_on_target / self.career_shots * 100) if self.career_shots > 0 else 0.0
    
    def get_dribble_success_rate(self) -> float:
        """Calculate career dribble success rate percentage."""
        return (self.career_dribbles_successful / self.career_dribbles * 100) if self.career_dribbles > 0 else 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'career_matches': self.career_matches,
            'career_minutes': self.career_minutes,
            'career_goals': self.career_goals,
            'career_assists': self.career_assists,
            'career_saves': self.career_saves,
            'career_clean_sheets': self.career_clean_sheets,
            'career_yellow_cards': self.career_yellow_cards,
            'career_red_cards': self.career_red_cards,
            'career_motm': self.career_motm,
            'career_shots': self.career_shots,
            'career_shots_on_target': self.career_shots_on_target,
            'career_passes': self.career_passes,
            'career_passes_completed': self.career_passes_completed,
            'career_tackles': self.career_tackles,
            'career_tackles_won': self.career_tackles_won,
            'career_interceptions': self.career_interceptions,
            'career_dribbles': self.career_dribbles,
            'career_dribbles_successful': self.career_dribbles_successful,
            'career_fouls_committed': self.career_fouls_committed,
            'career_fouls_suffered': self.career_fouls_suffered,
            'tournament_stats': dict(self.tournament_stats)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PlayerStats':
        """Create PlayerStats from dictionary."""
        tournament_stats = {}
        for tournament, stats in data.get('tournament_stats', {}).items():
            tournament_stats[tournament] = defaultdict(int, stats)
        
        return cls(
            career_matches=data.get('career_matches', 0),
            career_minutes=data.get('career_minutes', 0),
            career_goals=data.get('career_goals', 0),
            career_assists=data.get('career_assists', 0),
            career_saves=data.get('career_saves', 0),
            career_clean_sheets=data.get('career_clean_sheets', 0),
            career_yellow_cards=data.get('career_yellow_cards', 0),
            career_red_cards=data.get('career_red_cards', 0),
            career_motm=data.get('career_motm', 0),
            career_shots=data.get('career_shots', 0),
            career_shots_on_target=data.get('career_shots_on_target', 0),
            career_passes=data.get('career_passes', 0),
            career_passes_completed=data.get('career_passes_completed', 0),
            career_tackles=data.get('career_tackles', 0),
            career_tackles_won=data.get('career_tackles_won', 0),
            career_interceptions=data.get('career_interceptions', 0),
            career_dribbles=data.get('career_dribbles', 0),
            career_dribbles_successful=data.get('career_dribbles_successful', 0),
            career_fouls_committed=data.get('career_fouls_committed', 0),
            career_fouls_suffered=data.get('career_fouls_suffered', 0),
            tournament_stats=tournament_stats
        )


@dataclass
class Player:
    """
    Enhanced player with fatigue, form, and extended attributes.
    """
    name: str
    position: Position
    
    # Core attributes (0-100)
    goalkeeping: int
    defending: int
    passing: int
    dribbling: int
    shooting: int
    physical: int
    
    # Player nationality (with default for backward compatibility)
    nationality: str = "Unknown"
    
    # Extended attributes (0-100)
    natural_fitness: int = 70      # Base stamina and recovery rate
    work_rate: int = 50           # How quickly player gets tired
    injury_proneness: int = 30    # Likelihood of getting injured when fatigued
    pressure_handling: int = 60   # Performance under high-stakes situations
    concentration: int = 60       # Maintains performance when tired
    determination: int = 60       # Resistance to negative momentum
    composure: int = 60          # Performance in crucial moments
    leadership: int = 30         # Influence on team momentum
    
    # Personality and physical traits
    temperament: TemperamentType = TemperamentType.CONSISTENT
    preferred_foot: str = "right"
    age: int = 25
    
    # Performance tracking (runtime data)
    current_stamina: float = 100.0
    match_intensity: float = 50.0
    minutes_played_today: float = 0.0
    
    # Match status (runtime data)
    is_sent_off: bool = False     # NEW: Track if player was sent off
    yellow_cards: int = 0         # NEW: Track yellow cards in current match
    
    # Form tracking
    form: PlayerForm = field(default_factory=PlayerForm)
    
    # Statistics tracking
    stats: PlayerStats = field(default_factory=PlayerStats)
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "position": self.position.name,
            "nationality": self.nationality,
            "goalkeeping": self.goalkeeping,
            "defending": self.defending,
            "passing": self.passing,
            "dribbling": self.dribbling,
            "shooting": self.shooting,
            "physical": self.physical,
            "natural_fitness": self.natural_fitness,
            "work_rate": self.work_rate,
            "injury_proneness": self.injury_proneness,
            "pressure_handling": self.pressure_handling,
            "concentration": self.concentration,
            "determination": self.determination,
            "composure": self.composure,
            "leadership": self.leadership,
            "temperament": self.temperament.value,
            "preferred_foot": self.preferred_foot,
            "age": self.age,
            "current_stamina": self.current_stamina,
            # Form data is reset each time for simplicity
            "form_base": self.form.base_form,
            "form_confidence": self.form.confidence,
            # Statistics data
            "stats": self.stats.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary."""
        # Handle legacy data that might not have extended attributes
        player = cls(
            name=data["name"],
            position=Position[data["position"]],
            nationality=data.get("nationality", "Unknown"),  # Handle legacy data
            goalkeeping=data["goalkeeping"],
            defending=data["defending"],
            passing=data["passing"],
            dribbling=data["dribbling"],
            shooting=data["shooting"],
            physical=data["physical"],
            natural_fitness=data.get("natural_fitness", data.get("physical", 70)),
            work_rate=data.get("work_rate", 50),
            injury_proneness=data.get("injury_proneness", 30),
            pressure_handling=data.get("pressure_handling", 60),
            concentration=data.get("concentration", 60),
            determination=data.get("determination", 60),
            composure=data.get("composure", 60),
            leadership=data.get("leadership", 30),
            temperament=TemperamentType(data.get("temperament", "consistent")),
            preferred_foot=data.get("preferred_foot", "right"),
            age=data.get("age", 25),
            current_stamina=data.get("current_stamina", 100.0)
        )
        
        # Restore form data if available
        if "form_base" in data:
            player.form.base_form = data["form_base"]
        if "form_confidence" in data:
            player.form.confidence = data["form_confidence"]
        
        # Restore stats data if available
        if "stats" in data:
            player.stats = PlayerStats.from_dict(data["stats"])
            
        return player
    
    def overall_rating(self) -> float:
        """Calculate overall player rating based on position."""
        if self.position == Position.GK:
            return (self.goalkeeping * 0.5 + self.defending * 0.2 + 
                    self.physical * 0.2 + self.passing * 0.1)
        elif self.position in [Position.CB, Position.SW, Position.LB, Position.RB]:
            return (self.defending * 0.4 + self.physical * 0.3 + 
                    self.passing * 0.2 + self.dribbling * 0.1)
        elif self.position in [Position.CM, Position.DM, Position.WB, Position.LWB, Position.RWB]:
            return (self.passing * 0.3 + self.defending * 0.2 + 
                    self.physical * 0.2 + self.dribbling * 0.2 + self.shooting * 0.1)
        elif self.position in [Position.AM, Position.LM, Position.RM]:
            return (self.passing * 0.3 + self.dribbling * 0.3 + 
                    self.shooting * 0.2 + self.physical * 0.1 + self.defending * 0.1)
        else:  # ST, LW, RW
            return (self.shooting * 0.35 + self.dribbling * 0.25 + 
                    self.physical * 0.2 + self.passing * 0.15 + self.defending * 0.05)
    
    def reset_match_state(self):
        """Reset player state for a new match."""
        self.match_intensity = 50.0
        self.minutes_played_today = 0.0
        self.is_sent_off = False       # NEW: Reset red card status
        self.yellow_cards = 0          # NEW: Reset yellow cards
        # Don't reset stamina here - it should carry over between matches
    
    def get_display_name(self) -> str:
        """Get player name with nationality for display."""
        if self.nationality != "Unknown":
            return f"{self.name} ({self.nationality})"
        return self.name
    
    def get_nationality_flag(self) -> str:
        """Get nationality with flag emoji where possible."""
        flag_map = {
            'American': '🇺🇸', 'British': '🇬🇧', 'English': '🇬🇧',
            'French': '🇫🇷', 'German': '🇩🇪', 'Italian': '🇮🇹',
            'Spanish': '🇪🇸', 'Portuguese': '🇵🇹', 'Brazilian': '🇧🇷',
            'Dutch': '🇳🇱', 'Belgian': '🇧🇪', 'Swedish': '🇸🇪',
            'Norwegian': '🇳🇴', 'Danish': '🇩🇰', 'Finnish': '🇫🇮',
            'Polish': '🇵🇱', 'Russian': '🇷🇺', 'Ukrainian': '🇺🇦',
            'Czech': '🇨🇿', 'Slovak': '🇸🇰', 'Hungarian': '🇭🇺',
            'Croatian': '🇭🇷', 'Serbian': '🇷🇸', 'Greek': '🇬🇷',
            'Turkish': '🇹🇷', 'Japanese': '🇯🇵', 'Korean': '🇰🇷',
            'Chinese': '🇨🇳', 'Argentine': '🇦🇷', 'Mexican': '🇲🇽',
            'Colombian': '🇨🇴', 'Chilean': '🇨🇱', 'Peruvian': '🇵🇪'
        }
        flag = flag_map.get(self.nationality, '🌍')
        return f"{flag} {self.nationality}"
    
    def __str__(self) -> str:
        """String representation of player."""
        return f"{self.get_display_name()} - {self.position.name} (OVR: {self.overall_rating():.0f})"


@dataclass
class Team:
    """
    Enhanced team with performance tracking.
    """
    name: str
    formation: str
    players: List[Player] = field(default_factory=list)
    style: TacticalStyle = TacticalStyle.BALANCED
    elo_rating: float = 1500.0
    streak_count: int = 0
    
    # Team momentum tracking
    team_momentum: float = 0.0  # -100 to +100
    
    def get_available_players(self) -> List[Player]:
        """Get list of players still available to play (not sent off)."""
        return [p for p in self.players if not p.is_sent_off]
    
    def get_sent_off_players(self) -> List[Player]:
        """Get list of players who have been sent off."""
        return [p for p in self.players if p.is_sent_off]
    
    def compute_team_ratings(self) -> Dict[str, float]:
        """Compute aggregated team ratings from player attributes."""
        total = {
            "keeping": 0,
            "defence": 0,
            "midfield": 0,
            "attack": 0,
            "left_flow": 0,
            "right_flow": 0,
            "center_flow": 0,
        }
        
        # Only consider available players (not sent off)
        available_players = self.get_available_players()
        
        for p in available_players:
            # Goalkeeping
            total["keeping"] += p.goalkeeping if p.position == Position.GK else 0
            
            # Defence
            total["defence"] += p.defending
            
            # Midfield
            total["midfield"] += p.passing + p.physical
            
            # Attack
            total["attack"] += p.shooting + p.dribbling
            
            # Flow calculations
            if p.position in [Position.LB, Position.LM, Position.LW, Position.LWB]:
                total["left_flow"] += p.passing
            elif p.position in [Position.RB, Position.RM, Position.RW, Position.RWB]:
                total["right_flow"] += p.passing
            elif p.position in [Position.CM, Position.AM, Position.DM, Position.ST, Position.SW]:
                total["center_flow"] += p.passing
        
        # Normalize by available player count, apply penalty for reduced numbers
        available_count = len(available_players)
        if available_count == 0:
            return {k: 0 for k in total.keys()}  # No players available
        
        # Apply numerical disadvantage penalty
        numerical_penalty = self._get_numerical_disadvantage_penalty(available_count)
        
        normalized_ratings = {k: (v / available_count) * numerical_penalty for k, v in total.items()}
        return normalized_ratings
    
    def _get_numerical_disadvantage_penalty(self, available_players: int) -> float:
        """Calculate performance penalty for having fewer than 11 players."""
        if available_players >= 11:
            return 1.0  # No penalty
        elif available_players == 10:
            return 0.85  # 15% penalty for 10 players
        elif available_players == 9:
            return 0.70  # 30% penalty for 9 players
        elif available_players == 8:
            return 0.55  # 45% penalty for 8 players
        elif available_players == 7:
            return 0.40  # 60% penalty for 7 players
        else:
            return 0.25  # 75% penalty for very few players
    
    def compute_strength(self) -> float:
        """Compute overall team strength."""
        ratings = self.compute_team_ratings()
        att_mult, def_mult, mid_mult = self.style.multipliers()
        
        # Apply tactical multipliers
        gk = ratings["keeping"]
        defense = ratings["defence"] * def_mult
        midfield = ratings["midfield"] * mid_mult
        attack = ratings["attack"] * att_mult
        
        # Weighted average
        base_strength = gk * 0.1 + defense * 0.3 + midfield * 0.3 + attack * 0.3
        
        # Apply additional penalty for playing with fewer players
        available_count = len(self.get_available_players())
        if available_count < 11:
            # Extra penalty beyond the ratings adjustment
            cohesion_penalty = 0.95 ** (11 - available_count)  # Each missing player = 5% additional penalty
            base_strength *= cohesion_penalty
        
        return base_strength
    
    def adjust_for_streak(self, enabled: bool = True) -> float:
        """Calculate momentum adjustment based on streak."""
        if not enabled:
            return 1.0
        streak_bonus = min(max(self.streak_count, -5), 5)
        return 1 + 0.03 * streak_bonus
    
    def get_team_momentum_modifier(self) -> float:
        """Get performance modifier from team momentum."""
        return 1 + (self.team_momentum / 100) * 0.15  # Max 15% boost/penalty
    
    def update_team_momentum(self, change: float):
        """Update team momentum and apply decay."""
        self.team_momentum = max(-100, min(100, self.team_momentum + change))
        # Apply small decay
        self.team_momentum *= 0.98
    
    def reset_players_for_match(self):
        """Reset all players' match state."""
        for player in self.players:
            player.reset_match_state()
    
    def to_dict(self) -> Dict:
        """Convert team to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "formation": self.formation,
            "style": self.style.name,
            "elo_rating": self.elo_rating,
            "streak_count": self.streak_count,
            "team_momentum": self.team_momentum,
            "players": [p.to_dict() for p in self.players]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Team':
        """Create team from dictionary."""
        players = [Player.from_dict(p) for p in data.get("players", [])]
        return cls(
            name=data["name"],
            formation=data["formation"],
            players=players,
            style=TacticalStyle[data.get("style", "BALANCED")],
            elo_rating=data.get("elo_rating", 1500.0),
            streak_count=data.get("streak_count", 0),
            team_momentum=data.get("team_momentum", 0.0)
        )
    
    def validate_formation(self) -> Tuple[bool, str]:
        """Validate team formation."""
        if len(self.players) != 11:
            return False, f"Team must have exactly 11 players, has {len(self.players)}"
        
        gk_count = sum(1 for p in self.players if p.position == Position.GK)
        if gk_count != 1:
            return False, f"Team must have exactly 1 goalkeeper, has {gk_count}"
        
        return True, "Valid formation"
    
    def summary(self) -> str:
        """Generate a summary of the team."""
        ratings = self.compute_team_ratings()
        strength = self.compute_strength()
        
        # Format streak
        if self.streak_count > 0:
            streak_str = f"{self.streak_count}W streak"
            streak_emoji = "🔥"
        elif self.streak_count < 0:
            streak_str = f"{abs(self.streak_count)}L streak"
            streak_emoji = "❄️"
        else:
            streak_str = "No streak"
            streak_emoji = "⚪"
        
        lines = [
            f"\n📋 {self.name} ({self.style.name})",
            f"Formation: {self.formation}",
            f"Elo Rating: {self.elo_rating:.0f}",
            f"Current Form: {streak_emoji} {streak_str}",
            f"Team Momentum: {self.team_momentum:+.1f}",
            f"Total Strength: {strength:.2f}",
            "",
            "Players:"
        ]
        
        for p in sorted(self.players, key=lambda x: x.position.name):
            # Show extended attributes in summary
            lines.append(
                f"  {p.name:20} {p.position.name:3} "
                f"G:{p.goalkeeping:2d} D:{p.defending:2d} P:{p.passing:2d} "
                f"Dr:{p.dribbling:2d} S:{p.shooting:2d} Ph:{p.physical:2d} "
                f"(OVR: {p.overall_rating():.0f}) "
                f"Fit:{p.natural_fitness:2d} Temp:{p.temperament.value[:4]}"
            )
        
        lines.extend([
            "",
            "Team Ratings:",
            f"  Keeping: {ratings['keeping']:.1f}",
            f"  Defence: {ratings['defence']:.1f}",
            f"  Midfield: {ratings['midfield']:.1f}",
            f"  Attack: {ratings['attack']:.1f}",
            f"  Left Flow: {ratings['left_flow']:.1f}",
            f"  Center Flow: {ratings['center_flow']:.1f}",
            f"  Right Flow: {ratings['right_flow']:.1f}"
        ])
        
        # Show sent off players if any
        sent_off = self.get_sent_off_players()
        if sent_off:
            lines.append("")
            lines.append("🟥 Sent Off Players:")
            for p in sent_off:
                lines.append(f"  {p.name} ({p.position.name}) - Red Card")
        
        return "\n".join(lines)
    
    def get_nationality_distribution(self) -> Dict[str, int]:
        """Get distribution of nationalities in the team."""
        distribution = {}
        for player in self.players:
            nationality = player.nationality
            distribution[nationality] = distribution.get(nationality, 0) + 1
        return distribution
    
    def get_most_common_nationality(self) -> str:
        """Get the most common nationality in the team."""
        distribution = self.get_nationality_distribution()
        if not distribution:
            return "Unknown"
        return max(distribution.items(), key=lambda x: x[1])[0]
    
    def is_international_team(self) -> bool:
        """Check if team has players from multiple nationalities."""
        return len(self.get_nationality_distribution()) > 1
    
    def get_international_summary(self) -> str:
        """Get a summary of the team's international composition."""
        distribution = self.get_nationality_distribution()
        if len(distribution) <= 1:
            nationality = list(distribution.keys())[0] if distribution else "Unknown"
            return f"Domestic team ({nationality})"
        
        # Sort by count, descending
        sorted_nationalities = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        summary_parts = []
        for nationality, count in sorted_nationalities[:3]:  # Show top 3
            summary_parts.append(f"{nationality}: {count}")
        
        if len(sorted_nationalities) > 3:
            others = sum(count for _, count in sorted_nationalities[3:])
            summary_parts.append(f"Others: {others}")
        
        return f"International team ({', '.join(summary_parts)})"


# Position groupings for team building
POSITION_GROUPS = {
    "Goalkeeper": [Position.GK],
    "Defenders": [Position.CB, Position.SW, Position.LB, Position.RB],
    "Defensive Midfielders": [Position.DM, Position.WB, Position.LWB, Position.RWB],
    "Midfielders": [Position.CM, Position.LM, Position.RM],
    "Attacking Midfielders": [Position.AM],
    "Forwards": [Position.ST, Position.LW, Position.RW],
}

# Common formations with position requirements
FORMATIONS = {
    "4-4-2": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.CM: 2,
        Position.LM: 1,
        Position.RM: 1,
        Position.ST: 2
    },
    "4-3-3": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.CM: 3,
        Position.LW: 1,
        Position.RW: 1,
        Position.ST: 1
    },
    "3-5-2": {
        Position.GK: 1,
        Position.CB: 3,
        Position.CM: 2,
        Position.LWB: 1,
        Position.RWB: 1,
        Position.AM: 1,
        Position.ST: 2
    },
    "4-2-3-1": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.DM: 2,
        Position.AM: 1,
        Position.LW: 1,
        Position.RW: 1,
        Position.ST: 1
    },
    "5-3-2": {
        Position.GK: 1,
        Position.CB: 3,
        Position.LWB: 1,
        Position.RWB: 1,
        Position.CM: 3,
        Position.ST: 2
    },
    "3-4-3": {
        Position.GK: 1,
        Position.CB: 3,
        Position.LM: 1,
        Position.RM: 1,
        Position.CM: 2,
        Position.LW: 1,
        Position.RW: 1,
        Position.ST: 1
    },
    "4-1-4-1": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.DM: 1,
        Position.LM: 1,
        Position.RM: 1,
        Position.CM: 2,
        Position.ST: 1
    },
    "4-5-1": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.LM: 1,
        Position.RM: 1,
        Position.CM: 3,
        Position.ST: 1
    },
    "3-4-2-1": {
        Position.GK: 1,
        Position.CB: 3,
        Position.LM: 1,
        Position.RM: 1,
        Position.CM: 2,
        Position.AM: 2,
        Position.ST: 1
    },
    "4-1-2-1-2": {
        Position.GK: 1,
        Position.CB: 2,
        Position.LB: 1,
        Position.RB: 1,
        Position.DM: 1,
        Position.CM: 2,
        Position.AM: 1,
        Position.ST: 2
    }
}


# Tournament-related data structures
@dataclass
class TournamentMatch:
    """Represents a single match in a tournament."""
    round_name: str
    match_id: str
    home_team: Optional[str]  # Team name or None if TBD
    away_team: Optional[str]  # Team name or None if TBD
    winner: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    completed: bool = False


@dataclass 
class TournamentRound:
    """Represents a round in the tournament."""
    round_name: str
    matches: List[TournamentMatch]
    completed: bool = False


@dataclass
class Tournament:
    """Represents a complete knockout tournament."""
    name: str
    teams: List[str]  # Team names
    rounds: List[TournamentRound]
    current_round: int = 0
    completed: bool = False
    winner: Optional[str] = None
    
    def get_current_round(self) -> Optional[TournamentRound]:
        """Get the current active round."""
        if self.current_round < len(self.rounds):
            return self.rounds[self.current_round]
        return None
    
    def advance_round(self) -> bool:
        """Move to the next round if current is completed."""
        current = self.get_current_round()
        if current and current.completed:
            self.current_round += 1
            if self.current_round >= len(self.rounds):
                self.completed = True
                # Find winner from final match
                final_round = self.rounds[-1]
                if final_round.matches and final_round.matches[0].winner:
                    self.winner = final_round.matches[0].winner
            return True
        return False
