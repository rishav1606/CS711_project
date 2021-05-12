import math
from typing import List, Tuple

GLICKO_Q = 0.00575646273  # ln(10)/400

GLICKO_DEFAULT_RD = 350
PERIODS_FOR_RD_RESET = 100
AVERAGE_RD = 50
RD_C = math.sqrt((GLICKO_DEFAULT_RD**2 - AVERAGE_RD**2)/PERIODS_FOR_RD_RESET)


# Determines new RD from old RD
def _get_new_rd(old_rd, periods):
    new_rd_value = math.sqrt(old_rd**2 + periods*(RD_C**2))
    new_rd = min(new_rd_value, GLICKO_DEFAULT_RD)
    return new_rd


# Glicko's g function
def _glicko_g(rd):
    inside_sqrt = 1 + 3*((GLICKO_Q*rd/math.pi)**2)
    return 1/math.sqrt(inside_sqrt)


# Glicko's E function
def _glicko_e(mu_1, mu_2, rd_2):
    exponential = (_glicko_g(rd_2)*(mu_1 - mu_2))/(-400)
    denominator = 1 + math.pow(10, exponential)
    return 1/denominator


def _glicko_d_sq(player_mu, others: List[Tuple[float, float]]):
    d_sq_denominator = 0
    for rating in others:
        other_mu, other_phi = rating
        g_sq = _glicko_g(other_phi) ** 2
        e_value = _glicko_e(player_mu, other_mu, other_phi)
        sum_value = g_sq * e_value * (1 - e_value)
        d_sq_denominator += sum_value
    d_sq_denominator *= GLICKO_Q ** 2
    return 1 / d_sq_denominator


# Runs the Glicko algorithm given a player's initial rating and series of games
def glicko_multi_update(player_mu, player_phi, others: List[Tuple[Tuple[float, float], float]]):
    others_ratings = [x[0] for x in others]
    d_sq = _glicko_d_sq(player_mu, others_ratings)
    # Find summation
    main_sum = 0
    for opp_rating, result in others:
        opp_mu, opp_phi = opp_rating
        term_1 = _glicko_g(opp_phi)
        term_2 = result - _glicko_e(player_mu, opp_mu, opp_phi)
        main_sum += term_1*term_2
    # Find multiplying term: q / (1/RD^2 + 1/d^2)
    temp_rd = _get_new_rd(player_phi, 1)
    denominator = 1/(temp_rd**2) + 1/d_sq
    multiplying_term = GLICKO_Q/denominator
    # Calculate new rating and RD
    new_player_mu = player_mu + multiplying_term*main_sum
    new_player_phi = 1/math.sqrt(denominator)
    return new_player_mu, new_player_phi


# Updates a player's rating on a single game
def glicko_single_update(mu1, phi1, mu2, phi2, result):
    return glicko_multi_update(mu1, phi1, [((mu2, phi2), result)])


if __name__ == "__main__":
    print(glicko_single_update(1500, 350, 1500, 350, 1))
