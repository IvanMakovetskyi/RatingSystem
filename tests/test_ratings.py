import pytest
import random
from ratingSystem.player.player import Player
from ratingSystem.game.game import Game
from ratingSystem.ratings.ratings import getDope, changeRating
from ratingSystem.ratings.constants import MAX_DOPES, WIN_CHANGE, DOPES_MEAN
from tests.test_game import create_dummy_players

# -------------------------------
# Helper: create a dummy player
# -------------------------------
def create_player(character="Normal", rating=100):
    p = Player(0)
    p.character = character
    p.rating = rating
    return p

# -------------------------------
# Test getDope returns values within bounds
# -------------------------------
def test_getDope_bounds():
    random.seed(42)
    player = create_player("Good")
    for _ in range(1000):
        dope = getDope(player)
        assert -MAX_DOPES <= dope <= MAX_DOPES

# -------------------------------
# Test changeRating increases rating on win
# -------------------------------
def test_changeRating_win():
    random.seed(42)
    player = create_player("Normal", rating=100)
    old_rating = player.getRating()
    changeRating(player, won=True)
    assert player.getRating() >= old_rating  # rating should increase

# -------------------------------
# Test changeRating decreases rating on loss
# -------------------------------
def test_changeRating_loss():
    random.seed(42)
    player = create_player("Normal", rating=100)
    old_rating = player.getRating()
    changeRating(player, won=False)
    assert player.getRating() <= old_rating  # rating should decrease

# -------------------------------
# Test rating stays within reasonable range after multiple updates
# -------------------------------
def test_rating_clamped():
    random.seed(42)
    player = create_player("Very Good", rating=100)
    for _ in range(1000):
        changeRating(player, won=True)
        assert player.getRating() <= 100 + (MAX_DOPES + WIN_CHANGE) * 1000
        assert player.getRating() >= 100 - (MAX_DOPES - WIN_CHANGE) * 1000

# -----------------------------------
# Test rating update modifies player stats
# -----------------------------------
def test_change_rating_updates_stats():
    random.seed(42)

    p = Player(1)
    p.character = "Normal"
    p.rating = 100

    changeRating(p, won=True)

    assert p.games == 1
    assert isinstance(p.avgDope, float)


# -----------------------------------
# Test avgDope calculation and games counter
# -----------------------------------
def test_avg_dope_and_games_increment():
    random.seed(42)

    players = create_dummy_players()
    game = Game(players)
    
    for p in players:
        assert p.games == 0
        assert p.avgDope == 0

    for _ in range(10000):
        game.play()

    for p in players:
        meanDope = DOPES_MEAN[p.getCharacter()]
        assert abs(p.avgDope - meanDope) < 0.15
        assert p.games == 10000

    #Print Players Rating
    """
    for i in range(10):
        print(f" \n Player {i} ({players[i].getCharacter()}) rating: {players[i].getRating()} \n")
    """
