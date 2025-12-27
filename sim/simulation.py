from ratingSystem.player.player import Player
from ratingSystem.game.game import Game
import random
import math
import matplotlib.pyplot as plt

class Simulation:

    def __init__(self, id, games, playersCount = 10):
        self.id = id
        self.games = games
        self.playersCount = playersCount
        self.players = []
        self.redWins = 0
        
    def createPlayers(self):
        for i in range(self.playersCount):
            self.players.append(Player(i))

        return self.players
    
    def playGames(self):
        for i in range(self.games):
            players = random.sample(self.players, 10)
            game = Game(players)
            game.setRoles()
            if (game.play()):
                self.redWins += 1

    def displayStats(self):
        players = self.players

        ratings = [p.rating for p in players]
        games_played = [p.games for p in players]

        avg_rating = sum(ratings) / len(ratings)
        variance = sum((r - avg_rating) ** 2 for r in ratings) / len(ratings)
        std_dev = math.sqrt(variance)

        print("=== Simulation Stats ===")
        print(f"Games played: {self.games}")
        print(f"Red wins: {self.redWins}")
        print(f"Red win rate: {self.redWins / self.games:.2%}")
        print()
        print(f"Avg rating: {avg_rating:.2f}")
        print(f"Rating std dev: {std_dev:.2f}")
        print(f"Min rating: {min(ratings):.2f}")
        print(f"Max rating: {max(ratings):.2f}")
        print(f"Avg games/player: {sum(games_played) / len(players):.2f}")
        plt.hist(ratings, bins=20)
        plt.title("Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Players")
        plt.show()

    def run(self):
        self.createPlayers()
        self.playGames()
        self.displayStats()

sim = Simulation(0, 1000, 100)

sim.run()

