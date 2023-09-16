import os

from utils import File, Log

from cricket.core import (CWC2023_ODI_LIST, EMOJI, SOUTH_ASIA_COUNTRY_LIST,
                          HeadToHead, Team)

log = Log('cwc2023_odds')

P_HOT =1.0/3


def p_to_emoji(p):
    if p > 1 - P_HOT:
        return EMOJI.WIN
    if p < P_HOT:
        return EMOJI.LOSE
    return EMOJI.DRAW

def prune_hashtags(lines):
    hashtag_set = set()
    pruned_lines = []
    for line in lines:
        words = line.split()
        pruned_line = line
        for word in words:
            if word.startswith('#'):
                if word in hashtag_set:
                    pruned_line = pruned_line.replace(word, word[1:])
                else:
                    hashtag_set.add(word)
        pruned_lines.append(pruned_line)
    return pruned_lines


def get_p1(team1, team2):
    num, den = 0, 0

    # SOUTH ASIA
    W_SOUTH_ASIA = 0.25
    h2h_south_asia = HeadToHead(
        lambda odi: (
            odi.winner == team1
            and odi.loser == team2
            and odi.country in SOUTH_ASIA_COUNTRY_LIST
        ),
        lambda odi: (
            odi.winner == team2
            and odi.loser == team1
            and odi.country in SOUTH_ASIA_COUNTRY_LIST
        ),
    )
    if h2h_south_asia.n > 0:
        num += h2h_south_asia.wp1 * h2h_south_asia.wn * W_SOUTH_ASIA
        den += h2h_south_asia.wn * W_SOUTH_ASIA

    # WORLD
    W_WORLD = 0.25
    head_to_head_world = HeadToHead(
        lambda odi: (odi.winner == team1 and odi.loser == team2),
        lambda odi: (odi.winner == team2 and odi.loser == team1),
    )
    if head_to_head_world.n > 0:
        num += head_to_head_world.wp1 * head_to_head_world.wn * W_WORLD
        den += head_to_head_world.wn * W_WORLD

    # ALL TEAMS
    W_ALL_TEAMS = 0.5
    head_to_head_world_all_team1 = HeadToHead(
        lambda odi: (odi.winner == team1 and odi.loser in CWC2023_ODI_LIST),
        lambda odi: (odi.winner in CWC2023_ODI_LIST and odi.loser == team1),
    )
    head_to_head_world_all_team2 = HeadToHead(
        lambda odi: (odi.winner == team2 and odi.loser in CWC2023_ODI_LIST),
        lambda odi: (odi.winner in CWC2023_ODI_LIST and odi.loser == team2),
    )

    if (
        head_to_head_world_all_team1.n > 0
        and head_to_head_world_all_team2.n > 0
    ):
        num += head_to_head_world_all_team1.wp1 * W_ALL_TEAMS
        den += (
            head_to_head_world_all_team1.wp1
            + head_to_head_world_all_team2.wp1
        ) * W_ALL_TEAMS

    p1 = num / den
    W_NOISE = 0.1
    return p1 * (1 - W_NOISE) + (1 - p1) * W_NOISE


def main():
    TEAM = Team.load('Sri Lanka')
    prev_week = None
    lines = [
        "2023 Men's #ODI @CricketWorldCup",
        f"{TEAM} #GroupStage Odds",
        '',
    ]
    for odi in CWC2023_ODI_LIST:
        team1 = Team.load(odi.team1)
        team2 = Team.load(odi.team2)

        if TEAM not in [team1, team2]:
            continue
        assert team1 is not team2

        week = odi.date_week
        if week != prev_week:
            lines += ['']
        prev_week = week

        p1 = get_p1(team1.name, team2.name)

        if team2 == TEAM:
            team1, team2 = team2, team1
            p1 = 1 - p1

        lines.append(
            f'{p_to_emoji(p1)} {p1:.0%} {team2}'
        )

    lines += ['', '#CWC23', '⚠️ Work-in-progress']
    file_path = os.path.join('tweets', 'group_state_cwc2023.txt')
    lines = prune_hashtags(lines)
    File(file_path).write('\n'.join(lines))
    log.info(f'Wrote {file_path}')


if __name__ == '__main__':
    main()
