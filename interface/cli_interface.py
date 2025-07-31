#!/usr/bin/env python3
"""
CLI Interface
~~~~~~~~~~~~~

Command line interface utilities for creating interactive menus.
"""

import os
from typing import List, Dict, Optional


class CLIInterface:
    """Command line interface for menu interactions."""
    
    def __init__(self):
        self._menus: Dict[int, Dict[str, any]] = {}
        self._next_id = 1
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause_and_clear(self, message="Press Enter to continue..."):
        """Pause for user input then clear screen."""
        input("\n"+message)
        self.clear_screen()
    
    def add_menu(self, options: List[str], title: str = None) -> int:
        if not options:
            raise ValueError("Options list cannot be empty")
        
        menu_id = self._next_id
        self._next_id += 1
        
        self._menus[menu_id] = {
            'title': title,
            'options': options.copy()
        }
        return menu_id
    
    def remove_menu(self, menu_id: int):
        if menu_id in self._menus:
            del self._menus[menu_id]
    
    def get_menu_options(self, menu_id: int) -> Optional[List[str]]:
        menu = self._menus.get(menu_id)
        return menu['options'].copy() if menu else None
    
    def get_menu_title(self, menu_id: int) -> Optional[str]:
        menu = self._menus.get(menu_id)
        return menu['title'] if menu else None
    
    def list_menus(self) -> List[int]:
        return list(self._menus.keys())
    
    def display_menu(self, menu_id: int) -> int:
        if menu_id not in self._menus:
            raise ValueError(f"Menu '{menu_id}' not found")
        
        menu = self._menus[menu_id]
        return self.display_menu_and_select(menu['options'], menu['title'])
    
    def display_menu_and_select(self, options: List[str], title: str = None) -> int:
        if not options:
            raise ValueError("Options list cannot be empty")
        
        self.clear_screen()
        
        if title:
            print("=" * 60)
            print(title)
        print("=" * 60)
        print()
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("\n" + "="*60)
        
        while True:
            try:
                choice = input("Enter your choice: ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(options):
                    return choice_num - 1
                print(f"Please enter a number between 1 and {len(options)}")    
            except ValueError:
                print("Please enter a valid number")
            except (EOFError, KeyboardInterrupt):
                print("\n\nGracefully exiting Fantasy Football Manager...")
                print("Thank you for playing!")
                quit()