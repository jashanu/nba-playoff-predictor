from nba_api.stats.endpoints import leaguegamelog, leaguedashteamstats
import pandas as pd
import time

seasons = [
    '2015-16',
    '2016-17',
    '2017-18',
    '2018-19',
    '2019-20',
    '2020-21',
    '2021-22',
    '2022-23',
    '2023-24',
    '2024-25'
]

all_rows = []

for season in seasons:

    print(f"Processing {season}")

    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season
    ).get_data_frames()[0]

    playoffs = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star='Playoffs'
    ).get_data_frames()[0]

    games = playoffs['GAME_ID'].unique()

    for game_id in games:

        game = playoffs[playoffs['GAME_ID'] == game_id]

        if len(game) != 2:
            continue

        team_a = game.iloc[0]
        team_b = game.iloc[1]

        a_stats = team_stats[
            team_stats['TEAM_ID'] == team_a['TEAM_ID']
        ]

        b_stats = team_stats[
            team_stats['TEAM_ID'] == team_b['TEAM_ID']
        ]

        if len(a_stats) == 0 or len(b_stats) == 0:
            continue

        a = a_stats.iloc[0]
        b = b_stats.iloc[0]

        row = {
            'W_PCT_DIFF': a['W_PCT'] - b['W_PCT'],
            'PTS_DIFF': a['PTS'] - b['PTS'],
            'REB_DIFF': a['REB'] - b['REB'],
            'AST_DIFF': a['AST'] - b['AST'],
            'FG_PCT_DIFF': a['FG_PCT'] - b['FG_PCT'],
            'FG3_PCT_DIFF': a['FG3_PCT'] - b['FG3_PCT'],
            'FT_PCT_DIFF': a['FT_PCT'] - b['FT_PCT'],
            'STL_DIFF': a['STL'] - b['STL'],
            'BLK_DIFF': a['BLK'] - b['BLK'],
            'PLUS_MINUS_DIFF': a['PLUS_MINUS'] - b['PLUS_MINUS'],
            'TARGET': 1 if team_a['WL'] == 'W' else 0
        }

        all_rows.append(row)

    time.sleep(1)

df = pd.DataFrame(all_rows)

df.to_csv("playoff_dataset.csv", index=False)

print("\nDONE")
print(df.head())
print("\nShape:", df.shape)