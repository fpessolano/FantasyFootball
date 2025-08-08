"""
Player Manager - Enhanced
~~~~~~~~~~~~~~~~~~~~~~~~~

Module for creating and managing players with extended attributes.
"""

import json
import random
from pathlib import Path
from typing import List, Optional, Dict
from core.models import Player, Position, TemperamentType

# Import faker name generator with fallback
try:
    from core.generators.name_generator import InternationalNameGenerator
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    print("⚠️  Name generator not available. Run: python dependency_checker.py")


class PlayerManager:
    """Enhanced player manager with extended attributes and migration support."""
    
    def __init__(self, filename: Path | str = Path("data/players.json")):
        self.filename = Path(filename)
        self.players: List[Player] = []
        
        # Initialize name generator if available
        if FAKER_AVAILABLE:
            self.name_generator = InternationalNameGenerator()
        else:
            self.name_generator = None
        
        self.load_players()
    
    def load_players(self) -> None:
        """Load players from JSON file with migration support."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            
            migrated_players = []
            migration_needed = False
            
            for p_data in data:
                try:
                    # Try to load as extended player
                    player = Player.from_dict(p_data)
                    migrated_players.append(player)
                except (KeyError, ValueError) as e:
                    # Migration from legacy format
                    print(f"Migrating legacy player: {p_data.get('name', 'Unknown')}")
                    migrated_player = self._migrate_legacy_player(p_data)
                    if migrated_player:
                        migrated_players.append(migrated_player)
                        migration_needed = True
            
            self.players = migrated_players
            
            # If we migrated any players, save in new format
            if migration_needed:
                print(f"Migrated {len(migrated_players)} players to extended format")
                self.save_players()
                
        except FileNotFoundError:
            self.players = []
    
    def _migrate_legacy_player(self, legacy_data: Dict) -> Optional[Player]:
        """Migrate a legacy player to extended format."""
        try:
            # Create extended player with legacy attributes + reasonable defaults
            return Player(
                name=legacy_data['name'],
                position=Position[legacy_data['position']],
                goalkeeping=legacy_data['goalkeeping'],
                defending=legacy_data['defending'],
                passing=legacy_data['passing'],
                dribbling=legacy_data['dribbling'],
                shooting=legacy_data['shooting'],
                physical=legacy_data['physical'],
                # Generate reasonable defaults for new attributes
                natural_fitness=max(50, min(90, legacy_data['physical'] + random.randint(-10, 10))),
                work_rate=random.randint(40, 80),
                injury_proneness=random.randint(20, 50),
                pressure_handling=random.randint(40, 80),
                concentration=random.randint(45, 75),
                determination=random.randint(40, 80),
                composure=random.randint(40, 75),
                leadership=random.randint(20, 60),
                temperament=random.choice(list(TemperamentType)),
                age=random.randint(20, 32)
            )
        except Exception as e:
            print(f"Failed to migrate player {legacy_data.get('name', 'Unknown')}: {e}")
            return None
    
    def save_players(self) -> None:
        """Save players to JSON file."""
        with open(self.filename, "w") as f:
            json.dump([p.to_dict() for p in self.players], f, indent=2)
    
    def add_player(self, player: Player) -> None:
        """Add a player to the roster."""
        self.players.append(player)
        self.save_players()
    
    def _generate_realistic_name(self, nationality: Optional[str] = None) -> Dict[str, str]:
        """Generate a realistic name and nationality using faker."""
        if self.name_generator is None:
            # Fallback to generic names if faker not available
            generic_names = [
                "John Smith", "Mike Johnson", "David Brown", "Chris Wilson", 
                "Alex Davis", "Matt Miller", "Steve Garcia", "Paul Rodriguez",
                "Mark Martinez", "Tom Anderson", "Dan Thomas", "Joe Jackson"
            ]
            return {
                'full_name': random.choice(generic_names),
                'nationality': 'Unknown'
            }
        
        if nationality:
            # Try to find locale for specific nationality
            locale_map = {
                'Brazilian': 'pt_BR', 'Spanish': 'es_ES', 'French': 'fr_FR',
                'German': 'de_DE', 'Italian': 'it_IT', 'Portuguese': 'pt_PT',
                'British': 'en_GB', 'American': 'en_US', 'Dutch': 'nl_NL',
                'Russian': 'ru_RU', 'Polish': 'pl_PL', 'Swedish': 'sv_SE',
                'Norwegian': 'no_NO', 'Danish': 'da_DK', 'Finnish': 'fi_FI',
                'Japanese': 'ja_JP', 'Korean': 'ko_KR', 'Chinese': 'zh_CN',
                'Turkish': 'tr_TR', 'Greek': 'el_GR', 'Hebrew': 'he_IL'
            }
            locale = locale_map.get(nationality, 'en_US')
            return self.name_generator.generate_name(locale)
        else:
            # Generate random international name
            return self.name_generator.generate_random_name()
    
    def create_random_player(self, position: Optional[Position] = None, 
                           name_prefix: Optional[str] = None) -> Player:
        """Create a random player with extended attributes."""
        if position is None:
            position = random.choice(list(Position))
        
        # Generate realistic name and nationality
        if name_prefix is None:
            name_data = self._generate_realistic_name()
            name = name_data['full_name']
            nationality = name_data['nationality']
        else:
            # If name prefix specified, use it with realistic nationality
            name_data = self._generate_realistic_name()
            name = f"{name_prefix}_{random.randint(100, 999)}"
            nationality = name_data['nationality']
        
        # Generate core attributes based on position
        core_attrs = self._generate_position_attributes(position)
        
        # Generate extended attributes  
        player = Player(
            name=name,
            position=position,
            **core_attrs,
            nationality=nationality,
            # Physical/Mental attributes
            natural_fitness=random.randint(40, 95),
            work_rate=random.randint(30, 90),
            injury_proneness=random.randint(10, 60),
            pressure_handling=random.randint(30, 90),
            concentration=random.randint(40, 85),
            determination=random.randint(30, 90),
            composure=random.randint(35, 85),
            leadership=random.randint(10, 80),
            temperament=random.choice(list(TemperamentType)),
            preferred_foot=random.choice(["left", "right", "both"]),
            age=random.randint(18, 35)
        )
        
        # Adjust some attributes based on age
        if player.age < 22:  # Young players
            player.leadership = max(10, player.leadership - 20)
            player.composure = max(30, player.composure - 15)
            player.natural_fitness += 5  # Young players fitter
        elif player.age > 30:  # Older players
            player.leadership += 15
            player.composure += 10
            player.natural_fitness = max(40, player.natural_fitness - 10)
            
        # Clamp all values to valid ranges
        player.natural_fitness = min(100, max(30, player.natural_fitness))
        player.leadership = min(100, max(0, player.leadership))
        player.composure = min(100, max(20, player.composure))
        
        return player
    
    def _generate_position_attributes(self, position: Position) -> Dict[str, int]:
        """Generate position-appropriate base attributes."""
        if position == Position.GK:
            return {
                'goalkeeping': random.randint(60, 95),
                'defending': random.randint(20, 60),
                'passing': random.randint(40, 80),
                'dribbling': random.randint(20, 50),
                'shooting': random.randint(10, 40),
                'physical': random.randint(50, 85)
            }
        elif position in [Position.CB, Position.SW]:
            return {
                'goalkeeping': random.randint(5, 25),
                'defending': random.randint(70, 95),
                'passing': random.randint(50, 80),
                'dribbling': random.randint(30, 60),
                'shooting': random.randint(20, 50),
                'physical': random.randint(65, 90)
            }
        elif position in [Position.LB, Position.RB]:
            return {
                'goalkeeping': random.randint(5, 20),
                'defending': random.randint(60, 85),
                'passing': random.randint(55, 85),
                'dribbling': random.randint(50, 80),
                'shooting': random.randint(25, 55),
                'physical': random.randint(70, 90)
            }
        elif position in [Position.DM, Position.CM]:
            return {
                'goalkeeping': random.randint(5, 20),
                'defending': random.randint(50, 80),
                'passing': random.randint(70, 95),
                'dribbling': random.randint(60, 85),
                'shooting': random.randint(35, 70),
                'physical': random.randint(60, 85)
            }
        elif position in [Position.LM, Position.RM, Position.LWB, Position.RWB, Position.WB]:
            return {
                'goalkeeping': random.randint(5, 20),
                'defending': random.randint(35, 70),
                'passing': random.randint(60, 85),
                'dribbling': random.randint(65, 90),
                'shooting': random.randint(30, 70),
                'physical': random.randint(65, 90)
            }
        elif position == Position.AM:
            return {
                'goalkeeping': random.randint(5, 20),
                'defending': random.randint(25, 60),
                'passing': random.randint(75, 95),
                'dribbling': random.randint(70, 90),
                'shooting': random.randint(60, 85),
                'physical': random.randint(55, 80)
            }
        else:  # ST, LW, RW
            return {
                'goalkeeping': random.randint(5, 20),
                'defending': random.randint(20, 50),
                'passing': random.randint(50, 80),
                'dribbling': random.randint(65, 90),
                'shooting': random.randint(70, 95),
                'physical': random.randint(65, 90)
            }
    
    def create_manual_player(self) -> Optional[Player]:
        """Create a player through user input with extended attributes."""
        print("\n=== Create New Player ===")
        
        # name = input("Enter player name (or 'q' to go back): ").strip()
        name = input("Enter player name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return None
        if name.lower() in ['q', 'quit', 'back']:
            return None
        
        # Select nationality
        # nationality = input("Enter nationality [Unknown] (or 'q' to go back): ").strip()
        nationality = input("Enter nationality [Unknown]: ").strip()
        if nationality.lower() in ['q', 'quit', 'back']:
            return None
        if not nationality:
            nationality = "Unknown"
        
        # Select position
        print("\nAvailable positions:")
        positions = list(Position)
        for i, pos in enumerate(positions, 1):
            print(f"{i}. {pos.name} - {pos.value}")
        
        try:
            # pos_input = input("Select position (number, or 'q' to go back): ").strip()
            pos_input = input("Select position: ").strip()
            if pos_input.lower() in ['q', 'quit', 'back']:
                return None
            
            pos_idx = int(pos_input) - 1
            if pos_idx < 0 or pos_idx >= len(positions):
                print("Invalid position selection!")
                return None
            position = positions[pos_idx]
        except ValueError:
            print("Invalid input!")
            return None
        
        # Get core attributes
        print("\nEnter core attributes (0-100):")
        try:
            if position == Position.GK:
                goalkeeping = int(input("Goalkeeping: "))
            else:
                goalkeeping = 0
                print("Goalkeeping: 0 (not a goalkeeper)")
            
            defending = int(input("Defending: "))
            passing = int(input("Passing: "))
            dribbling = int(input("Dribbling: "))
            shooting = int(input("Shooting: "))
            physical = int(input("Physical: "))
            
            # Validate ranges
            core_attrs = [goalkeeping, defending, passing, dribbling, shooting, physical]
            if any(a < 0 or a > 100 for a in core_attrs):
                print("All attributes must be between 0 and 100!")
                return None
            
        except ValueError:
            print("Invalid input! Attributes must be numbers.")
            return None
        
        # Get extended attributes with defaults
        print("\nExtended attributes (press Enter for default):")
        try:
            age_input = input(f"Age [25]: ").strip()
            age = int(age_input) if age_input else 25
            if age < 16 or age > 45:
                print("Age must be between 16 and 45!")
                return None
            
            fitness_input = input(f"Natural Fitness [70]: ").strip()
            natural_fitness = int(fitness_input) if fitness_input else 70
            
            work_rate_input = input(f"Work Rate [50]: ").strip()
            work_rate = int(work_rate_input) if work_rate_input else 50
            
            pressure_input = input(f"Pressure Handling [60]: ").strip()
            pressure_handling = int(pressure_input) if pressure_input else 60
            
            # Select temperament
            print("\nTemperament types:")
            temp_types = list(TemperamentType)
            for i, temp in enumerate(temp_types, 1):
                print(f"{i}. {temp.value.replace('_', ' ').title()}")
            
            temp_idx = int(input("Select temperament [2]: ") or "2") - 1
            if temp_idx < 0 or temp_idx >= len(temp_types):
                temperament = TemperamentType.CONSISTENT
            else:
                temperament = temp_types[temp_idx]
            
            # Validate extended attributes
            extended_attrs = [natural_fitness, work_rate, pressure_handling]
            if any(a < 0 or a > 100 for a in extended_attrs):
                print("Extended attributes must be between 0 and 100!")
                return None
            
        except ValueError:
            print("Invalid input! Using defaults for extended attributes.")
            age = 25
            natural_fitness = 70
            work_rate = 50
            pressure_handling = 60
            temperament = TemperamentType.CONSISTENT
        
        # Generate reasonable defaults for remaining extended attributes
        player = Player(
            name=name,
            position=position,
            goalkeeping=goalkeeping,
            defending=defending,
            passing=passing,
            dribbling=dribbling,
            shooting=shooting,
            physical=physical,
            nationality=nationality,
            age=age,
            natural_fitness=natural_fitness,
            work_rate=work_rate,
            pressure_handling=pressure_handling,
            temperament=temperament,
            # Generate reasonable defaults for other extended attributes
            injury_proneness=random.randint(20, 50),
            concentration=random.randint(45, 75),
            determination=random.randint(40, 80),
            composure=random.randint(40, 75),
            leadership=random.randint(20, 60) if age > 25 else random.randint(10, 40),
            preferred_foot=random.choice(["left", "right"])
        )
        
        return player
    
    def generate_player_pool(self, count: int, ensure_all_positions: bool = True) -> List[Player]:
        """Generate a pool of random players with extended attributes."""
        players = []
        
        if ensure_all_positions and count >= len(list(Position)):
            # Ensure at least 1 player per position if we have enough slots
            positions = list(Position)
            for pos in positions:
                players.append(self.create_random_player(pos))
            
            # Fill remaining slots randomly  
            while len(players) < count:
                players.append(self.create_random_player())
        else:
            # Generate completely random players
            for _ in range(count):
                players.append(self.create_random_player())
        
        return players
    
    def find_players_by_position(self, position: Position) -> List[Player]:
        """Find all players with a specific position."""
        return [p for p in self.players if p.position == position]
    
    def find_players_by_name(self, name_part: str) -> List[Player]:
        """Find players whose name contains the given string."""
        name_lower = name_part.lower()
        return [p for p in self.players if name_lower in p.name.lower()]
    
    def get_top_players(self, count: int = 10) -> List[Player]:
        """Get top players by overall rating."""
        return sorted(self.players, key=lambda p: p.overall_rating(), reverse=True)[:count]
    
    def create_player_by_nationality(self, position: Optional[Position] = None, 
                                   nationality: str = "Brazilian") -> Player:
        """Create a player with a specific nationality."""
        if position is None:
            position = random.choice(list(Position))
        
        # Generate name for specific nationality
        name_data = self._generate_realistic_name(nationality)
        
        # Generate core attributes based on position
        core_attrs = self._generate_position_attributes(position)
        
        player = Player(
            name=name_data['full_name'],
            position=position,
            **core_attrs,
            nationality=name_data['nationality'],
            # Physical/Mental attributes
            natural_fitness=random.randint(40, 95),
            work_rate=random.randint(30, 90),
            injury_proneness=random.randint(10, 60),
            pressure_handling=random.randint(30, 90),
            concentration=random.randint(40, 85),
            determination=random.randint(30, 90),
            composure=random.randint(35, 85),
            leadership=random.randint(10, 80),
            temperament=random.choice(list(TemperamentType)),
            preferred_foot=random.choice(["left", "right", "both"]),
            age=random.randint(18, 35)
        )
        
        # Age-based adjustments (same as create_random_player)
        if player.age < 22:
            player.natural_fitness = min(95, player.natural_fitness + 5)
            player.injury_proneness = max(10, player.injury_proneness - 10)
        elif player.age > 30:
            player.natural_fitness = max(40, player.natural_fitness - 10)
            player.injury_proneness = min(60, player.injury_proneness + 15)
        
        return player
    
    def generate_international_squad(self, count: int = 25) -> List[Player]:
        """Generate a diverse international squad with players from various nationalities."""
        players = []
        
        # Major football nations with rough distribution
        nationality_weights = [
            ('Brazilian', 0.15),
            ('Spanish', 0.12),
            ('French', 0.12), 
            ('German', 0.10),
            ('Italian', 0.10),
            ('English', 0.08),
            ('Portuguese', 0.08),
            ('Dutch', 0.06),
            ('American', 0.05),
            ('Polish', 0.04),
            ('Russian', 0.04),
            ('Swedish', 0.03),
            ('Norwegian', 0.03)
        ]
        
        # Generate players with weighted nationality distribution
        for _ in range(count):
            nationality = random.choices(
                [n for n, _ in nationality_weights],
                weights=[w for _, w in nationality_weights],
                k=1
            )[0]
            players.append(self.create_player_by_nationality(None, nationality))
        
        return players
    
    def generate_national_team(self, nationality: str = "Brazilian", count: int = 23) -> List[Player]:
        """Generate a national team with players all from the same country."""
        players = []
        
        # Ensure at least 1 player per position for core positions
        essential_positions = [Position.GK, Position.CB, Position.CM, Position.ST]
        for pos in essential_positions:
            players.append(self.create_player_by_nationality(pos, nationality))
        
        # Add more players to reach desired count
        while len(players) < count:
            players.append(self.create_player_by_nationality(None, nationality))
        
        return players
    
    def find_players_by_nationality(self, nationality: str) -> List[Player]:
        """Find all players with a specific nationality."""
        return [p for p in self.players if p.nationality.lower().strip() == nationality.lower().strip()]
    
    def get_nationality_distribution(self) -> Dict[str, int]:
        """Get distribution of nationalities in the player database."""
        from collections import Counter
        return dict(Counter(player.nationality for player in self.players))
    
    def display_player_stats(self, player: Player) -> None:
        """Display detailed player statistics with extended attributes."""
        print(f"\n{'='*70}")
        print(f"Name: {player.name}")
        print(f"Position: {player.position.value}")
        print(f"Age: {player.age}")
        print(f"Overall Rating: {player.overall_rating():.0f}")
        print(f"Temperament: {player.temperament.value.replace('_', ' ').title()}")
        print(f"Preferred Foot: {player.preferred_foot.title()}")
        
        print(f"\nCore Attributes:")
        print(f"  Goalkeeping: {player.goalkeeping:3d}")
        print(f"  Defending:   {player.defending:3d}")
        print(f"  Passing:     {player.passing:3d}")
        print(f"  Dribbling:   {player.dribbling:3d}")
        print(f"  Shooting:    {player.shooting:3d}")
        print(f"  Physical:    {player.physical:3d}")
        
        print(f"\nPhysical & Mental:")
        print(f"  Natural Fitness:   {player.natural_fitness:3d}")
        print(f"  Work Rate:         {player.work_rate:3d}")
        print(f"  Injury Proneness:  {player.injury_proneness:3d}")
        print(f"  Pressure Handling: {player.pressure_handling:3d}")
        print(f"  Concentration:     {player.concentration:3d}")
        print(f"  Determination:     {player.determination:3d}")
        print(f"  Composure:         {player.composure:3d}")
        print(f"  Leadership:        {player.leadership:3d}")
        
        print(f"\nCurrent Status:")
        print(f"  Stamina:     {player.current_stamina:5.1f}%")
        print(f"  Form Rating: {player.form.base_form:5.1f}/10")
        print(f"  Confidence:  {player.form.confidence:5.1f}%")
        
        print(f"{'='*70}")
    
    def get_players_by_fitness_status(self) -> Dict[str, List[Player]]:
        """Group players by their fitness status."""
        categories = {
            "Fully Fit": [],      # 90%+ stamina
            "Good Shape": [],     # 70-89% stamina
            "Tired": [],          # 50-69% stamina
            "Exhausted": []       # <50% stamina
        }
        
        for player in self.players:
            if player.current_stamina >= 90:
                categories["Fully Fit"].append(player)
            elif player.current_stamina >= 70:
                categories["Good Shape"].append(player)
            elif player.current_stamina >= 50:
                categories["Tired"].append(player)
            else:
                categories["Exhausted"].append(player)
        
        return categories
    
    def rest_all_players(self, hours: float = 24):
        """Apply rest recovery to all players."""
        from performance_system import RecoverySystem
        recovery_system = RecoverySystem()
        
        print(f"\nApplying {hours} hours of rest to all players...")
        recovered_count = 0
        
        for player in self.players:
            old_stamina = player.current_stamina
            recovery_system.calculate_recovery(player, hours, "full_rest")
            if player.current_stamina > old_stamina:
                recovered_count += 1
        
        self.save_players()
        print(f"✅ {recovered_count} players recovered stamina")
