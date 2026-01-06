import pandas as pd
import numpy as np

df = pd.read_csv("../data/PlayerStatistics.csv")
# print(df.shape)
# print(df.head())
# print(df.columns)

columns_to_drop = [
    'personId', 'gameType', 'gameLabel', 'gameSubLabel', 
    'seriesGameNumber', 'home', 'numMinutes', 'fieldGoalsAttempted', 
    'fieldGoalsMade', 'fieldGoalsPercentage', 'threePointersAttempted', 
    'threePointersMade', 'threePointersPercentage', 'freeThrowsAttempted', 
    'freeThrowsMade', 'freeThrowsPercentage', 'reboundsDefensive', 
    'reboundsOffensive', 'foulsPersonal', 'plusMinusPoints'
]

df = df.drop(columns=columns_to_drop)
# print(df.columns)

# Convert the date column to datetime format for easy comparison
df['gameDateTimeEst'] = pd.to_datetime(df['gameDateTimeEst'])
# df['gameDateTimeEst'] = df['gameDateTimeEst'].dt.date
cutoff_date = pd.to_datetime('2024-10-22')
df = df[df['gameDateTimeEst'] > cutoff_date]
# print(df.shape)

# Combine 'firstName' and 'lastName' into a new 'name' column
df['name'] = df['firstName'] + ' ' + df['lastName']
df = df.drop(columns=['firstName', 'lastName'])
# print(df.columns)

# Generate the gameSummary column
df['gameDateTimeEst'] = df['gameDateTimeEst'].dt.date
df['gameSummary'] = (
    'On ' + df['gameDateTimeEst'].astype(str) + ', ' + 
    df['name'] + ' delivered an impressive performance, registering ' + 
    df['points'].astype(str) + ' points, ' + 
    df['reboundsTotal'].astype(str) + ' rebounds, and ' + 
    df['assists'].astype(str) + ' assists, along with ' + 
    df['steals'].astype(str) + ' steals, ' + 
    df['blocks'].astype(str) + ' blocks, and ' + 
    df['turnovers'].astype(str) + ' turnovers, in a game against ' + 
    df['opponentteamName'] + ', ' + 
    np.where(df['win'] == 1, 'winning', 'losing') + ' the game.'
)
print(df.loc[0, 'gameSummary']) 


# Combine city name and team name into a new matchup column
team_abbreviations = {
    "Los Angeles": "LAL",
    "Dallas": "DAL",
    "Memphis": "MEM",
    "Miami": "MIA",
    "Boston": "BOS",
    "Golden State": "GSW",
    "Brooklyn": "BKN",
    "Chicago": "CHI",
    "Cleveland": "CLE",
    "Denver": "DEN",
    "Detroit": "DET",
    "Indiana": "IND",
    "LA Clippers": "LAC",
    "Minnesota": "MIN",
    "New Orleans": "NOP",
    "New York": "NYK",
    "Oklahoma City": "OKC",
    "Orlando": "ORL",
    "Philadelphia": "PHI",
    "Phoenix": "PHX",
    "Portland": "POR",
    "Sacramento": "SAC",
    "San Antonio": "SAS",
    "Toronto": "TOR",
    "Utah": "UTA",
    "Washington": "WAS"
}
df['matchup'] = df['playerteamCity'].map(team_abbreviations) + " vs. " + df['opponentteamCity'].map(team_abbreviations)
df = df.drop(columns=['playerteamCity', 'playerteamName', 'opponentteamCity', 'opponentteamName','reboundsTotal', 'win', 'assists', 'steals', 'blocks', 'turnovers', 'points'])
print(df.columns)

# Export the cleaned DataFrame to a new CSV file
df.to_csv("../data/cleaned_player_statistics.csv", index=False)
