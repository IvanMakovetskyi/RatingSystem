import random
import pytest
from sim.simulation import Simulation


# =====================================================
# Player creation tests
# =====================================================

def test_create_players_count():
    """
    Simulation should create exactly `playersCount` players.
    """
    sim = Simulation(0, games=10, playersCount=20)
    players = sim.createPlayers()

    assert len(players) == 20
    assert len(sim.players) == 20


def test_players_have_unique_ids():
    """
    Each created player should have a unique ID.
    """
    sim = Simulation(0, games=1, playersCount=15)
    sim.createPlayers()

    ids = [p.id for p in sim.players]
    assert len(ids) == len(set(ids))


# =====================================================
# Simulation execution tests
# =====================================================

def test_run_creates_players_and_plays_games():
    """
    Running the simulation should:
    - create players
    - play the requested number of games
    - produce a valid redWins count
    """
    random.seed(0)
    sim = Simulation(0, games=50, playersCount=20)
    sim.run()

    assert len(sim.players) == 20
    assert 0 <= sim.redWins <= sim.games


def test_each_game_uses_10_players():
    """
    Each game should be played with exactly 10 players.
    """
    sim = Simulation(0, games=1, playersCount=10)
    sim.createPlayers()

    players = random.sample(sim.players, 10)
    assert len(players) == 10


def test_games_increment_player_games():
    """
    At least some players should have their games counter
    incremented after the simulation runs.
    """
    random.seed(1)
    sim = Simulation(0, games=20, playersCount=20)
    sim.run()

    total_games = sum(p.games for p in sim.players)
    assert total_games > 0


def test_red_win_rate_bounds():
    """
    Red win rate should always stay within [0.1, 0.7].
    """
    random.seed(2)
    sim = Simulation(0, games=100, playersCount=20)
    sim.run()

    win_rate = sim.redWins / sim.games
    assert 0.1 < win_rate < 0.7
