from cricket.core import CWC2023_TEAM_LIST, EMOJI, HeadToHead, Team


def p_to_emoji(p):
    if p > 0.7:
        return EMOJI.WIN
    if p < 0.3:
        return EMOJI.LOSE
    return EMOJI.DRAW


COUNTRY_LIST = ['India', 'Sri Lanka', 'Pakistan', 'Bangladesh', 'Afghanistan']


def main():
    for team1_name in CWC2023_TEAM_LIST:
        team1 = Team.load(team1_name)
        print('-' * 32)
        print(f'{team1}')
        for team2_name in CWC2023_TEAM_LIST:
            team2 = Team.load(team2_name)
            if team1 == team2:
                continue
            head_to_head = HeadToHead(team1.name, team2.name, COUNTRY_LIST)
            if head_to_head.n >= 1:
                p = head_to_head.wp1
                emoji = p_to_emoji(p)
                print(f'{emoji} {p:.0%} {team2} {head_to_head.history_emoji}')


if __name__ == '__main__':
    main()
