from random import sample
from typing import List
from classes import Rating

# Default number of players in database
DEFAULT_DB_SIZE = 50


class PlayerDatabase(object):
    """
    Maintains the information of all players
    in the data set
    """
    players: List[Rating]

    def __init__(self, count=DEFAULT_DB_SIZE):
        self.players = init_players(count)

    def get_count(self):
        return len(self.players)


# Creates an array of new players
def init_players(num_of_players):
    players = [Rating() for _ in range(num_of_players)]
    return players


# Creates two randomized teams
def select_random_teams(total_players, team_size):
    selection = sample(range(total_players), 2*team_size)
    return selection[:team_size], selection[team_size:]



