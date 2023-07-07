import random
from functools import cache

from cricket.core import CWC2023_TEAM_LIST, ODI, HeadToHead, Team

GENDER = 'male'
SOUTH_ASIA_COUNTRY_LIST = [
    'India',
    'Sri Lanka',
    'Pakistan',
    'Bangladesh',
    'Afghanistan',
]

MIN_ODIS = 20


class CWC2023:
    @property
    def teams(self):
        return CWC2023_TEAM_LIST

    @cache
    def get_p(self, team1: str, team2: str):
        h2h_india = HeadToHead(team1, team2, ['India'])
        if h2h_india.n >= MIN_ODIS:
            p1 = h2h_india.wp1
            print(team1, team2, p1, 'india')
        else:
            h2h_south_asia = HeadToHead(team1, team2, SOUTH_ASIA_COUNTRY_LIST)
            if h2h_south_asia.n >= MIN_ODIS:
                p1 = h2h_south_asia.wp1
                print(team1, team2, p1, 'south_asia')
            else:
                h2h_all = HeadToHead(team1, team2, [])
                p1 = h2h_all.wp1
                print(team1, team2, p1, 'all')
        return p1

    def simulate_match(self, team1: str, team2: str) -> str:
        p1 = self.get_p(team1, team2)
        return team1 if random.random() < p1 else team2

    def simulate_league_state(self):
        teams = self.teams
        n = len(teams)
        odi_list = []
        for i1 in range(n - 1):
            for i2 in range(i1 + 1, n):
                team1 = teams[i1]
                team2 = teams[i2]
                winner = self.simulate_match(team1, team2)
                odi = ODI.build_hypothetical(team1, team2, winner)
                odi_list.append(odi)
        return odi_list

    def simulate_league_table(self):
        odi_list = self.simulate_league_state()
        table = {}
        for odi in odi_list:
            winner = odi.winner
            if winner not in table:
                table[winner] = 0
            table[winner] += 1
        table = dict(
            sorted(
                table.items(),
                key=lambda item: item[1] + random.random() * 0.1,
                reverse=True,
            )
        )
        return table

    def simulate_knockouts(self):
        table = self.simulate_league_table()
        top_teams = list(table.keys())[0:4]
        sf11, sf12 = top_teams[0], top_teams[3]
        sf21, sf22 = top_teams[1], top_teams[2]
        f1 = self.simulate_match(sf11, sf12)
        f2 = self.simulate_match(sf21, sf22)
        winner = self.simulate_match(f1, f2)
        return winner


if __name__ == '__main__':
    cwc = CWC2023()
    N_G = 100_000
    team_to_wins = {}
    for g in range(0, N_G):
        print(f'{g=}', end='\r')
        winner = cwc.simulate_knockouts()
        if winner not in team_to_wins:
            team_to_wins[winner] = 0
        team_to_wins[winner] += 1
    print('\n' * 2)
    for team, n_wins in sorted(
        team_to_wins.items(), key=lambda item: item[1], reverse=True
    ):
        p_wins = n_wins / N_G
        print(
            f"{p_wins:.1%}\t{Team.load(team).emoji} {Team.load(team).hashtag}"
        )
