from cricket.core import ODI


def main(team_name):
    from cricket.core.Team import TEAM_IDX, Team

    odis = ODI.load_list_for_team(team_name)
    prev_year = None
    for odi in odis:
        other_team = odi.team1 if odi.team2 == team_name else odi.team2
        if other_team not in TEAM_IDX:
            continue

        year = odi.year
        if prev_year != year:
            print('')
        prev_year = year

        icon = '✅' if odi.winner == team_name else '❌'
        print(
            f"{odi.date} ({odi.time_weight:.2f}) {icon} {Team.load(other_team)}"
        )


if __name__ == "__main__":
    TEAM = 'Sri Lanka'
    main(TEAM)
