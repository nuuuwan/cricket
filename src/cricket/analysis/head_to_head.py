from functools import cache

from cricket.core.ODI import ODI


@cache
def head_to_head_odds(gender):
    idx = ODI.load_idx2_by_teams(gender)
    idx2 = {}
    for team1 in idx:
        idx2[team1] = {}
        for team2 in idx[team1]:
            odis = idx[team1][team2]
            wn1, wn2, w = 0, 0, 0
            for odi in odis:
                w = odi.time_weight
                if odi.winner == team1:
                    wn1 += w
                elif odi.winner == team2:
                    wn2 += w
            p1 = wn1 / (wn1 + wn2)
            idx2[team1][team2] = p1
    return idx2
