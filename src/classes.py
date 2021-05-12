from __future__ import annotations
from typing import List
from src.glicko import glicko_single_update

# Glicko default parameters
GLICKO_DEFAULT_RATING = 1500
GLICKO_DEFAULT_RD = 350

# Match result constants
WIN_VALUE = 2
DRAW_VALUE = 1
LOSS_VALUE = 0


class Rating(object):
    """
    Stores the Glicko rating parameters of a single player
    """
    mu: float = GLICKO_DEFAULT_RATING
    phi: float = GLICKO_DEFAULT_RD

    def __init__(self, mu=GLICKO_DEFAULT_RATING, phi=GLICKO_DEFAULT_RD):
        self.mu = mu
        self.phi = phi

    def update(self, other: Rating, result: int):
        glicko_result = result/2
        new_mu, new_phi = glicko_single_update(
            self.mu, self.phi, other.mu, other.phi, glicko_result)
        self.mu, self.phi = new_mu, new_phi


class Team(object):
    """
    Represents a team of one or more players
    """
    players: List[Rating]

    def __init__(self, ratings: List[Rating]):
        self.players = ratings

    def get_player_count(self):
        return len(self.players)

    def get_composite_player(self):
        total_mu, total_phi = 0, 0
        num_of_players = self.get_player_count()
        for player in self.players:
            total_mu += player.mu
            total_phi += player.phi
        total_mu /= num_of_players
        total_phi /= num_of_players
        player = Rating(total_mu, total_phi)
        return player


class Match(object):
    """
    Represents a match between two teams,
    storing the team info and result
    """
    teams: List[Team]  # List of two teams
    result: int  # 0 if team 1 won, 2 if team 2 won, 1 if draw

    def __init__(self, team_a: Team, team_b: Team, result: int):
        self.teams = [team_a, team_b]
        self.result = result

    def get_team_result(self, team_id: int):
        if self.result == 1:
            return 0.5
        elif self.result/2 == team_id:
            return 1
        else:
            return 0
