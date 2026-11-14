from nba_api.stats.endpoints import leaguedashteamstats

stats = leaguedashteamstats.LeagueDashTeamStats(
    season="2025-26",
    season_type_all_star="Regular Season"
)

df = stats.get_data_frames()[0]

columns = [
    "TEAM_NAME",
    "W_PCT",
    "PTS",
    "REB",
    "AST",
    "FG_PCT",
    "FG3_PCT",
    "FT_PCT",
    "STL",
    "BLK",
    "PLUS_MINUS"
]

df = df[columns]

print(df)

df.to_csv("current_teams.csv", index=False)