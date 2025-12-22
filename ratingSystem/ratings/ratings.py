from ratingSystem.ratings.constants import DOPES_MEAN, DOPES_SIGMA, MAX_DOPES, WIN_CHANGE
import random

def getDope(player):
    """
    @brief Calculates a random "dope" value for a player based on their character.

    The dope value is sampled from a normal (Gaussian) distribution with:
    - mean determined by DOPES_MEAN(player.getCharacter())
    - standard deviation DOPES_SIGMA
    The result is clamped to [-MAX_DOPES, MAX_DOPES] to avoid extreme changes.

    @param player Player object whose dope is calculated.
    @return Float value representing the dope adjustment for this player.
    """
    dope = random.gauss(DOPES_MEAN[player.getCharacter()], DOPES_SIGMA)
    dope = max(-MAX_DOPES, min(dope, MAX_DOPES))
    return dope

def changeRating(player, won):
    """
    @brief Updates a player's rating based on game outcome and dope.

    The rating change is calculated as:
    1. Get a random dope value for the player.
    2. Add WIN_CHANGE if the player won, or subtract WIN_CHANGE if lost.
    3. Update the player's rating with the total change.

    @param player Player object whose rating is updated.
    @param won Boolean indicating if the player won (True) or lost (False).
    """
    change = getDope(player)

    if won:
        change += WIN_CHANGE
    else:
        change -= WIN_CHANGE

    player.setRating(player.getRating() + change)
