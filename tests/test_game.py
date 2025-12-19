import random
from ratingSystem.player.player import Player
from ratingSystem.game.game import game

# -------------------------------
# Helper: create dummy players
# -------------------------------
def create_dummy_players(num_players=10):
    players = []
    for i in range(num_players):
        p = Player(i)
        p.rating = random.randint(50, 100)  # assign random rating for testing
        players.append(p)
    return players

# -------------------------------
# Test role assignment
# -------------------------------
def test_set_roles():
    players = create_dummy_players()
    g = game(players)
    g.setRoles()

    # Check number of players per team
    assert len(g.blackPlayers) == 3
    assert len(g.redPlayers) == 7

    # Check roles are correctly assigned
    for p in g.blackPlayers:
        assert p.role == "black"
    for p in g.redPlayers:
        assert p.role == "red"

# -------------------------------
# Test play function returns boolean
# -------------------------------
def test_play_returns_boolean():
    players = create_dummy_players()
    g = game(players)
    g.setRoles()
    result = g.play()
    assert isinstance(result, bool)

# -------------------------------
# Test probabilistic outcome
# -------------------------------
def test_play_probabilistic():
    # Create players with very high rating for red team
    players = create_dummy_players()
    for i, p in enumerate(players):
        if i < 3:
            p.rating = 10  # Black team weak
        else:
            p.rating = 1000  # Red team very strong

    g = game(players)
    g.setRoles()

    # Run play multiple times, Red should almost always win
    red_wins = sum(g.play() for _ in range(100))
    assert red_wins > 90  # At least 90% wins
