from cricket.core import CWC2023_TEAM_LIST, EMOJI, HeadToHead, Team


def p_to_emoji(p):
    if p > 0.7:
        return EMOJI.WIN
    if p < 0.3:
        return EMOJI.LOSE
    return EMOJI.DRAW


SOUTH_ASIA_COUNTRY_LIST = [
    'India',
    'Sri Lanka',
    'Pakistan',
    'Bangladesh',
    'Afghanistan',
]
W_SOUTH_ASIA = 0.2
W_WORLD = 0.8


def main():
    for team1_name in ['Sri Lanka']:
        team1 = Team.load(team1_name)
        print('-' * 32)
        print(f'{team1}')
        for team2_name in CWC2023_TEAM_LIST:
            team2 = Team.load(team2_name)
            if team1 == team2:
                continue
            head_to_head_world = HeadToHead(team1.name, team2.name, [])
            head_to_head_subcontinent = HeadToHead(
                team1.name, team2.name, SOUTH_ASIA_COUNTRY_LIST
            )

            p = (
                head_to_head_world.wp1 * W_WORLD
                + head_to_head_subcontinent.wp1 * W_SOUTH_ASIA
            ) / (W_WORLD + W_SOUTH_ASIA)
            print(f'{p_to_emoji(p)} {p:.0%} {team2}')


if __name__ == '__main__':
    main()
