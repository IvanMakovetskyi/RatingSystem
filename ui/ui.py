import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sim.simulation import Simulation
from ratingSystem.ratings import constants
from collections import Counter, defaultdict

st.title("🎯 Rating System Simulator")

# ---------------------------
# Simulation Controls
# ---------------------------
games = st.slider("Games", 1, 5000, 1000)
num_players = st.slider("Players", 10, 1000, 500)

st.divider()

st.sidebar.subheader("⚙️ Simulation Constants")

constants.WIN_CHANGE = st.sidebar.number_input(
    "WIN_CHANGE", min_value=1, max_value=100, value=constants.WIN_CHANGE
)

constants.DOPES_COEFFICIENT = st.sidebar.number_input(
    "DOPES_COEFFICIENT", min_value=0.0, max_value=5.0, value=constants.DOPES_COEFFICIENT
)

st.sidebar.subheader("🎭 Character Parameters")

for char, params in constants.CHARACTER_PARAMS.items():
    st.sidebar.markdown(f"**{char}**")

    params["redWinRate"] = st.sidebar.slider(
        f"{char} Red WinRate", 0.0, 1.0, params["redWinRate"], 0.01
    )

    params["blackWinRate"] = st.sidebar.slider(
        f"{char} Black WinRate", 0.0, 1.0, params["blackWinRate"], 0.01
    )

    params["avgDope"] = st.sidebar.slider(
        f"{char} Avg Dope", -1.0, 1.0, params["avgDope"], 0.01
    )

constants.DOPES_SIGMA = st.sidebar.number_input(
    "WINRATE_SIGMA", 0.0, 1.0, constants.WINRATE_SIGMA
)

constants.GAMES_COEFFICIENT_A = st.sidebar.number_input(
    "GAMES_COEFFICIENT_A", 1, 50, constants.GAMES_COEFFICIENT_A
)

constants.GAMES_COEFFICIENT_B = st.sidebar.number_input(
    "GAMES_COEFFICIENT_B", 1, 100, constants.GAMES_COEFFICIENT_B
)

constants.RATING_COEFFICIENT_A = st.sidebar.number_input(
    "RATING_COEFFICIENT_A", 1, 100, constants.RATING_COEFFICIENT_A
)

constants.RATING_COEFFICIENT_B = st.sidebar.number_input(
    "RATING_COEFFICIENT_B", 1, 1000, constants.RATING_COEFFICIENT_B
)

constants.RATING_COEFFICIENT_C = st.sidebar.number_input(
    "RATING_COEFFICIENT_C", 0.0, 2.0, constants.RATING_COEFFICIENT_C
)

# ---------------------------
# Select Stats to Calculate
# ---------------------------
st.subheader("📊 Select Statistics to Display")

stats_options = {
    "Summary Metrics": False,
    "Rating Change Stats": False,
    "Overall Rating Histogram": False,
    "Character-wise Rating Distribution": False,
    "Rank Composition": False,
    "Top 10 Players": False
}

selected_stats = {}
for stat_name, default in stats_options.items():
    selected_stats[stat_name] = st.checkbox(stat_name, value=default)

# ============================================================
# RUN
# ============================================================
if st.button("▶ Run Simulation"):
    sim = Simulation(0, games, num_players)
    sim.run()

    stats = sim.getStats()
    players = stats["players"]

    # ---------------------------
    # Summary Metrics
    # ---------------------------
    if selected_stats["Summary Metrics"]:

        ratings = stats["ratings"]
        zero_count = sum(1 for r in ratings if r == 0)
        zero_perc = (zero_count / len(ratings)) * 100 if ratings else 0

        c1, c2 = st.columns(2)
        c1.metric("Avg Rating", f"{stats['avgRating']:.2f}")
        c2.metric("Std Dev", f"{stats['stdDev']:.2f}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Min Rating", f"{stats['minRating']:.2f}")
        c2.metric("0 Rating", f"{zero_count} / {zero_perc:.2f}%")
        c3.metric("Max Rating", f"{stats['maxRating']:.2f}")

        st.divider()

    # ============================================================
    # 📈 Rating Change Statistics
    # ============================================================
    if selected_stats["Rating Change Stats"]:
        st.subheader("📈 Average Rating Change Statistics")

        rank_changes = defaultdict(list)
        rank_dopes = defaultdict(list)
        rank_win_coefs = defaultdict(list)
        rank_loss_coefs = defaultdict(list)

        char_changes = defaultdict(list)
        char_dopes = defaultdict(list)
        char_win_coefs = defaultdict(list)
        char_loss_coefs = defaultdict(list)


        id_to_char = {p.getId(): p.character for p in players}

        for entry in sim.ratingChange:
            for pid, (rank, change, dope, coef) in entry.items():
                pid = int(pid)
                if pid not in id_to_char:
                    continue

                # Rank-based
                rank_changes[rank].append(change)
                rank_dopes[rank].append(dope)

                if change > 0:
                    rank_win_coefs[rank].append(coef)
                elif change < 0:
                    rank_loss_coefs[rank].append(coef)

                # Character-based
                char = id_to_char[pid]
                char_changes[char].append(change)
                char_dopes[char].append(dope)

                if change > 0:
                    char_win_coefs[char].append(coef)
                elif change < 0:
                    char_loss_coefs[char].append(coef)


        def avg(lst):
            return sum(lst) / len(lst) if lst else 0

        def avg_inc(lst):
            return avg([x for x in lst if x > 0])

        def avg_dec(lst):
            return avg([x for x in lst if x < 0])

        st.markdown("### 🏅 By Rank")
        rank_rows = []
        for rank in constants.RANKS:
            ch = rank_changes.get(rank, [])
            if not ch:
                continue
            rank_rows.append({
            "Rank": rank,
            "Avg Increase": avg_inc(ch),
            "Avg Decrease": avg_dec(ch),
            "Avg Change": avg(ch),
            "Avg Dope": avg(rank_dopes[rank]),
            "Avg Win Coef": avg(rank_win_coefs[rank]),
            "Avg Loss Coef": avg(rank_loss_coefs[rank]),
        })

        st.dataframe(pd.DataFrame(rank_rows), use_container_width=True)

        st.markdown("### 🎭 By Character")
        char_rows = []
        for char, ch in char_changes.items():
            char_rows.append({
            "Character": char,
            "Avg Increase": avg_inc(ch),
            "Avg Decrease": avg_dec(ch),
            "Avg Change": avg(ch),
            "Avg Dope": avg(char_dopes[char]),
            "Avg Win Coef": avg(char_win_coefs[char]),
            "Avg Loss Coef": avg(char_loss_coefs[char]),
        })

        st.dataframe(pd.DataFrame(char_rows), use_container_width=True)

    # ============================================================
    # 📊 Rating Distributions
    # ============================================================
    if selected_stats["Overall Rating Histogram"]:
        st.subheader("📊 Overall Rating Distribution")
        fig, ax = plt.subplots()
        ax.hist(stats["ratings"], bins=20)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Players")
        st.pyplot(fig)

        st.subheader("🎭 Rating Distribution by Character")

        char_colors = {
            "Very Bad": "red",
            "Bad": "lightcoral",
            "Normal": "yellow",
            "Good": "lightgreen",
            "Very Good": "green",
        }

        fig, ax = plt.subplots(figsize=(10, 6))
        for char, ratings in stats["charHistograms"].items():
            ax.hist(
                ratings,
                bins=20,
                alpha=0.6,
                label=char,
                color=char_colors.get(char, "gray"),
                range=(min(stats["ratings"]), max(stats["ratings"]))
            )

        ax.legend()
        ax.set_xlabel("Rating")
        ax.set_ylabel("Players")
        st.pyplot(fig)

    # ---------------------------
    # Character-wise Rating Distribution
    # ---------------------------
    if selected_stats["Character-wise Rating Distribution"]:
        st.subheader("🎯 Character-wise Rating Distributions (Separate Histograms)")

        # Define the order
        char_order = ["Very Bad", "Bad", "Normal", "Good", "Very Good"]

        char_colors = {
            "Very Bad": "red",
            "Bad": "lightcoral",
            "Normal": "yellow",
            "Good": "lightgreen",
            "Very Good": "green",
        }

        # Compute global min and max for consistent x-axis
        all_ratings = []
        for ratings in stats["charHistograms"].values():
            all_ratings.extend(ratings)

        if not all_ratings:
            st.info("No character rating data available.")
        else:
            x_min = min(all_ratings)
            x_max = max(all_ratings)

            # Loop in the predefined order
            for char in char_order:
                ratings = stats["charHistograms"].get(char, [])
                if not ratings:  # skip if no players of this character
                    continue

                fig, ax = plt.subplots()
                ax.hist(
                    ratings,
                    bins=20,
                    color=char_colors.get(char, "gray"),
                    edgecolor="black",
                    range=(x_min, x_max)
                )
                ax.set_title(f"{char} Rating Distribution")
                ax.set_xlabel("Rating")
                ax.set_ylabel("Number of Players")
                ax.set_xlim(x_min, x_max)  # consistent x-axis
                st.pyplot(fig)

    # ============================================================
    # 📊 Rank Composition
    # ============================================================
    if selected_stats["Rank Composition"]:
        st.subheader("📊 Rank-based Statistics (Class-relative)")

        all_class_counts = Counter(p.character for p in players)
        rank_data = defaultdict(list)

        for p in players:
            rank_data[p.rank].append(p.character)

        for rank in constants.RANKS:
            chars = rank_data.get(rank, [])
            if not chars:
                continue

            st.markdown(f"**{rank}** — {len(chars)} players ({len(chars)/len(players):.2%})")
            counts = Counter(chars)

            for char, count in counts.items():
                st.write(
                    f"- {char}: {count} ({count / all_class_counts[char]:.2%} of all {char})"
                )

            st.divider()

    # ============================================================
    # 🏆 Top 10 Players
    # ============================================================
    if selected_stats["Top 10 Players"]:
        st.subheader("🏆 Top 10 Players")

        top = sorted(players, key=lambda p: p.getRating(), reverse=True)[:10]

        df = pd.DataFrame({
            "Player ID": [p.id for p in top],
            "Character": [p.character for p in top],
            "Rating": [p.getRating() for p in top],
            "Red WinRate": [p.redWinRate for p in top],
            "Black WinRate": [p.blackWinRate for p in top],
        })

        st.dataframe(df, use_container_width=True)
