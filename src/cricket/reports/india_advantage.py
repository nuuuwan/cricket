from cricket.core import ODI, Team


def main():
    odis = ODI.load_list()
    filtered_odis = [
        odi
        for odi in odis
        if odi.country == 'India'
        and odi.loser is not None
        and odi.did_team_play('India')
    ]
    n_india = {}
    n_win_india = {}
    for odi in filtered_odis:
        winner = odi.winner
        loser = odi.loser
        w = 1  # odi.time_weight

        for team_name in [winner, loser]:
            n_india[team_name] = n_india.get(team_name, 0) + w
        n_win_india[winner] = n_win_india.get(winner, 0) + w

    for team_name, n_i_india in sorted(n_india.items(), key=lambda x: x[1]):
        n_i_win_india = n_win_india.get(team_name, 0)
        p_i_win_india = n_i_win_india / n_i_india
        print(f"{p_i_win_india:.0%} {Team.load(team_name)}")


if __name__ == '__main__':
    main()
