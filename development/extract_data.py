import pandas as pd
import os
from tqdm import tqdm  # For displaying progress bars

version = 24.0  # Specify FIFA version for filtering
base_path = '../assets'  # Base path for reading files

# Read teams and players CSV files
team_csv = pd.read_csv(os.path.join(base_path, 'raw/male_teams.csv'))
players_csv = pd.read_csv(os.path.join(base_path, 'raw/male_players.csv'))

# Filter dataframes by fifa_version
team_csv = team_csv[team_csv['fifa_version'] == version]
players_csv = players_csv[players_csv['fifa_version'] == version]

# Exclude 'Friendly International' from teams data
teams_csv_filtered_df = team_csv[team_csv['league_name'] != 'Friendly International']
# Get unique combinations of league_name and nationality_name
teams_csv_unique_combinations = teams_csv_filtered_df[['league_name', 'nationality_name']].drop_duplicates()

base_path = '../assets/data'  # Update base path for saving data

# Iterate through unique combinations with progress bar
for _, row in tqdm(teams_csv_unique_combinations.iterrows(), total=teams_csv_unique_combinations.shape[0]):
    league, nationality = row['league_name'], row['nationality_name']
    # Filter teams by league and nationality
    league_teams = team_csv[(team_csv['league_name'] == league) & (team_csv['nationality_name'] == nationality)]

    # Process only if there are more than 10 teams in the league
    if len(league_teams) > 10:
        # Replace spaces with underscores for file naming
        folder_name = nationality.replace(' ', '_')
        subfolder_name = league.replace(' ', '_')
        # Create directory path
        full_path = os.path.join(base_path, folder_name, subfolder_name)
        os.makedirs(full_path, exist_ok=True)  # Ensure directory exists
        # Save league_teams dataframe to CSV
        league_teams.to_csv(os.path.join(full_path, 'all_teams.csv'), sep=',', header=True, index=False)
        
        # Save individual team data
        for team_name in league_teams['team_name']:
            team = players_csv[players_csv['club_name'] == team_name]
            # Save each team's player data to a CSV file
            team.to_csv(os.path.join(full_path, team_name.replace(' ', '_').replace('/', '') + '.csv'), sep=',', header=True, index=False)
