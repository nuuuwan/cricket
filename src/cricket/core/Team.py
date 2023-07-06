from cricket.core.COUNTRY_TO_EMOJI import COUNTRY_TO_EMOJI
class Team:
    def __init__(self, name: str):
        self.name = name

    @property
    def alpha3(self) -> str:
        return {
            'India': "IND",
            'Australia': 'AUS',
            'England': 'ENG',
            'New Zealand': 'NZL',
            'South Africa': 'RSA',
            'Pakistan': 'PAK',
            'Bangladesh': 'BAN',
            'West Indies': 'WIN',
            'Sri Lanka': 'SRI',
            'Afghanistan': 'AFG',
        }.get(self.name, '')

    @property
    def hashtag(self) -> str:
        return "#" + self.name.replace(' ', '')
    
    @property
    def emoji(self) -> str:
        return COUNTRY_TO_EMOJI.get(self.name, '')
