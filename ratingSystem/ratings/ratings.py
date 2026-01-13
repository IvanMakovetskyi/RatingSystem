from ratingSystem.ratings import constants
from math import sqrt


def getDope(player):
    """
    @brief Calculates a  "dope" value for a player based on their character.

    @param player Player object whose dope is calculated.
    @return Float value representing the dope adjustment for this player.
    """
    dope = constants.CHARACTER_PARAMS[player.getCharacter()]["avgDope"] * constants.WIN_CHANGE * constants.DOPES_COEFFICIENT

    player.games += 1

    return dope


def calculateCoefficients(player, won):
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
        / (constants.RATING_COEFFICIENT_C * sqrt(player.getRating() + constants.RATING_COEFFICIENT_B))
    )

    if not won:
        g_coef = 1/g_coef
        r_coef = 1/r_coef

    return g_coef * r_coef

def updateRank(player):
    """
    @brief Updates the player's rank based on their current rating.

    Logic:
    1. Take the player's rating modulo 300 to determine position within the rank tiers.
    2. Map the result to a rank using the RANKS list from constants.
    3. Update the player's rank using setRank().

    @param player Player object whose rank is being updated.
    """
    # Calculate the player's position within the rank cycle
    rank = int(player.getRating() // 300)
    
    # Map the position to the actual rank name
    if rank > 6:
        rank = "Capo"
    else:
        rank = constants.RANKS[rank]
    
    # Update the player's rank
    player.setRank(rank)


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
    dope = getDope(player)
    coef = calculateCoefficients(player, won)
    change = dope

    if won:
        change += constants.WIN_CHANGE
        dif = constants.WIN_CHANGE
        
    else:
        change -= constants.WIN_CHANGE
        dif = -constants.WIN_CHANGE

    change *= coef
    dif *= coef

    rating = player.getRating() + change

    if rating < 0:
        rating = 0

    player.setRating(rating)
    updateRank(player)

    print({player.getId(): [player.getRank(), dif, dope, coef]})
    return({player.getId(): [player.getRank(), dif, dope, coef]})
