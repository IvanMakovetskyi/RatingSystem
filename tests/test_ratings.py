import pytest
import random
from ratingSystem.player.player import Player
from ratingSystem.ratings.ratings import getDope, changeRating
from ratingSystem.ratings.constants import MAX_DOPES, WIN_CHANGE

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
