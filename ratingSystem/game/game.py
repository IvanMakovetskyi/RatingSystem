import random
from ratingSystem.ratings.ratings import changeRating

class Game:
    """
    @brief Represents a single game simulation with Red and Black teams.
    """

    def __init__(self, players):
        """
        @brief Initializes the game with a list of Player objects.
        
        @param players List of Player objects participating in the game.
        """
        self.players = players
        self.blackPlayers = []
        self.redPlayers = []

    def setRoles(self):
        """
        @brief Assigns roles to players: first 3 are Black, the rest are Red.
        
        The method also divides players into separate lists for each team:
        - blackPlayers: first 3 players
        - redPlayers: remaining players
        """
        for i in range(0, 10):
            if i < 3:
                role = "black"
            else:
                role = "red"

            self.players[i].setRole(role)
        
        # Divide players into teams
        self.blackPlayers = self.players[:3]
        self.redPlayers = self.players[3:]

    def play(self):
        """
        @brief Simulates the game and determines if Red team wins.
        
        Computes the average rating of Red and Black teams and uses a
        probabilistic approach to determine outcome.

        @return True if Red team wins, False if Black team wins.
        """
        # Average skill of each team
        redSkill = sum(p.getRating() for p in self.redPlayers) / 7  # NOTE: hardcoded 7, should match len(redPlayers)
        blackSkill = sum(p.getRating() for p in self.blackPlayers) / 3

        # Compute Red team win probability
        if (redSkill + blackSkill) > 0:
            cityWon = redSkill / (redSkill + blackSkill)
        else:
            cityWon = 0.3

        # Random outcome based on probability
        cityWon = cityWon > random.random()  # random.random() returns float in [0,1)

        #Change rating for each player
        for p in self.players:
            #Player won:
            if (cityWon and p in self.redPlayers) or ( not cityWon and p in self.blackPlayers):
                changeRating(p, True)
            #Player lost:
            else: 
                changeRating(p, False)

        return cityWon
