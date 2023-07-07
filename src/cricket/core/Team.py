class Team:
    def __init__(self, alpha3: str, name: str, emoji: str):
        self.alpha3 = alpha3
        self.name = name
        self.emoji = emoji

    @property
    def hashtag(self) -> str:
        return "#" + self.name.replace(' ', '')

    @staticmethod
    def load_list():
        return TEAMS

    @staticmethod
    def load(team_name):
        return TEAM_IDX[team_name]

    def __str__(self):
        return f"{self.emoji} {self.hashtag}"

    def __eq__(self, other):
        return isinstance(other, Team) and self.name == other.name


TEAMS = [
    Team('AFG', 'Afghanistan', '🇦🇫'),
    Team('AUS', 'Australia', '🇦🇺'),
    Team('BAN', 'Bangladesh', '🇧🇩'),
    Team('ENG', 'England', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
    Team('IND', 'India', '🇮🇳'),
    Team('NLD', 'Netherlands', '🇳🇱'),
    Team('NZL', 'New Zealand', '🇳🇿'),
    Team('PAK', 'Pakistan', '🇵🇰'),
    Team('RSA', 'South Africa', '🇿🇦'),
    Team('SRI', 'Sri Lanka', '🇱🇰'),
]
TEAM_IDX = {team.name: team for team in TEAMS}
