import os

from utils import JSONFile, Log

log = Log('ODI')


class ODI:
    def __init__(self, date: str, country1: str, country2: str, winner: str):
        self.date = date
        self.country1 = country1
        self.country2 = country2
        self.winner = winner

    def did_country_play(self, country: str) -> bool:
        return country in (self.country1, self.country2)

    @staticmethod
    def load(path: str):
        data = JSONFile(path).read()
        info = data["info"]
        date = info["dates"][0]
        teams = info["teams"]
        country1, country2 = teams
        outcome = info["outcome"]
        winner = outcome.get("winner") or "no winner"
        return ODI(date, country1, country2, winner)

    @staticmethod
    def loadAll() -> list:
        odis = []
        for filename in os.listdir(os.path.join("data", "odis")):
            odis.append(ODI.load(os.path.join("data", "odis", filename)))
        odis = sorted(odis, key=lambda odi: odi.date, reverse=True)
        log.info(f"Loaded {len(odis)} ODIs")
        return odis

    def __str__(self):
        icon1 = icon2 = ''
        if self.country1 == self.winner:
            icon1 = '✅'
        elif self.country2 == self.winner:
            icon2 = '✅'
        return f"{self.date} {icon1}{self.country1} vs {icon2}{self.country2}"


if __name__ == '__main__':
    odi_list = ODI.loadAll()
    for odi in odi_list:
        if odi.did_country_play('Sri Lanka'):
            print(odi)
