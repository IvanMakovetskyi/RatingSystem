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
