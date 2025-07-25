# Data Sources for Fantasy Football Manager

This document explains how to set up automatic weekly team rating updates for the Fantasy Football Manager.

## Overview

The game automatically checks for updated team ratings every week. When new data is available, it updates the ELO scores to reflect current team performance.

## Setting Up Data Updates

### Method 1: EA Sports FC 25 Data (Recommended)

1. **Download the dataset**:
   - Visit [Kaggle EA Sports FC 25 Dataset](https://www.kaggle.com/datasets/nyagami/ea-sports-fc-25-database-ratings-and-stats)
   - Create a free Kaggle account if you don't have one
   - Download the `male_teams.csv` file

2. **Place the file**:
   - Rename the downloaded file to `ea_sports_fc_25_teams.csv`
   - Place it in the `assets/data/` directory of your Fantasy Football Manager installation
   - The game will automatically detect and use this file for weekly updates

3. **File structure should look like**:
   ```
   FantasyFootball/
   ├── assets/
   │   ├── data/
   │   │   └── ea_sports_fc_25_teams.csv  ← Place here
   │   └── raw/
   │       └── male_teams.csv             ← Original data
   └── ...
   ```

### Method 2: Manual Updates

If you don't want to use automatic updates, the game will continue to work with the existing team data. The ratings will remain static but fully functional.

## How Updates Work

1. **Weekly Check**: Every 7 days, the game automatically checks if new data is available
2. **Backup Creation**: Before updating, the game creates a backup of current ratings
3. **Silent Updates**: Updates happen silently unless new data is actually applied
4. **Notification**: If ratings are updated, you'll see a brief message: "📈 Team ratings have been updated with latest data"

## Data Sources Information

### Primary Sources
- **EA Sports FC 25**: Official game ratings from EA Sports (via Kaggle)
- **FIFA Index**: Community-maintained database (backup method)

### Alternative Sources (For Advanced Users)
- **Club ELO**: Professional club ratings (clubelo.com)
- **SoccerData Library**: Python library for multiple data sources
- **Custom CSV**: You can create your own team ratings file

## File Formats

The system expects CSV files with these columns:
- `team_name`: Official team name
- `overall`: Team overall rating (0-100)
- `fifa_version`: Version identifier (e.g., 24.0)
- `league_name`: League/competition name
- `nationality_name`: Country/region

## Advanced ELO Rating System

The game features a sophisticated ELO estimation system that handles missing data intelligently:

### Smart ELO Estimation
When ELO scores are not available, the system uses **similarity matching** with teams that have known ratings:

1. **Multi-Metric Analysis**: Uses overall rating, attack, midfield, defense, prestige, and financial data
2. **League Context**: Prioritizes teams from the same league/country for more accurate estimates
3. **Similarity Matching**: Finds teams with similar characteristics and calculates weighted averages
4. **Confidence Scoring**: Provides estimation confidence (high/medium/low) based on available data

### Estimation Methods (in priority order)
1. **Overall Rating Similarity**: Matches teams with similar overall ratings
2. **Multi-Metric Similarity**: Comprehensive analysis using all available team stats
3. **League Context**: Uses league average and relative team position
4. **Prestige Similarity**: Based on international/domestic prestige and club worth

### Realistic Conversion Scale
- **FIFA Overall 0-45** → **ELO 1000-1200** (very weak teams)
- **FIFA Overall 45-85** → **ELO 1200-1800** (normal distribution)
- **FIFA Overall 85-100** → **ELO 1800-2000** (elite teams)

**Specific Examples:**
- Overall 45 = ELO 1200 (weak team)
- Overall 55 = ELO 1350 (below average)
- Overall 65 = ELO 1500 (average team)
- Overall 75 = ELO 1650 (strong team)
- Overall 85 = ELO 1800 (elite team)
- Overall 95 = ELO 1933 (world class)

### Conservative Fallback Hierarchy
- **Complete Data**: Realistic conversion based on bell curve distribution
- **Missing Overall**: Estimated using attack/midfield/defense with penalty → ELO ~1433
- **Prestige Only**: Conservative prestige mapping → ELO 1150-1650
- **League Level**: Competition tier estimate → ELO 1200-1450
- **Minimal Data**: Conservative default → ELO 1350 (below average)

### Automatic Fallbacks
- **Missing ELO**: Advanced estimation or 1350 conservative default
- **Invalid data**: Any non-numeric values become 1350
- **Out of range**: Values are clamped to 1000-2000 range
- **Incomplete data**: Penalty applied for missing metrics
- **Unknown teams**: Conservative estimate below average

### Error Handling
- **Corrupt data**: Individual teams skipped, process continues
- **Missing files**: Game uses existing ratings
- **Network issues**: Local data always available
- **Invalid updates**: Automatic rollback to backups
- **Estimation failures**: Graceful fallback to safe defaults

## Troubleshooting

### No Updates Happening
- Check if `ea_sports_fc_25_teams.csv` exists in `assets/data/`
- Ensure the file is properly formatted CSV
- Check `assets/data/update_log.json` for error details

### Invalid ELO Scores
- Game automatically fixes invalid ELO values
- Check team ratings in-game to verify fallbacks working
- All teams will have ELO between 1000-2000

### Game Not Starting
- The game works without update files
- Remove any corrupt CSV files from `assets/data/`
- Check `assets/data/backups/` for previous working versions

### Manual Reset
To reset the update system:
1. Delete `assets/data/update_log.json`
2. Remove any CSV files from `assets/data/`
3. Restart the game

## Privacy and Terms

- **Kaggle**: Free account required, follows Kaggle terms of service
- **Data Usage**: All data is processed locally on your machine
- **No Internet Required**: Once downloaded, updates work offline
- **Backup Policy**: Last 5 data backups are automatically kept

## Support

For issues with data updates:
1. Check this documentation
2. Verify file placement and formatting
3. Check the `assets/data/update_log.json` file for error messages
4. The game will fall back to existing data if updates fail

---
*Last updated: January 2025*