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
    'Player: ' + df['name'] + '. ' +
    'Team: ' + df['playerteamName'] + '. ' +
    'Opponent: ' + df['opponentteamName'] + '. ' +
    'Date: ' + df['gameDateTimeEst'].astype(str) + '. ' +
    'Stats: ' + df['points'].astype(str) + ' PTS, ' + 
    df['reboundsTotal'].astype(str) + ' REB, ' + 
    df['assists'].astype(str) + ' AST. ' +
    'Other: ' + df['steals'].astype(str) + ' STL, ' + 
    df['blocks'].astype(str) + ' BLK. ' +
    'Outcome: ' + np.where(df['win'] == 1, 'Win', 'Loss') + '.'
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


df['searchText'] = (
    df['name'] + " | " + 
    df['gameDateTimeEst'].astype(str) + " | " + 
    df['matchup']
)
print(df.columns)

# Export the cleaned DataFrame to a new CSV file
df.to_csv("../data/cleaned_player_statistics.csv", index=False)
