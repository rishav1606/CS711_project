from .classes import Match


# Composite team rating update
# Create the "average" player of the other team, and
# match players of team against this composite player
def update_ratings_from_match(match: Match):
    for i, team in enumerate(match.teams):
        team_result = match.get_team_result(i)
        other_team = match.teams[2 - i]
        composite_player = other_team.get_composite_player()
        for player_a in team.players:
            player_a.update(composite_player, team_result)
