import random

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
        self.setCharacter()

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

    def getRating(self):
        """
        @brief Returns the player's current rating.

        @return The rating value of the player (int or float).
        """
        return self.rating
    
    def getCharacter(self):
        """
        @brief Returns the player's character.

        @return The character of the player "string".
        """
        return self.character
