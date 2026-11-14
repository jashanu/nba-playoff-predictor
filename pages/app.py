import streamlit as st
import sys
import os
from PIL import Image

sys.path.append(os.path.dirname(__file__))

from playoff_simulator import run_simulation


# ----------------------------
# CONFIG
# ----------------------------

st.set_page_config(
    page_title="NBA Playoff Predictor",
    page_icon="🏀",
    layout="wide"
)


# ----------------------------
# LOGO PATH
# ----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "logos")


# ----------------------------
# NORMALIZE LOGOS
# ----------------------------

@st.cache_data
def load_logo(team):

    path = os.path.join(
        LOGO_DIR,
        f"{team}.png"
    )

    if not os.path.exists(path):
        return None


    img = Image.open(path).convert("RGBA")


    # remove transparent borders

    bbox = img.getbbox()

    if bbox:
        img = img.crop(bbox)



    # resize while keeping aspect ratio

    img.thumbnail(
        (120,120)
    )


    # create same size canvas

    canvas = Image.new(
        "RGBA",
        (120,120),
        (0,0,0,0)
    )


    x = (120 - img.width)//2
    y = (120 - img.height)//2


    canvas.paste(
        img,
        (x,y),
        img
    )


    return canvas



# ----------------------------
# SPACING
# ----------------------------

def space(amount):

    for _ in range(amount):
        st.write("")



# ----------------------------
# MATCHUP CARD
# ----------------------------

def game_card(game):

    winner = game["winner"]
    loser = game["loser"]



    with st.container():


        # winner row

        c1, c2 = st.columns(
            [1,5]
        )


        with c1:

            img = load_logo(winner)

            if img:
                st.image(
                    img,
                    width=45
                )


        with c2:

            st.markdown(
                f"**{winner}**"
            )



        st.markdown(
            f"**{game['score']}**"
        )



        # loser row

        c1, c2 = st.columns(
            [1,5]
        )


        with c1:

            img = load_logo(loser)

            if img:
                st.image(
                    img,
                    width=45
                )


        with c2:

            st.write(loser)



        st.caption(
            f"Series Probability: "
            f"{game['winner_series_prob']:.0%}"
        )


        st.divider()



# ----------------------------
# TITLE
# ----------------------------

st.title(
    "🏀 NBA Playoff Predictor"
)



# ----------------------------
# RUN SIMULATION
# ----------------------------

if st.button(
    "🚀 Run Simulation"
):

    with st.spinner(
        "Simulating playoffs..."
    ):

        st.session_state.results = run_simulation()



# ----------------------------
# BRACKET
# ----------------------------

if "results" in st.session_state:


    r = st.session_state.results


    st.subheader(
        "2025-26 NBA Playoff Bracket"
    )



    (
        east_r1,
        east_r2,
        east_cf,
        finals,
        west_cf,
        west_r2,
        west_r1

    ) = st.columns(
        [
            1.7,
            1.7,
            1.7,
            2.2,
            1.7,
            1.7,
            1.7
        ]
    )



    # EAST ROUND 1

    with east_r1:

        st.markdown(
            "### East R1"
        )

        for game in r["round1_east"]:

            game_card(game)



    # EAST ROUND 2

    with east_r2:

        st.markdown(
            "### East R2"
        )

        space(6)

        game_card(
            r["round2_east"][0]
        )

        space(8)

        game_card(
            r["round2_east"][1]
        )



    # EAST FINALS

    with east_cf:

        st.markdown(
            "### ECF"
        )

        space(16)

        game_card(
            r["east_final"]
        )



    # FINALS

    with finals:

        st.markdown(
            "## 🏆 NBA FINALS"
        )

        space(22)

        game_card(
            r["nba_final"]
        )


        st.success(
            f"🏆 Champion: {r['champion']}"
        )



    # WEST FINALS

    with west_cf:

        st.markdown(
            "### WCF"
        )

        space(16)

        game_card(
            r["west_final"]
        )



    # WEST ROUND 2

    with west_r2:

        st.markdown(
            "### West R2"
        )

        space(6)

        game_card(
            r["round2_west"][0]
        )

        space(8)

        game_card(
            r["round2_west"][1]
        )



    # WEST ROUND 1

    with west_r1:

        st.markdown(
            "### West R1"
        )

        for game in r["round1_west"]:

            game_card(game)