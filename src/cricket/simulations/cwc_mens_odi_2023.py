import random

from cricket.analysis.head_to_head import head_to_head_odds
from cricket.core.ODI import ODI
from cricket.core.Team import Team


class CWC2023:
    def __init__(self):
        self.odds = head_to_head_odds()

    @property
    def teams(self) -> list[str]:
        return [
            'Afghanistan',
            'Australia',
            'Bangladesh',
            'England',
            'India',
            'Netherlands',
            'New Zealand',
            'Pakistan',
            'South Africa',
            'Sri Lanka',
        ]

    def simulate_match(self, team1: str, team2: str) -> str:
        p1 = self.odds.get(team1, {}).get(team2, 0.5)
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
                odi = ODI(None, None, team1, team2, winner)
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
        table = CWC2023().simulate_league_table()
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
        winner = cwc.simulate_knockouts()
        if winner not in team_to_wins:
            team_to_wins[winner] = 0
        team_to_wins[winner] += 1
    for team, n_wins in sorted(
        team_to_wins.items(), key=lambda item: item[1], reverse=True
    ):
        p_wins = n_wins / N_G
        print(
            f"{p_wins:.1%}\t{Team.load(team).emoji} {Team.load(team).hashtag}"
        )
