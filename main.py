from typing import List
from copy import deepcopy
from prettytable import PrettyTable
from src.classes import Rating, Team, Match
from src.run_rating_update import RatingUpdater


# Creates a Team object from user input
def get_team_information(team_name):
    print("=====")
    size = int(input(f"Enter team size of team {team_name}: "))
    print("=====\n")
    player_ratings: List[Rating] = []
    for player_id in range(size):
        print(f"--- Player {player_id}")
        mu = float(input("Enter Glicko rating: "))
        phi = float(input("Enter Glicko RD: "))
        player_ratings.append(Rating(mu, phi))
        print()
    return Team(player_ratings)


# Gets PPIs of a team's members from user input
def get_ppis_of_team(team: Team, name: str):
    team_size = team.get_player_count()
    ppis: List[float] = []
    print(f"--- For team {name}:")
    for player_id in range(team_size):
        player = team.players[player_id]
        ppi = float(input(f"Enter PPI of player {player_id + 1} (Glicko rating: {player.mu}): "))
        ppis.append(ppi)
    print()
    return ppis


# Get team and match performance information
def get_two_team_match():
    team_a = get_team_information("A")
    team_b = get_team_information("B")
    result_a = int(input("Enter the match result (0 if team A wins, 2 if team B wins, 1 if draw): "))
    match = Match(team_a, team_b, result_a)
    ppis_a = get_ppis_of_team(team_a, "A")
    ppis_b = get_ppis_of_team(team_b, "B")
    return match, [ppis_a, ppis_b]


# Diff ratings of a team and show updates
def show_team_updates(old_team: Team, new_team: Team, ppis: List[float]):
    table = PrettyTable()
    table.field_names = ['Player #', 'PPI', 'Old rating', 'New rating', 'Delta']
    team_size = old_team.get_player_count()
    for player_id in range(team_size):
        player_ppi = ppis[player_id]
        old_rating = old_team.players[player_id].mu
        new_rating = new_team.players[player_id].mu
        delta = new_rating - old_rating
        table.add_row([player_id + 1, player_ppi, old_rating, new_rating, delta])
    print(table)


# Diff ratings across a match and show updates
def show_match_updates(old_match: Match, new_match: Match, teams_ppis: List[List[float]]):
    num_of_teams = len(old_match.teams)
    for team_id in range(num_of_teams):
        show_team_updates(old_match.teams[team_id], new_match.teams[team_id], teams_ppis[team_id])


def main():
    match, team_ppis = get_two_team_match()
    memo_match = deepcopy(match)
    rating_machine = RatingUpdater(0.375)
    rating_machine.update_ratings(match, team_ppis)
    show_match_updates(memo_match, match, team_ppis)


if __name__ == "__main__":
    main()
