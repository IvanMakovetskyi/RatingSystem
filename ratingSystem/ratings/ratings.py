from ratingSystem.ratings import constants
import random
from math import sqrt


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
    dope = random.gauss(
        constants.CHARACTER_PARAMS[player.getCharacter()]["avgDope"] * constants.WIN_CHANGE,
        constants.DOPES_SIGMA
    )

    MAX_DOPES = constants.MAX_DOPES_COEFFICIENT * constants.WIN_CHANGE

    dope = max(-MAX_DOPES, min(dope, MAX_DOPES))
    player.avgDope = (player.avgDope * player.games + dope) / (player.games + 1)
    player.games += 1
    return dope


def calculateCoefficients(player):
    """
    @brief Calculates dynamic scaling coefficients for rating changes.

    This function returns two multiplicative coefficients:
    1. Games coefficient (g_coef):
       - Accelerates rating changes for new players.
       - Uses a square-root decay to smoothly reduce impact as the number of
         played games increases.
       - Fully disabled (g_coef = 1) after the player reaches 50 games to
         stabilize long-term ratings.

    2. Rating coefficient (r_coef):
       - Scales rating gains/losses based on the player's current rating.
       - Uses a square-root decay so lower-rated players gain more per win,
         while higher-rated players progress more slowly.
       - The coefficient approaches 1 around the target rating defined by
         RATING_COEFFICIENT_B.

    @param player Player object used to determine games played and current rating.
    @return Tuple (g_coef, r_coef) used to scale rating changes.
    """

    # Games coefficient: boosts early progression, decays smoothly with experience
    g_coef = 1
    if player.getGames() < 50:
        g_coef = (
            constants.GAMES_COEFFICIENT_A
            / sqrt(player.getGames() + constants.GAMES_COEFFICIENT_B)
        )

    # Rating coefficient: slows progression as rating increases
    r_coef = (
        constants.RATING_COEFFICIENT_A
        / sqrt(player.getRating() + constants.RATING_COEFFICIENT_B)
    )

    return g_coef, r_coef


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
    g_coef, r_coef = calculateCoefficients(player)

    if won:
        change += constants.WIN_CHANGE
    else:
        change -= constants.WIN_CHANGE
        g_coef = 1/g_coef
        r_coef = 1/r_coef

    change = change * g_coef * r_coef

    rating = player.getRating() + change

    if rating < 0:
        rating = 0

    player.setRating(rating)
