import os
import random
from functools import cache

from utils import File, Log, Time, TimeFormat

from cricket.core import CWC2023_TEAM_LIST, ODI, Team
from cricket.reports.group_state_cwc2023 import get_p1, prune_hashtags

log = Log('cwc2023')


class CWC2023:
    @property
    def teams(self):
        return CWC2023_TEAM_LIST

    @cache
    def get_p(self, team1: str, team2: str):
        return get_p1(team1, team2)

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

    lines = [
        "Predictions for the 2023 Men's ODI 🏏@CricketWorldCup",
        "WINNER",
        '⚠️ Work-in-progress. Still improving models.',
        '',
    ]

    for team, n_wins in sorted(
        team_to_wins.items(), key=lambda item: item[1], reverse=True
    ):
        p_wins = n_wins / N_G
        lines.append(f"{p_wins:.0%} {Team.load(team)}")

    date_str = TimeFormat('%Y-%m-%d').stringify(Time.now())
    lines += ['', f'Updated {date_str}', '#CWC23']
    file_path = os.path.join('tweets', 'winner_cwc2023.txt')
    lines = prune_hashtags(lines)
    File(file_path).write('\n'.join(lines))
    log.info(f'Wrote {file_path}')
