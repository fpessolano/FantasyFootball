
# SCRATCH FILE: Player position analysis experiment  
# Analyzes player position modifiers from CSV data - normalizes position ratings
# Used for development/testing of player attribute system (v0.5.x redesign)
# Not used in main application - experimental position rating calculations

import pandas as pd


drop_list = ['player_id', 'player_url', 'fifa_version', 'fifa_update', 'update_as_of',
             'club_team_id', 'club_name', 'league_id', 'league_name', 'league_level', 'real_face']

general_informartion = ['short_name', 'long_name',
                        'age', 'dob',  'nation_team_id', 'nationality_name', ]
general_physical = ['height_cm', 'weight_kg', 'body_type',]

contract = ['value_eur', 'wage_eur', 'club_loaned_from',
            'club_joined_date', 'club_contract_valid_until_year',]

positon = ['player_positions', 'club_position', 'club_jersey_number',
           'nation_position', 'nation_jersey_number', 'international_reputation',]

position_modifiers = ['ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram', 'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb',
                      'lb', 'lcb', 'cb', 'rcb', 'rb', 'gk']

goalkeeping = ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 'goalkeeping_positioning', 'goalkeeping_reflexes',
               'goalkeeping_speed',]

column_names = ['overall', 'potential',
                'preferred_foot', 'weak_foot', 'skill_moves',  'work_rate',
                'release_clause_eur', 'player_tags', 'player_traits', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'attacking_crossing', 'attacking_finishing',
                'attacking_heading_accuracy', 'attacking_short_passing', 'attacking_volleys', 'skill_dribbling', 'skill_curve', 'skill_fk_accuracy',
                'skill_long_passing', 'skill_ball_control', 'movement_acceleration', 'movement_sprint_speed', 'movement_agility', 'movement_reactions',
                'movement_balance', 'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots', 'mentality_aggression', 'mentality_interceptions',
                'mentality_positioning', 'mentality_vision', 'mentality_penalties', 'mentality_composure', 'defending_marking_awareness', 'defending_standing_tackle',
                'defending_sliding_tackle',]

csv_file_path = '../assets/data/Belgium/Jupiler_Pro_League/Anderlecht.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)
df = df.drop(drop_list, axis=1)

# List all column names in the DataFrame
column_names = df.columns.tolist()

# Print the list of column names
# print("Column names in the CSV file:")
# for name in column_names:
#     # print(name)
#     print(f"{name}, ", end='')
# print()

# row = df.iloc[3]
# for column, value in row.items():
#     print(f"{column}: {value}")

# for value in df['long_name']:
#     print(value)


# Iterate over rows and print values of specified columns
print(position_modifiers)
for index, row in df.iterrows():
    values = [eval(row[column]) for column in position_modifiers]
    max_value = max(values)
    normalized_array = [int(x*100 / max_value)/100 for x in values]
    print(normalized_array)
