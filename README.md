# Mafia Rating System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**Mafia Rating System** is a Python-based simulation framework for Mafia-style games, featuring dynamic player ratings, team matchmaking, and statistical analysis.

---

## Features

- **Dynamic Player Ratings:** Ratings adjust after each game with fast early progression and diminishing returns at higher levels.
- **Simulation Engine:** Run single or bulk games to analyze win probabilities, rating progression, and team balance.
- **Matchmaking Logic:** Supports balanced teams with rating-based and random assignment algorithms.
- **Data Analytics:** Track rating distributions, win/loss statistics, and rating convergence.
- **CLI Interface:** Run and inspect simulations easily from the command line.
- **Extensible Design:** Easily add new roles, rating models, or simulation scenarios.

---

## Folder Structure

rating_system/ # Core logic (Player, Game, Rating, Simulation)
sim/ # Simulation scripts (single, bulk, Monte Carlo)
ui/ # User interface (CLI / optional GUI)
data/ # Configs, logs, sample datasets
tests/ # Unit tests

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/mafia-rating-system.git
cd mafia-rating-system
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run a simulation

bash
Copy code
python sim/single_game.py
