from ratingSystem.player.player import Player
from ratingSystem.game.game import Game
import random
import math
import matplotlib.pyplot as plt


class Simulation:
    """
    Simulation class responsible for:
    - creating players
    - running multiple games
    - tracking red team wins
    - collecting statistics for UI or analysis
    """

    def __init__(self, id, games, playersCount=10):
        """
        Initialize a simulation instance.

        :param id: Simulation identifier
        :param games: Number of games to simulate
        :param playersCount: Total number of players in the simulation
        """
        self.id = id
        self.games = games
        self.playersCount = playersCount
        self.players = []
        self.redWins = 0

    def createPlayers(self):
        """
        Create Player objects and store them in the simulation.

        Each player is assigned a unique ID based on creation order.

        :return: List of created players
        """
        for i in range(self.playersCount):
            self.players.append(Player(i))

        return self.players

    def playGames(self):
        """
        Run the simulation for the specified number of games.

        For each game:
        - randomly select 10 players
        - assign roles
        - play the game
        - count red team wins
        """
        for _ in range(self.games):
            players = random.sample(self.players, 10)
            game = Game(players)
            game.setRoles()

            if game.play():
                self.redWins += 1

    def getStats(self):
        """
        Collect aggregated statistics from the simulation.
        Instead of failing if 'character' is missing, 
        we use 'Unknown' as default.
        """
        players = self.players
        ratings = [p.rating for p in players]

        avg_rating = sum(ratings) / len(ratings)
        variance = sum((r - avg_rating) ** 2 for r in ratings) / len(ratings)

        # Group ratings by character safely
        char_histograms = {}
        for p in players:
            char = getattr(p, "character", "Unknown")  # fallback
            if char not in char_histograms:
                char_histograms[char] = []
            char_histograms[char].append(p.rating)

        return {
            "games": self.games,
            "redWins": self.redWins,
            "redWinRate": self.redWins / self.games if self.games else 0,
            "avgRating": avg_rating,
            "stdDev": math.sqrt(variance),
            "minRating": min(ratings),
            "maxRating": max(ratings),
            "ratings": ratings,
            "players": players,
            "charHistograms": char_histograms,
        }



    def run(self):
        """
        Execute the full simulation lifecycle:
        - create players
        - play games
        """
        self.createPlayers()
        self.playGames()
