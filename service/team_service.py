#!/usr/bin/env python3
"""
Team Menu - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all team management functionality.
"""

from core.models import TacticalStyle
from interface.cli_interface import CLIInterface
from interface.constants import TEAM_MENU


class TeamService:
    """Service for team management operations."""
    
    def __init__(self, team_manager, player_manager):
        self.team_manager = team_manager
        self.player_manager = player_manager
        self.cli = CLIInterface()
    
    def show_menu(self):
        """Display team management submenu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    TEAM_MENU, 
                    "TEAM MANAGEMENT"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(TEAM_MENU) - 1:  # Back to Main Menu
                    break
                
                # Handle menu choices
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice."""
        if choice == 0:  # View All Teams
            self.view_all_teams()
            input("\nPress Enter to continue...")
        elif choice == 1:  # Create Random Team
            self.create_random_team()
            input("\nPress Enter to continue...")
        elif choice == 2:  # Create Manual Team
            self.create_manual_team()
            input("\nPress Enter to continue...")
        elif choice == 3:  # Create National Team
            self.create_national_team()
            input("\nPress Enter to continue...")
        elif choice == 4:  # Create Mixed Nationality Team
            self.create_mixed_nationality_team()
            input("\nPress Enter to continue...")
        elif choice == 5:  # Create Continental Team
            self.create_continental_team()
            input("\nPress Enter to continue...")
        elif choice == 6:  # View Team Details
            self.view_team_details()
            input("\nPress Enter to continue...")
        elif choice == 7:  # Modify Team
            self.modify_team()
        elif choice == 8:  # Delete Team
            self.delete_team()
            input("\nPress Enter to continue...")
        elif choice == 9:  # Check Nationality Availability
            self.check_nationality_availability()
            input("\nPress Enter to continue...")
    
    def view_all_teams(self):
        """Display all teams."""
        if not self.team_manager.teams:
            print("\nNo teams found!")
            return
        
        self.team_manager.display_team_rankings()
    
    def create_random_team(self):
        """Create a random team."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        name = input("Enter team name (or 'q' to go back): ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        if name.lower() in ['q', 'quit', 'back']:
            return
        
        team = self.team_manager.create_random_team(
            name, self.player_manager.players
        )
        
        if team:
            self.team_manager.add_team(team)
            print(team.summary())
            print("\nTeam created successfully!")
    
    def create_manual_team(self):
        """Create a team manually."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        team = self.team_manager.create_manual_team(self.player_manager.players)
        
        if team:
            self.team_manager.add_team(team)
            print(team.summary())
            print("\nTeam created successfully!")
    
    def create_national_team(self):
        """Create a team with players all from the same nationality."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        # Show available nationalities
        distribution = self.player_manager.get_nationality_distribution()
        print("\n=== Available Nationalities ===")
        sorted_nationalities = sorted(distribution.items())
        for i, (nationality, count) in enumerate(sorted_nationalities, 1):
            print(f"{i:2}. {nationality}: {count} players")
        
        nationality_input = input("\nEnter nationality (name or number, or 'q' to go back): ").strip()
        if not nationality_input:
            print("Nationality cannot be empty!")
            return
        if nationality_input.lower() in ['q', 'quit', 'back']:
            return
        
        # Check if input is a number
        nationality = None
        try:
            choice_num = int(nationality_input)
            if 1 <= choice_num <= len(sorted_nationalities):
                nationality = sorted_nationalities[choice_num - 1][0]
            else:
                print(f"Invalid choice! Please select 1-{len(sorted_nationalities)}")
                return
        except ValueError:
            # Input is a nationality name
            nationality = nationality_input
        
        # Check if national team is possible
        can_create, reason = self.team_manager.can_create_national_team(nationality, self.player_manager.players)
        
        create_missing = False
        if not can_create:
            print(f"\n❌ Cannot create national team: {reason}")
            
            # Ask if user wants to create missing players
            response = input("\nWould you like to create missing players to complete the team? (y/n, or 'q' to go back): ").strip().lower()
            if response in ['q', 'quit', 'back']:
                return
            elif response in ['y', 'yes']:
                create_missing = True
                print("✅ Will create missing players as needed.")
            else:
                return
        
        name = input(f"Enter team name [{nationality} FC] (or 'q' to go back): ").strip()
        if name.lower() in ['q', 'quit', 'back']:
            return
        if not name:
            name = f"{nationality} FC"
        
        # Select formation
        from core.models import FORMATIONS
        formations = list(FORMATIONS.keys())
        print("\nAvailable formations:")
        for i, formation in enumerate(formations, 1):
            print(f"{i}. {formation}")
        
        try:
            formation_input = input("Select formation (number, or 'q' to go back): ").strip()
            if formation_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(formation_input)
            if 1 <= choice <= len(formations):
                formation = formations[choice - 1]
            else:
                formation = "4-3-3"
        except ValueError:
            formation = "4-3-3"
        
        # Select tactical style
        from core.models import TacticalStyle
        styles = list(TacticalStyle)
        print("\nAvailable tactical styles:")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            style_input = input("Select tactical style (number, or 'q' to go back): ").strip()
            if style_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(style_input)
            if 1 <= choice <= len(styles):
                tactical_style = styles[choice - 1]
            else:
                tactical_style = TacticalStyle.BALANCED
        except ValueError:
            tactical_style = TacticalStyle.BALANCED
        
        team = self.team_manager.create_national_team(name, nationality, self.player_manager.players, formation, tactical_style, create_missing)
        
        if team:
            self.team_manager.add_team(team)
            print(f"\n✅ {nationality} national team created successfully!")
            print(team.summary())
        else:
            print(f"\n❌ Failed to create {nationality} national team.")
    
    def create_mixed_nationality_team(self):
        """Create a team with a specific mix of nationalities."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        # Show available nationalities with IDs
        distribution = self.player_manager.get_nationality_distribution()
        print("\n=== Available Nationalities ===")
        sorted_nationalities = sorted(distribution.items())
        for i, (nationality, count) in enumerate(sorted_nationalities, 1):
            print(f"{i:2}. {nationality}: {count} players")
        
        name = input("\nEnter team name (or 'q' to go back): ").strip()
        if not name:
            print("Team name cannot be empty!")
            return
        if name.lower() in ['q', 'quit', 'back']:
            return
        
        print("\nSpecify nationality requirements (minimum players per nationality)")
        print("Format: 'ID:count ID:count' (e.g., '12:4 11:3 17:2') or leave empty to finish")
        print("Example: 2:5 12:3 (Brazilian:5 German:3)")
        
        nationality_mix = {}
        while True:
            req = input("Enter requirement (or press Enter to finish, 'q' to go back): ").strip()
            if not req:
                break
            if req.lower() in ['q', 'quit', 'back']:
                return
            
            # Parse space-separated ID:count pairs
            pairs = req.split()
            added_any = False
            
            for pair in pairs:
                try:
                    parts = pair.split(':')
                    if len(parts) == 2:
                        nat_id = int(parts[0].strip())
                        count = int(parts[1].strip())
                        
                        # Validate nationality ID
                        if 1 <= nat_id <= len(sorted_nationalities):
                            nationality = sorted_nationalities[nat_id - 1][0]
                            if count > 0:
                                nationality_mix[nationality] = count
                                print(f"✅ Added: {nationality} (ID {nat_id}) - {count} players")
                                added_any = True
                            else:
                                print(f"Count must be positive for ID {nat_id}!")
                        else:
                            print(f"Invalid nationality ID: {nat_id}! Use 1-{len(sorted_nationalities)}")
                    else:
                        print(f"Invalid format in '{pair}'! Use 'ID:Count'")
                except ValueError:
                    print(f"Invalid format in '{pair}'! Use numbers only (e.g., '12:4')")
            
            if not added_any and req:
                print("No valid requirements added. Try format: '12:4 17:3' (ID:count pairs)")
        
        if not nationality_mix:
            print("No nationality requirements specified!")
            return
        
        # Select formation
        from core.models import FORMATIONS
        formations = list(FORMATIONS.keys())
        print("\nAvailable formations:")
        for i, formation in enumerate(formations, 1):
            print(f"{i}. {formation}")
        
        try:
            formation_input = input("Select formation (number, or 'q' to go back): ").strip()
            if formation_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(formation_input)
            if 1 <= choice <= len(formations):
                formation = formations[choice - 1]
            else:
                formation = "4-3-3"
        except ValueError:
            formation = "4-3-3"
        
        # Select tactical style
        from core.models import TacticalStyle
        styles = list(TacticalStyle)
        print("\nAvailable tactical styles:")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            style_input = input("Select tactical style (number, or 'q' to go back): ").strip()
            if style_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(style_input)
            if 1 <= choice <= len(styles):
                tactical_style = styles[choice - 1]
            else:
                tactical_style = TacticalStyle.BALANCED
        except ValueError:
            tactical_style = TacticalStyle.BALANCED
        
        # First try without creating missing players
        team = self.team_manager.create_mixed_nationality_team(name, nationality_mix, self.player_manager.players, formation, tactical_style)
        
        if not team:
            # Ask if user wants to create missing players
            response = input("\nWould you like to create missing players to complete the team? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ Will create missing players as needed.")
                team = self.team_manager.create_mixed_nationality_team(name, nationality_mix, self.player_manager.players, formation, tactical_style, True)
        
        if team:
            self.team_manager.add_team(team)
            print(f"\n✅ Mixed nationality team '{name}' created successfully!")
            print(team.summary())
        else:
            print(f"\n❌ Failed to create mixed nationality team.")
    
    def create_continental_team(self):
        """Create a team with minimum players from a specific continent."""
        if len(self.player_manager.players) < 11:
            print("\nNot enough players! Generate more players first.")
            return
        
        continents = ["Europe", "Americas", "Asia"]
        print("\n=== Available Continents ===")
        print("1. Europe (23 countries)")
        print("2. Americas (2 countries)")  
        print("3. Asia (3 countries)")
        
        try:
            continent_input = input("Select continent (1-3, or 'q' to go back): ").strip()
            if continent_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(continent_input)
            if 1 <= choice <= 3:
                continent = continents[choice - 1]
            else:
                print("Invalid choice!")
                return
        except ValueError:
            print("Invalid input!")
            return
        
        name = input(f"\nEnter team name [{continent} FC] (or 'q' to go back): ").strip()
        if name.lower() in ['q', 'quit', 'back']:
            return
        if not name:
            name = f"{continent} FC"
        
        try:
            min_input = input(f"Minimum players from {continent} (1-11, or 'q' to go back): ").strip()
            if min_input.lower() in ['q', 'quit', 'back']:
                return
            
            min_players = int(min_input)
            if not 1 <= min_players <= 11:
                print("Must be between 1 and 11!")
                return
        except ValueError:
            print("Invalid number!")
            return
        
        # Select formation
        from core.models import FORMATIONS
        formations = list(FORMATIONS.keys())
        print("\nAvailable formations:")
        for i, formation in enumerate(formations, 1):
            print(f"{i}. {formation}")
        
        try:
            formation_input = input("Select formation (number, or 'q' to go back): ").strip()
            if formation_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(formation_input)
            if 1 <= choice <= len(formations):
                formation = formations[choice - 1]
            else:
                formation = "4-3-3"
        except ValueError:
            formation = "4-3-3"
        
        # Select tactical style
        from core.models import TacticalStyle
        styles = list(TacticalStyle)
        print("\nAvailable tactical styles:")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            style_input = input("Select tactical style (number, or 'q' to go back): ").strip()
            if style_input.lower() in ['q', 'quit', 'back']:
                return
            
            choice = int(style_input)
            if 1 <= choice <= len(styles):
                tactical_style = styles[choice - 1]
            else:
                tactical_style = TacticalStyle.BALANCED
        except ValueError:
            tactical_style = TacticalStyle.BALANCED
        
        # First try without creating missing players
        team = self.team_manager.create_continental_team(name, continent, min_players, self.player_manager.players, formation, tactical_style)
        
        if not team:
            # Ask if user wants to create missing players
            response = input("\nWould you like to create missing players to complete the team? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ Will create missing players as needed.")
                team = self.team_manager.create_continental_team(name, continent, min_players, self.player_manager.players, formation, tactical_style, True)
        
        if team:
            self.team_manager.add_team(team)
            print(f"\n✅ Continental team '{name}' created successfully!")
            print(team.summary())
        else:
            print(f"\n❌ Failed to create continental team.")
    
    def check_nationality_availability(self):
        """Check availability of players by nationality for team creation."""
        print("\n=== Nationality Availability Analysis ===")
        
        # Get availability data
        availability = self.team_manager.get_nationality_availability(self.player_manager.players)
        
        if not availability:
            print("No players available!")
            return
        
        # Show overall nationality distribution
        print("\n📊 Available Players by Nationality:")
        nationality_totals = {}
        for nat, positions in availability.items():
            nationality_totals[nat] = sum(positions.values())
        
        # Sort by total players
        sorted_nationalities = sorted(nationality_totals.items(), key=lambda x: x[1], reverse=True)
        
        for nat, total in sorted_nationalities:
            print(f"   {nat:15}: {total:2} players")
        
        # Check which nationalities can form complete teams
        print("\n⚽ National Team Feasibility (4-3-3 formation):")
        for nationality, _ in sorted_nationalities[:10]:  # Check top 10
            can_create, reason = self.team_manager.can_create_national_team(nationality, self.player_manager.players, "4-3-3")
            status = "✅" if can_create else "❌"
            print(f"   {status} {nationality:15}: {reason}")
        
        # Show detailed position breakdown for selected nationality
        print(f"\nFor detailed position breakdown, enter a nationality:")
        selected = input("Nationality (or press Enter to skip): ").strip()
        
        if selected and selected in availability:
            print(f"\n🔍 {selected} Position Breakdown:")
            positions = availability[selected]
            for pos, count in sorted(positions.items()):
                print(f"   {pos:3}: {count} players")
    
    def view_team_details(self):
        """View detailed team information."""
        team = self._select_team_by_number("Select team to view")
        if not team:
            return
        
        print(team.summary())
    
    def modify_team(self):
        """Modify an existing team."""
        team = self._select_team_by_number("Select team to modify")
        if not team:
            return
        
        try:
            while True:
                print("=" * 60)
                print(f"MODIFY TEAM: {team.name}")
                print("=" * 60)
                print("\n1. Change Team Name")
                print("2. Change Formation")
                print("3. Change Tactical Style")
                print("4. Replace Player")
                print("5. Modify by Nationality")
                print("6. View Current Team")
                print("7. View Team Nationality Analysis")
                print("0. Back")
                print("\n" + "=" * 60)
                
                choice = input("\nEnter choice: ").strip()
                
                if choice == "1":
                    self._change_team_name(team)
                elif choice == "2":
                    self._change_team_formation(team)
                elif choice == "3":
                    self._change_team_style(team)
                elif choice == "4":
                    self._replace_team_player(team)
                elif choice == "5":
                    self._modify_team_by_nationality(team)
                elif choice == "6":
                    print(team.summary())
                    input("\nPress Enter to continue...")
                elif choice == "7":
                    self._view_team_nationality_analysis(team)
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
                    input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\nReturning to team menu...")
            return
    
    def delete_team(self):
        """Delete a team."""
        team = self._select_team_by_number("Select team to delete")
        if not team:
            return
        
        confirm = input(f"\nDelete team '{team.name}'? (y/N, or 'q' to go back): ").strip().lower()
        if confirm.lower() in ['q', 'quit', 'back']:
            return
        elif confirm == 'y':
            self.team_manager.teams.remove(team)
            self.team_manager.save_teams()
            print("Team deleted!")
    
    def _select_team_by_number(self, prompt: str = "Select team"):
        """Helper method to select a team by number with list display."""
        if not self.team_manager.teams:
            print("\nNo teams found!")
            return None
        
        print("\nAvailable teams:")
        for i, team in enumerate(self.team_manager.teams, 1):
            print(f"{i}. {team.name}")
        
        try:
            team_input = input(f"\n{prompt} (1-{len(self.team_manager.teams)}, or 'q' to go back): ").strip()
            if team_input.lower() in ['q', 'quit', 'back']:
                return None
            
            choice = int(team_input)
            if not (1 <= choice <= len(self.team_manager.teams)):
                print("Invalid choice!")
                return None
            
            return self.team_manager.teams[choice - 1]
        except ValueError:
            print("Invalid input!")
            return None
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
    
    def _change_team_name(self, team):
        """Change team name."""
        new_name = input(f"Enter new name for '{team.name}': ").strip()
        if new_name and new_name != team.name:
            old_name = team.name
            team.name = new_name
            self.team_manager.save_teams()
            print(f"Team renamed from '{old_name}' to '{new_name}'!")
        else:
            print("Name unchanged.")
        input("\nPress Enter to continue...")
    
    def _change_team_formation(self, team):
        """Change team formation."""
        from models import FORMATIONS
        formations = list(FORMATIONS.keys())
        print(f"\nCurrent formation: {team.formation}")
        print("\nAvailable formations:")
        for i, formation in enumerate(formations, 1):
            print(f"{i}. {formation}")
        
        try:
            choice = int(input("Select new formation (number): "))
            if 1 <= choice <= len(formations):
                new_formation = formations[choice - 1]
                if new_formation != team.formation:
                    team.formation = new_formation
                    team.assign_positions()  # Reassign positions based on new formation
                    self.team_manager.save_teams()
                    print(f"Formation changed to {new_formation}!")
                else:
                    print("Formation unchanged.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        input("\nPress Enter to continue...")
    
    def _change_team_style(self, team):
        """Change team tactical style."""
        styles = list(TacticalStyle)
        print(f"\nCurrent style: {team.style.name}")
        print("\nAvailable styles:")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style.name}")
        
        try:
            choice = int(input("Select new style (number): "))
            if 1 <= choice <= len(styles):
                new_style = styles[choice - 1]
                if new_style != team.style:
                    team.style = new_style
                    self.team_manager.save_teams()
                    print(f"Tactical style changed to {new_style.name}!")
                else:
                    print("Style unchanged.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        input("\nPress Enter to continue...")
    
    def _replace_team_player(self, team):
        """Replace a player in the team."""
        print("\nCurrent team players:")
        for i, player in enumerate(team.players, 1):
            print(f"{i:2}. {player.name} ({player.position.name}) - {player.nationality}")
        
        try:
            player_idx = int(input("Select player to replace (number): ")) - 1
            if not (0 <= player_idx < len(team.players)):
                print("Invalid choice!")
                return
        except ValueError:
            print("Invalid input!")
            return
        
        old_player = team.players[player_idx]
        position = old_player.position
        
        # Find available replacement players
        available_players = [p for p in self.player_manager.players 
                           if p.position == position and p not in team.players]
        
        if not available_players:
            print(f"No available {position.name} players for replacement!")
            return
        
        print(f"\nAvailable {position.name} players:")
        for i, player in enumerate(available_players[:20], 1):  # Show top 20
            print(f"{i:2}. {player.name} ({player.nationality}) - OVR: {player.overall_rating():.0f}")
        
        try:
            choice = int(input("Select replacement player (number): ")) - 1
            if not (0 <= choice < len(available_players)):
                print("Invalid choice!")
                return
        except ValueError:
            print("Invalid input!")
            return
        
        new_player = available_players[choice]
        team.players[player_idx] = new_player
        self.team_manager.save_teams()
        
        print(f"Replaced {old_player.name} with {new_player.name}!")
        input("\nPress Enter to continue...")
    
    def _modify_team_by_nationality(self, team):
        """Modify team based on nationality requirements."""
        print("This feature would allow complex nationality-based team modifications.")
        print("Implementation would include options to:")
        print("- Set minimum players per nationality")
        print("- Convert to national team")
        print("- Balance nationality distribution")
        input("\nPress Enter to continue...")
    
    def _view_team_nationality_analysis(self, team):
        """View detailed nationality analysis of the team."""
        from collections import defaultdict
        
        nationality_count = defaultdict(int)
        for player in team.players:
            nationality_count[player.nationality] += 1
        
        print(f"\n=== {team.name} Nationality Analysis ===")
        print(f"Total players: {len(team.players)}")
        print("\nNationality breakdown:")
        
        for nationality, count in sorted(nationality_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(team.players)) * 100
            print(f"  {nationality:15}: {count:2} players ({percentage:5.1f}%)")
        
        input("\nPress Enter to continue...")