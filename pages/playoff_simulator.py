import pandas as pd
import joblib
import random
from math import comb


# ----------------------------
# LOAD MODEL + DATA
# ----------------------------

model = joblib.load("playoff_model.pkl")
teams = pd.read_csv("current_teams.csv")


# ----------------------------
# TEAM LOOKUP
# ----------------------------

def get_team(name):

    row = teams[teams["TEAM_NAME"].str.strip() == name.strip()]

    if row.empty:
        raise ValueError(f"Team not found: {name}")

    return row.iloc[0]



# ----------------------------
# GAME PROBABILITY
# ----------------------------

def get_win_prob(team_a, team_b):

    X = pd.DataFrame([{

        "W_PCT_DIFF": team_a["W_PCT"] - team_b["W_PCT"],
        "PTS_DIFF": team_a["PTS"] - team_b["PTS"],
        "REB_DIFF": team_a["REB"] - team_b["REB"],
        "AST_DIFF": team_a["AST"] - team_b["AST"],
        "FG_PCT_DIFF": team_a["FG_PCT"] - team_b["FG_PCT"],
        "FG3_PCT_DIFF": team_a["FG3_PCT"] - team_b["FG3_PCT"],
        "FT_PCT_DIFF": team_a["FT_PCT"] - team_b["FT_PCT"],
        "STL_DIFF": team_a["STL"] - team_b["STL"],
        "BLK_DIFF": team_a["BLK"] - team_b["BLK"],
        "PLUS_MINUS_DIFF": team_a["PLUS_MINUS"] - team_b["PLUS_MINUS"]

    }])

    return model.predict_proba(X)[0][1]



# ----------------------------
# SERIES PROBABILITY
# ----------------------------

def calculate_series_probability(p):

    probability = 0

    for losses in range(4):

        games = 3 + losses

        probability += (
            comb(games, 3)
            * (p ** 4)
            * ((1 - p) ** losses)
        )

    return probability



# ----------------------------
# SIMULATE BEST OF 7
# ----------------------------

def simulate_series(team_a_name, team_b_name):

    team_a = get_team(team_a_name)
    team_b = get_team(team_b_name)

    base_prob = get_win_prob(team_a, team_b)

    a_wins = 0
    b_wins = 0

    game_number = 1


    while a_wins < 4 and b_wins < 4:


        if game_number in [1,2,5,7]:
            game_prob = min(base_prob + 0.05, 0.95)

        else:
            game_prob = max(base_prob - 0.05, 0.05)



        if random.random() < game_prob:
            a_wins += 1

        else:
            b_wins += 1


        game_number += 1



    adjusted_prob = min(max(base_prob + 0.02,0.05),0.95)

    series_prob_a = calculate_series_probability(adjusted_prob)
    series_prob_b = 1 - series_prob_a



    if a_wins > b_wins:

        return {

            "winner": team_a_name,
            "loser": team_b_name,
            "score": f"{a_wins}-{b_wins}",

            "winner_game_prob": adjusted_prob,
            "loser_game_prob": 1-adjusted_prob,

            "winner_series_prob": series_prob_a,
            "loser_series_prob": series_prob_b

        }


    else:

        return {

            "winner": team_b_name,
            "loser": team_a_name,
            "score": f"{b_wins}-{a_wins}",

            "winner_game_prob": 1-adjusted_prob,
            "loser_game_prob": adjusted_prob,

            "winner_series_prob": series_prob_b,
            "loser_series_prob": series_prob_a

        }



# ----------------------------
# BRACKET HELPERS
# ----------------------------

def make_round1(conference):

    return [

        (conference[0], conference[7]),
        (conference[3], conference[4]),
        (conference[2], conference[5]),
        (conference[1], conference[6])

    ]


def make_round2(winners):

    return [

        (winners[0], winners[1]),
        (winners[2], winners[3])

    ]



# ----------------------------
# TEAMS
# ----------------------------

east = [

    "Detroit Pistons",
    "Boston Celtics",
    "New York Knicks",
    "Cleveland Cavaliers",
    "Toronto Raptors",
    "Atlanta Hawks",
    "Philadelphia 76ers",
    "Orlando Magic"

]


west = [

    "Oklahoma City Thunder",
    "San Antonio Spurs",
    "Denver Nuggets",
    "Los Angeles Lakers",
    "Houston Rockets",
    "Minnesota Timberwolves",
    "Phoenix Suns",
    "Portland Trail Blazers"

]



# ----------------------------
# MAIN SIMULATION FUNCTION
# ----------------------------

def run_simulation():


    results = {}


    # ROUND 1

    results["round1_east"] = [
        simulate_series(a,b)
        for a,b in make_round1(east)
    ]


    results["round1_west"] = [
        simulate_series(a,b)
        for a,b in make_round1(west)
    ]



    # ROUND 2

    east_winners = [
        x["winner"] for x in results["round1_east"]
    ]

    west_winners = [
        x["winner"] for x in results["round1_west"]
    ]



    results["round2_east"] = [
        simulate_series(a,b)
        for a,b in make_round2(east_winners)
    ]


    results["round2_west"] = [
        simulate_series(a,b)
        for a,b in make_round2(west_winners)
    ]



    # CONFERENCE FINALS

    results["east_final"] = simulate_series(
        results["round2_east"][0]["winner"],
        results["round2_east"][1]["winner"]
    )


    results["west_final"] = simulate_series(
        results["round2_west"][0]["winner"],
        results["round2_west"][1]["winner"]
    )



    # NBA FINALS

    results["nba_final"] = simulate_series(
        results["east_final"]["winner"],
        results["west_final"]["winner"]
    )


    results["champion"] = results["nba_final"]["winner"]


    return results




# ----------------------------
# TERMINAL MODE
# ----------------------------

if __name__ == "__main__":


    results = run_simulation()


    print("\n===== 2025-26 NBA PLAYOFF SIMULATION =====")


    for rnd in [
        "round1_east",
        "round1_west",
        "round2_east",
        "round2_west",
        "east_final",
        "west_final",
        "nba_final"
    ]:

        print(f"\n===== {rnd.upper()} =====\n")


        games = results[rnd]


        if isinstance(games, list):

            for game in games:

                print(
                    f"{game['winner']} def. "
                    f"{game['loser']} "
                    f"{game['score']}"
                )


        else:

            print(
                f"{games['winner']} def. "
                f"{games['loser']} "
                f"{games['score']}"
            )



    print(
        f"\n🏆 NBA CHAMPION: {results['champion']}"
    )