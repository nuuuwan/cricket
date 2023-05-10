from functools import cache

from cricket.core.ODI import ODI


@cache
def head_to_head_odis():
    odis = ODI.loadAll()
    idx = {}
    for odi in odis:
        team1 = odi.team1
        team2 = odi.team2
        if team1 not in idx:
            idx[team1] = {}
        if team2 not in idx[team1]:
            idx[team1][team2] = []
        if team2 not in idx:
            idx[team2] = {}
        if team1 not in idx[team2]:
            idx[team2][team1] = []

        idx[team1][team2].append(odi)
        idx[team2][team1].append(odi)
    return idx


@cache
def head_to_head_odds():
    idx = head_to_head_odis()
    idx2 = {}
    for team1 in idx:
        idx2[team1] = {}
        for team2 in idx[team1]:
            odis = idx[team1][team2][0:20]
            n1 = len([odi for odi in odis if odi.winner == team1])
            n2 = len([odi for odi in odis if odi.winner == team2])
            p1 = n1 / (n1 + n2)
            idx2[team1][team2] = p1
    return idx2
