import os

from utils import JSONFile, Log

from cricket.core.constants import CITIES_IN_INDIA

log = Log('ODI')


class ODI:
    def __init__(
        self, date: str, venue: str, team1: str, team2: str, winner: str
    ):
        self.date = date
        self.venue = venue
        self.team1 = team1
        self.team2 = team2
        self.winner = winner

    def did_team_play(self, team: str) -> bool:
        return team in (self.team1, self.team2)

    @property
    def is_in_india(self) -> bool:
        return self.venue in CITIES_IN_INDIA

    @staticmethod
    def load(path: str):
        data = JSONFile(path).read()
        info = data["info"]
        date = info["dates"][0]
        venue = info.get("city") or info["venue"]
        teams = info["teams"]
        team1, team2 = teams
        if team1 > team2:
            team1, team2 = team2, team1
        outcome = info["outcome"]
        winner = outcome.get("winner") or "no winner"
        return ODI(date, venue, team1, team2, winner)

    @staticmethod
    def loadAll() -> list:
        odis = []
        for filename in os.listdir(os.path.join("data", "odis")):
            odi = ODI.load(os.path.join("data", "odis", filename))
            odis.append(odi)

        odis = sorted(odis, key=lambda odi: odi.date, reverse=True)
        log.info(f"Loaded {len(odis)} ODIs")
        return odis

    def __str__(self):
        icon1 = icon2 = ''
        if self.team1 == self.winner:
            icon1 = '✅'
        elif self.team2 == self.winner:
            icon2 = '✅'
        return f"{self.date} {icon1}{self.team1} vs {icon2}{self.team2}"
