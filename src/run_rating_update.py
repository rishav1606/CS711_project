from typing import List
from .classes import Match, Team
from .glicko import glicko_multi_update


class RatingUpdater(object):
    r_s: float = 0

    def __init__(self, r_s):
        self.r_s = r_s

    def _get_cumul_s(self, team_s, avg_ppi, ppi):
        cumul_s = team_s + self.r_s*(ppi - avg_ppi)
        return cumul_s

    def _get_team_cumul_s(self, team: Team, result: float, ppis: List[float]):
        avg_ppi = sum(ppis)/team.get_player_count()
        cumul_sis = [self._get_cumul_s(result, avg_ppi, ppi) for ppi in ppis]
        print(cumul_sis)
        return cumul_sis

    def update_ratings(self, match: Match, ppis: List[List[float]]):
        teams = match.teams
        teams_cumul_si = [
            self._get_team_cumul_s(teams[i], match.get_team_result(i), ppis[i])
            for i in range(len(teams))]
        updated_ratings = [[], []]
        for i in range(2):
            curr_team, opp_team = teams[i], teams[1 - i]
            for player_a in range(curr_team.get_player_count()):
                player = curr_team.players[player_a]
                s_score = teams_cumul_si[i][player_a]
                others_ratings = [(p.mu, p.phi) for p in opp_team.players]
                others = [(rating, s_score) for rating in others_ratings]
                new_rating = glicko_multi_update(player.mu, player.phi, others)
                updated_ratings[i].append(new_rating)
        for i in range(2):
            curr_team = teams[i]
            for player_id in range(curr_team.get_player_count()):
                player = curr_team.players[player_id]
                player.mu = updated_ratings[i][player_id][0]
                player.phi = updated_ratings[i][player_id][1]

