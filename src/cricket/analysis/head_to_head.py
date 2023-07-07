from functools import cache

from cricket.core.ODI import ODI


def compute_odds(odis: list[ODI], team1: str, team2: str) -> float:
    wn1, wn2, w = 0, 0, 0
    for odi in odis:
        w = odi.time_weight
        if odi.winner == team1:
            wn1 += w
        elif odi.winner == team2:
            wn2 += w
    p1 = wn1 / (wn1 + wn2)
    return p1


@cache
def head_to_head_odds(gender: str) -> dict[str, dict[str, float]]:
    idx2 = ODI.load_idx2_by_teams(gender)
    idx_odds = {}
    for team1, idx1 in idx2.items():
        idx_odds[team1] = {}
        for team2, odis in idx1.items():
            idx_odds[team1][team2] = compute_odds(odis, team1, team2)
    return idx_odds
