import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sim.simulation import Simulation
from ratingSystem.ratings import constants  # import your constants module

st.title("🎯 Rating System Simulator")

# ---------------------------
# Simulation Controls
# ---------------------------
games = st.slider("Games", 1, 1000, 100)
players = st.slider("Players", 10, 1000, 500)

st.sidebar.subheader("⚙️ Simulation Constants")

# WIN_CHANGE
win_change = st.sidebar.number_input("WIN_CHANGE", min_value=1, max_value=100, value=constants.WIN_CHANGE)
constants.WIN_CHANGE = win_change

# MAX_DOPES_COEFFICIENT
max_dopes_coefficient = st.sidebar.number_input("MAX_DOPES_COEFFICIENT", min_value=0.0, max_value=5.0, value=constants.MAX_DOPES_COEFFICIENT)
constants.MAX_DOPES_COEFFICIENT = max_dopes_coefficient


st.sidebar.subheader("🎭 Character Parameters")

for char, params in constants.CHARACTER_PARAMS.items():
    st.sidebar.markdown(f"**{char}**")

    # Red WinRate slider (0.0 → 1.0)
    constants.CHARACTER_PARAMS[char]["redWinRate"] = st.sidebar.slider(
        f"{char} Red WinRate",
        min_value=0.0,
        max_value=1.0,
        value=params["redWinRate"],
        step=0.01
    )

    # Black WinRate slider (0.0 → 1.0)
    constants.CHARACTER_PARAMS[char]["blackWinRate"] = st.sidebar.slider(
        f"{char} Black WinRate",
        min_value=0.0,
        max_value=1.0,
        value=params["blackWinRate"],
        step=0.01
    )

    # Avg Dope slider (-50 → 50)
    constants.CHARACTER_PARAMS[char]["avgDope"] = st.sidebar.slider(
        f"{char} Avg Dope",
        min_value=-5.0,
        max_value=5.0,
        value=params["avgDope"],
        step=0.01
    )

# DOPES_SHIFT
dopes_shift = st.sidebar.number_input("DOPES_SHIFT", min_value=1, max_value=50, value=constants.DOPES_SHIFT)
constants.DOPES_SHIFT = dopes_shift

# DOPES_MEAN
dopes_mean = {
    "Very Bad": -dopes_shift,
    "Bad": -dopes_shift / 2,
    "Normal": 0,
    "Good": dopes_shift,
    "Very Good": dopes_shift * 2
}
constants.DOPES_MEAN = dopes_mean

# DOPES_SIGMA
dopes_sigma = st.sidebar.number_input("DOPES_SIGMA", min_value=1, max_value=50, value=constants.DOPES_SIGMA)
constants.DOPES_SIGMA = dopes_sigma

# GAMES_COEFFICIENT_A
games_coefficient_a = st.sidebar.number_input("GAMES_COEFFICIENT_A", min_value=1, max_value=50, value=constants.GAMES_COEFFICIENT_A)
constants.GAMES_COEFFICIENT_A = games_coefficient_a

# GAMES_COEFFICIENT_B
games_coefficient_b = st.sidebar.number_input("GAMES_COEFFICIENT_B", min_value=1, max_value=100, value=constants.GAMES_COEFFICIENT_B)
constants.GAMES_COEFFICIENT_B = games_coefficient_b

# RATING_COEFFICIENT_A
rating_coefficient_a = st.sidebar.number_input("RATING_COEFFICIENT_A", min_value=1, max_value=100, value=constants.RATING_COEFFICIENT_A)
constants.RATING_COEFFICIENT_A = rating_coefficient_a

# RATING_COEFFICIENT_B
rating_coefficient_b = st.sidebar.number_input("RATING_COEFFICIENT_B", min_value=1, max_value=1000, value=constants.RATING_COEFFICIENT_B)
constants.RATING_COEFFICIENT_B = rating_coefficient_b


if st.button("▶ Run Simulation"):
    sim = Simulation(0, games, players)
    sim.run()

    stats = sim.getStats()

    # ---------------------------
    # Metrics
    # ---------------------------

    col1, col2 = st.columns(2)
    col1.metric("Avg Rating", f"{stats['avgRating']:.2f}")
    col2.metric("Std Dev", f"{stats['stdDev']:.2f}")

    col1, col2 = st.columns(2)
    col1.metric("Min Rating", f"{stats['minRating']:.2f}")
    col2.metric("Max Rating", f"{stats['maxRating']:.2f}")

    st.divider()

    # ---------------------------
    # Overall Rating Histogram
    # ---------------------------
    st.subheader("📊 Overall Rating Distribution")
    fig, ax = plt.subplots()
    ax.hist(stats["ratings"], bins=20, color="skyblue", edgecolor="black")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Players")
    st.pyplot(fig)

    # ---------------------------
    # Character-wise Histograms (specific colors)
    # ---------------------------
    st.subheader("🎭 Rating Distribution by Character")
    if stats["charHistograms"]:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Determine global min and max for same scale
        all_ratings = stats["ratings"]
        x_min = min(all_ratings)
        x_max = max(all_ratings)

        # Define specific colors for characters
        char_colors = {
            "Very Bad": "red",
            "Bad": "lightcoral",       # light red
            "Normal": "yellow",
            "Good": "lightgreen",
            "Very Good": "green",
        }

        for char, ratings in stats["charHistograms"].items():
            color = char_colors.get(char, "gray")  # fallback color
            ax.hist(ratings, bins=20, alpha=0.6, label=char, color=color, range=(x_min, x_max))

        ax.set_xlabel("Rating")
        ax.set_ylabel("Players")
        ax.set_title("Character-wise Rating Distribution")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("No character information available. Showing overall histogram only.")


    # ---------------------------
    # Player Table
    # ---------------------------
    st.subheader("📋 Player Ratings Table")
    df = pd.DataFrame({
        "Player ID": [p.id for p in stats["players"]],
        "Character": [getattr(p, "character", "Unknown") for p in stats["players"]],
        "Rating": stats["ratings"],
        "Games Played": [p.games for p in stats["players"]],
    })
    st.dataframe(df, use_container_width=True)
