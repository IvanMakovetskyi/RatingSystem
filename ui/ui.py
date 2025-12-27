import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sim.simulation import Simulation
from ratingSystem.ratings import constants  # import your constants module
import itertools

st.title("🎯 Rating System Simulator")

# ---------------------------
# Simulation Controls
# ---------------------------
games = st.slider("Games", 100, 5000, 1000)
players = st.slider("Players", 10, 1000, 100)

st.sidebar.subheader("⚙️ Simulation Constants")

# WIN_CHANGE
win_change = st.sidebar.number_input("WIN_CHANGE", min_value=1, max_value=100, value=constants.WIN_CHANGE)
constants.WIN_CHANGE = win_change

# MAX_DOPES
max_dopes = st.sidebar.number_input("MAX_DOPES", min_value=1, max_value=500, value=constants.MAX_DOPES)
constants.MAX_DOPES = max_dopes

# DOPES_SHIFT
dopes_shift = st.sidebar.number_input("DOPES_SHIFT", min_value=1, max_value=50, value=constants.DOPES_SHIFT)
constants.DOPES_SHIFT = dopes_shift

# DOPES_MEAN
dop_mean = {
    "Very Bad": -dopes_shift,
    "Bad": -dopes_shift / 2,
    "Normal": 0,
    "Good": dopes_shift,
    "Very Good": dopes_shift * 2
}
constants.DOPES_MEAN = dop_mean

# DOPES_SIGMA
dopes_sigma = st.sidebar.number_input("DOPES_SIGMA", min_value=1, max_value=50, value=constants.DOPES_SIGMA)
constants.DOPES_SIGMA = dopes_sigma


if st.button("▶ Run Simulation"):
    sim = Simulation(0, games, players)
    sim.run()

    stats = sim.getStats()

    # ---------------------------
    # Metrics
    # ---------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Games", games)
    col2.metric("Red Wins", stats["redWins"])
    col3.metric("Red Win Rate", f"{stats.get('redWinRate', stats['redWins']/games):.2%}")

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Rating", f"{stats['avgRating']:.2f}")
    col2.metric("Std Dev", f"{stats['stdDev']:.2f}")
    col3.metric("Avg Games/Player", f"{sum(p.games for p in stats['players']) / len(stats['players']):.2f}")

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
