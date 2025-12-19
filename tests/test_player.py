import random
from ratingSystem.player.player import Player


def test_set_character_distribution():
    """
    @brief Tests that setCharacter follows the expected probability distribution.
    """

    random.seed(42)  # deterministic test

    trials = 100000
    counts = {
        "Very Bad": 0,
        "Bad": 0,
        "Normal": 0,
        "Good": 0,
        "Very Good": 0,
    }

    for i in range(trials):
        p = Player(i)
        counts[p.character] += 1

    # Convert to percentages
    percentages = {k: v / trials for k, v in counts.items()}

    assert 0.13 <= percentages["Very Bad"] <= 0.17
    assert 0.18 <= percentages["Bad"] <= 0.22
    assert 0.28 <= percentages["Normal"] <= 0.32
    assert 0.18 <= percentages["Good"] <= 0.22
    assert 0.13 <= percentages["Very Good"] <= 0.17
