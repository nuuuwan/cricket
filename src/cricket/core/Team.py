from cricket.core.constants import COUNTRY_TO_ALPHA3, COUNTRY_TO_EMOJI


class Team:
    def __init__(self, name: str):
        self.name = name

    @property
    def alpha3(self) -> str:
        return COUNTRY_TO_ALPHA3.get(self.name, '')

    @property
    def hashtag(self) -> str:
        return "#" + self.name.replace(' ', '')

    @property
    def emoji(self) -> str:
        return COUNTRY_TO_EMOJI.get(self.name, '')
