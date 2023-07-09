import os

from utils import File, Log

from cricket.core import EMOJI, HeadToHead, Team
from cricket.core.CWC2023_ODI_LIST import CWC2023_ODI_LIST

log = Log('cwc2023_odds')


def p_to_emoji(p):
    if p > 0.7:
        return EMOJI.COLD
    if p < 0.3:
        return EMOJI.COLD
    return EMOJI.HOT


SOUTH_ASIA_COUNTRY_LIST = [
    'India',
    'Sri Lanka',
    'Pakistan',
    'Bangladesh',
    'Afghanistan',
]


def main():
    def get_p1(team1, team2):
        num, den = 0, 0
        head_to_head_subcontinent = HeadToHead(
            team1, team2, SOUTH_ASIA_COUNTRY_LIST
        )
        if head_to_head_subcontinent.n > 0:
            num += (
                head_to_head_subcontinent.wp1 * head_to_head_subcontinent.wn
            )
            den += head_to_head_subcontinent.wn

        head_to_head_world = HeadToHead(team1, team2, [])
        if head_to_head_world.n > 0:
            num += head_to_head_world.wp1 * head_to_head_world.wn
            den += head_to_head_world.wn

        head_to_head_team1 = HeadToHead(team1, None, [])
        if head_to_head_team1.n > 0:
            num += head_to_head_team1.wp1 * head_to_head_team1.wn
            den += head_to_head_team1.wn

        head_to_head_team2 = HeadToHead(team2, None, [])
        if head_to_head_team2.n > 0:
            num += head_to_head_team2.wp1 * head_to_head_team2.wn
            den += head_to_head_team2.wn

        if den == 0:
            log.error(f'No data for {team1} vs {team2}')

        BASE_P = 1.0 / 100
        num += BASE_P / 2
        den += BASE_P

        return num / den

    prev_week = None
    lines = [
        "Predictions for the 2023 Men's ODI @CricketWorldCup",
        "GROUP STAGE",
    ]
    for odi in CWC2023_ODI_LIST:
        team1 = Team.load(odi.team1)
        team2 = Team.load(odi.team2)
        assert team1 is not team2

        week = odi.date_week
        if week != prev_week:
            lines += ['']
        prev_week = week

        p1 = get_p1(team1.name, team2.name)
        if p1 < 0.5:
            team1, team2 = team2, team1
            p1 = 1 - p1

        lines.append(
            f'{odi.date_short} {p_to_emoji(p1)} {p1:.0%} {team1} > {team2}'
        )

    lines += ['', '#CWC23']
    file_path = os.path.join('tweets', 'cwc2023_odds.txt')
    File(file_path).write('\n'.join(lines))
    log.info(f'Wrote {file_path}')


if __name__ == '__main__':
    main()
