# Fantasy Football Manager - Rich Terminal UI Guide

## Overview

The Rich Terminal UI provides a modern, beautiful command-line interface for Fantasy Football Manager v0.8.0. It features colored tables, progress bars, live match simulation, and an enhanced user experience.

## Features

### 🎨 Visual Enhancements
- **Colored Tables**: League standings with color-coded positions (green for Champions League, red for relegation)
- **Your Team Highlighting**: Your team is highlighted in yellow with blue background
- **Form Display**: Visual representation of recent match results (W/D/L)
- **Box Styles**: Professional borders and panels for better organization

### ⚽ Match Day Experience
- **Match Overview**: See all fixtures at a glance with kick-off times
- **Multiple Viewing Options**:
  - **Simulate All**: Quick results for all matches
  - **Watch All**: Live simulation of every match
  - **Follow Your Team**: Detailed view of only your matches
  - **Choose Matches**: Select specific matches to watch

### 📊 Live Match Simulation
- **Real-time Score Updates**: Watch goals as they happen
- **Match Statistics**: Possession, shots, corners updated live
- **Goal Events**: See who scored and when
- **Progress Timer**: Match minute counter

### 🏆 Season Management
- **Progress Bars**: Visual representation of season completion
- **Quick Stats Panel**: Your position, form, and goal difference at a glance
- **End of Season**: Beautiful presentation of final standings

## Getting Started

### Installation

1. Install the Rich library:
```bash
pip install -r requirements.txt
```

2. Run the Rich UI version:
```bash
python run_rich.py
```

## Usage Guide

### Main Menu
The enhanced main menu presents options in a clean table format:
- `new` - Start a new game
- `load` - Load a saved game
- `help` - View help information
- `exit` - Exit the game

### During Gameplay

#### Match Day Options
When a match day arrives, you'll see:
```
╔════════════════════════════════════════════════════════════╗
║                    MATCH DAY 15                            ║
║                 Saturday, March 15                         ║
╚════════════════════════════════════════════════════════════╝
```

Choose how to experience the matches:
- **S** - Simulate all matches quickly
- **W** - Watch all matches with live updates
- **F** - Follow only your team's match in detail
- **C** - Choose specific matches to watch

#### Viewing Options
- **V** - View detailed standings anytime
- **C** - Continue to next match day
- **S** - Simulate to end of season with progress bar
- **Q** - Save and quit

### League Table

The enhanced league table shows:
- Position with color coding
- Team names with your team highlighted
- Full statistics (MP, W, D, L, GF, GA, GD, Pts)
- Recent form (last 5 matches)

### Live Match Experience

When watching a match, you'll see:
- Live score updates
- Goal events with minute and scorer
- Real-time statistics
- Visual progress indicator

## Keyboard Controls

During live matches:
- **Space** - Pause/Resume
- **F** - Fast forward
- **S** - Skip to end

## Color Scheme

- **Green**: Wins, Champions League positions
- **Yellow**: Draws, your team highlight
- **Red**: Losses, relegation zone
- **Cyan**: Headers, important information
- **Blue**: Selected items, special highlights

## Tips

1. **Best Experience**: Use a terminal that supports full color (most modern terminals)
2. **Terminal Size**: Ensure your terminal is at least 80 characters wide
3. **Font**: Use a monospace font for proper table alignment
4. **Performance**: The Rich UI may be slightly slower than plain text but provides a much better experience

## Troubleshooting

If you experience issues:
1. Ensure Rich is installed: `pip install rich==13.7.0`
2. Check terminal compatibility (some very old terminals may have issues)
3. Try resizing your terminal window if tables appear cut off
4. Fall back to standard UI with `python run.py` if needed

## Future Enhancements

Planned features for future versions:
- Player statistics and ratings
- Transfer market interface
- Tactical formation display
- Match highlights replay
- Season statistics dashboard

---

Enjoy the beautiful game with a beautiful interface! ⚽✨