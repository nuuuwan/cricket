import os

from utils import SECONDS_IN, JSONFile, Log, Time, TimeFormat

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

    @property
    def data_ut(self):
        return TimeFormat('%Y-%m-%d').parse(self.date).ut

    @property
    def years_ago(self):
        return (Time.now().ut - self.data_ut) / SECONDS_IN.AVG_YEAR

    @property
    def time_weight(self):
        return 1 / (2**self.years_ago)

    @staticmethod
    def load(path: str):
        data = JSONFile(path).read()
        info = data["info"]
        gender = info['gender']
        if gender != 'male':
            return None
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
            if not odi:
                continue
            odis.append(odi)

        odis = sorted(odis, key=lambda odi: odi.date, reverse=True)
        log.info(f"Loaded {len(odis)} ODIs")
        return odis

    @staticmethod
    def load_with_team(team: str) -> list:
        odis = ODI.loadAll()
        odis = [odi for odi in odis if odi.did_team_play(team)]
        return odis

    def __str__(self):
        icon1 = icon2 = ''
        if self.team1 == self.winner:
            icon1 = '✅'
        elif self.team2 == self.winner:
            icon2 = '✅'
        return f"{self.date} {icon1}{self.team1} vs {icon2}{self.team2}"

    @property
    def year(self):
        return self.date[:4]


def teams_last_games(team_name):
    from cricket.core.Team import TEAM_IDX, Team

    odis = ODI.load_with_team(team_name)
    prev_year = None
    for odi in odis:
        other_team = odi.team1 if odi.team2 == team_name else odi.team2
        if other_team not in TEAM_IDX:
            continue

        year = odi.year
        if prev_year != year:
            print('')
        prev_year = year

        icon = '✅' if odi.winner == team_name else '❌'
        print(
            f"{odi.date} ({odi.time_weight:.2f}) {icon} {Team.load(other_team)}"
        )


if __name__ == "__main__":
    TEAM = 'Sri Lanka'
    teams_last_games(TEAM)
