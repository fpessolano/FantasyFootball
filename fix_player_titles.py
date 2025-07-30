#!/usr/bin/env python3
"""
Fix player names by removing professional titles.
"""

from player_manager import PlayerManager

def fix_player_titles():
    """Remove professional titles from player names."""
    pm = PlayerManager('players.json')
    
    # Define titles to remove
    titles_to_remove = ['Av.', 'Dr.', 'Mr.', 'Ms.', 'Prof.', 'Sr.', 'Jr.', 'Univ.Prof.', 
                       'Yrd. Doç.', 'Doç.', 'Arş. Gör.', 'Öğr. Gör.']
    
    # Find and fix players with titles
    fixed_count = 0
    for player in pm.players:
        original_name = player.name
        cleaned_name = original_name
        
        # Remove titles from the beginning of names
        for title in titles_to_remove:
            if cleaned_name.startswith(title + ' '):
                cleaned_name = cleaned_name[len(title + ' '):]
                
        # Also handle titles in the middle (like 'Univ.Prof.')
        for title in titles_to_remove:
            if title + ' ' in cleaned_name:
                cleaned_name = cleaned_name.replace(title + ' ', '')
        
        if cleaned_name != original_name:
            print(f'Fixed: "{original_name}" -> "{cleaned_name}"')
            player.name = cleaned_name
            fixed_count += 1
    
    print(f'\nFixed {fixed_count} player names')
    
    # Save the changes
    pm.save_players()
    print('Changes saved to players.json')

if __name__ == "__main__":
    fix_player_titles()