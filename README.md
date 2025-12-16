# Mafia Rating System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

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
```
RatingSystem/
│
├── README.md
├── .gitignore
├── requirements.txt
├── setup.py            # Optional, if you want to make it a package
│
├── rating_system/      # Core logic
│   ├── __init__.py
│   ├── player.py
│   ├── game.py
│   ├── rating.py
│   ├── simulation.py
│   ├── matchmaking.py
│   └── utils.py
│
├── sim/                # Simulation scripts
│   ├── single_game.py
│   ├── bulk_sim.py
│   └── monte_carlo.py
│
├── ui/                 # User interface
│   ├── cli.py
│   └── gui.py          # Optional for future
│
├── data/               # Configs, logs, and sample datasets
│   ├── configs/
│   │   ├── rating_v1.json
│   │   └── matchmaking.json
│   ├── logs/
│   │   ├── sim_run_001.csv
│   │   └── errors.log
│   └── samples/
│       └── players_seed.csv
│
└── tests/              # Unit tests
    ├── test_player.py
    ├── test_game.py
    ├── test_rating.py
    ├── test_simulation.py
    └── test_matchmaking.py
```

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/mafia-rating-system.git
cd mafia-rating-system
```
2. **Install dependencies**

```bash
pip install -r requirements.txt
```
3. **Run a simulation**

```bash
python sim/single_game.py
```
