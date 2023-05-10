from cricket.core.ODI import ODI


def head_to_head_odis():
    odis = ODI.loadAll()
    idx = {}
    for odi in odis:
        country1 = odi.country1
        country2 = odi.country2
        if country1 not in idx:
            idx[country1] = {}
        if country2 not in idx[country1]:
            idx[country1][country2] = []
        if country2 not in idx:
            idx[country2] = {}
        if country1 not in idx[country2]:
            idx[country2][country1] = []

        idx[country1][country2].append(odi)
        idx[country2][country1].append(odi)
    return idx


def head_to_head_odds():
    idx = head_to_head_odis()
    idx2 = {}
    for country1 in idx:
        idx2[country1] = {}
        for country2 in idx[country1]:
            odis = idx[country1][country2][0:10]
            n1 = len([odi for odi in odis if odi.winner == country1])
            n2 = len([odi for odi in odis if odi.winner == country2])
            p1 = n1 / (n1 + n2)
            idx2[country1][country2] = p1
    return idx2


if __name__ == '__main__':
    idx = head_to_head_odds()
    for country1 in idx:
        for country2 in idx[country1]:
            if 'Sri Lanka' == country1:
                print(f"{country1} vs {country2}: {idx[country1][country2]}")
