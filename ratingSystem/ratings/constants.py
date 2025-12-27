WIN_CHANGE = 25
MAX_DOPES = WIN_CHANGE * 2
DOPES_SHIFT = 10
DOPES_MEAN = {
    "Very Bad": -DOPES_SHIFT,
    "Bad" : -DOPES_SHIFT / 2,
    "Normal": 0,
    "Good": DOPES_SHIFT,
    "Very Good": DOPES_SHIFT * 2
}
DOPES_SIGMA = 10
