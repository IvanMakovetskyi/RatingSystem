import streamlit as st
import numpy as np
import pandas as pd

st.title("Rating System Simulator")

# ----------------------
# Simulation Settings
# ----------------------
st.sidebar.header("Constants")

WIN_CHANGE = st.sidebar.number_input("WIN_CHANGE", value=5.0)
MAX_DOPES = st.sidebar.number_input("MAX_DOPES", value=20.0)
DOPES_SIGMA = st.sidebar.number_input("DOPES_SIGMA", value=5.0)

st.sidebar.header("DOPES_MEAN")
mean_very_bad = st.sidebar.number_input("Very Bad", value=-10.0)
mean_bad = st.sidebar.number_input("Bad", value=-5.0)
mean_normal = st.sidebar.number_input("Normal", value=0.0)
mean_good = st.sidebar.number_input("Good", value=5.0)
mean_very_good = st.sidebar.number_input("Very Good", value=10.0)

st.sidebar.header("Simulation")
num_players = st.sidebar.slider("Players", 10, 1000, 100)
num_games = st.sidebar.slider("Games", 1, 5000, 1000)

# ----------------------
# Run Simulation
# ----------------------
class run_simulation:
    def __init__(self):
        print("Simulation created")

if st.button("Run Simulation"):
    print("Button pressed")
    """
    players = run_simulation()

    df = pd.DataFrame(players)

    # ----------------------
    # Statistics
    # ----------------------
    st.subheader("Rating Statistics")
    st.write(df["rating"].describe())

    st.subheader("Rating Distribution")
    st.bar_chart(df["rating"])

    st.subheader("Player Table")
    st.dataframe(df)
    """
