import random
from ratingSystem.ratings.ratings import changeRating
from ratingSystem.ratings import constants

class Player:
    """
    @brief Represents a single player in the rating system.
    """

    def __init__(self, id):
        """
        @brief Constructs a Player object.

        @param id Unique identifier for the player.
        """
        self.id = id
        self.rating = 0
        self.games = 0
        self.avgDope = 0
        self.redWinRate = 0
        self.blackWinRate = 0
        self.setCharacter()
        self.setWinRates()

    def setWinRates(self):
        """
        @brief Randomly using gauss distribution sets winrates to this player.

        @param redWinRate number between 0 and 1, winrate for red team
        @param blackWinRate number between 0 and 1, winrate for black team 
        """
        
        avgRedWinRate = constants.CHARACTER_PARAMS[self.character]["redWinRate"]
        avgBlackWinRate = constants.CHARACTER_PARAMS[self.character]["blackWinRate"]

        self.redWinRate = random.gauss(avgRedWinRate, constants.WINRATE_SIGMA)
        self.redBlackRate = random.gauss(avgBlackWinRate, constants.WINRATE_SIGMA)

    def setCharacter(self):
        """
        @brief Randomly assigns a performance character to the player.

        Distribution:
        - Very Bad  : 15%
        - Bad       : 20%
        - Normal    : 30%
        - Good      : 20%
        - Very Good : 15%

        @return Assigned character as a string.
        """
        roll = random.random()  # [0.0, 1.0)

        if roll < 0.15:
            self.character = "Very Bad"
        elif roll < 0.35:
            self.character = "Bad"
        elif roll < 0.65:
            self.character = "Normal"
        elif roll < 0.85:
            self.character = "Good"
        else:
            self.character = "Very Good"

        return self.character
    
    def setRole(self, role):
        """
        @brief Assigns a team role to the player.

        @param role A string representing the player's team. 
                    Example values: "red", "black".
        """
        self.role = role

    def setRating(self, rating):
        """
        @brief Sets the player's rating.

        @param rating An integer or float representing the player's rating value.
        """
        self.rating = rating  # fixed from self.role = rating

    def play(self):
        """
        @brief Simulates the outcome of a single game for the player.

        The method determines if the player wins based on either their red or black
        win rate, with a small chance to switch between them.

        Logic:
        1. Start with the player's red win rate.
        2. With 30% probability, use the black win rate instead.
        3. Generate a random number to determine if the player wins.
        4. Return True if the player won, False otherwise.

        @return Boolean indicating if the player won the game.
        """
        
        # Default win rate is the red win rate
        winrate = self.redWinRate
        
        # 30% chance to switch to black win rate
        if random.random() < 0.3:
            winrate = self.blackWinRate

        # Determine game outcome
        won = False
        if random.random() < winrate:
            won = True

        changeRating(self, won)

    def getRating(self):
        """
        @brief Returns the player's current rating.

        @return The rating value of the player (int or float).
        """
        return self.rating
    
    def getGames(self):
        """
        @brief Returns the player's games count.

        @return The number of games of the player "int".
        """
        return self.games
    
    def getCharacter(self):
        """
        @brief Returns the player's character.

        @return The character of the player "string".
        """
        return self.character
