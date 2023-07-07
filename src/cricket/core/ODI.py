import os

from utils import SECONDS_IN, JSONFile, Log, Time, TimeFormat

from cricket.core.CITY_TO_COUNTRY import CITY_TO_COUNTRY
from cricket.core.CWC_TEAM_LIST import CWC_TEAM_LIST
from cricket.core.utils import extract_city

log = Log('ODI')
TEAM_TYPE = 'international'
MATCH_TYPE = 'ODI'
GENDER = 'male'


class ODI:
    def __init__(
        self,
        gender: str,
        date: str,
        city: str,
        team1: str,
        team2: str,
        winner: str,
    ):
        self.gender = gender
        self.date = date
        self.city = city
        self.team1 = team1
        self.team2 = team2
        self.winner = winner

    def did_team_play(self, team: str) -> bool:
        return team in (self.team1, self.team2)

    @property
    def data_ut(self):
        return TimeFormat('%Y-%m-%d').parse(self.date).ut

    @property
    def years_ago(self):
        return (Time.now().ut - self.data_ut) / SECONDS_IN.AVG_YEAR

    @property
    def time_weight(self):
        return 1 / (2**self.years_ago)

    @property
    def country(self) -> str:
        return CITY_TO_COUNTRY.get(self.city)

    @property
    def loser(self) -> str:
        if self.winner == self.team1:
            return self.team2
        if self.winner == self.team2:
            return self.team1
        return None

    @property
    def is_neutral(self) -> bool:
        return not self.did_team_play(self.country)

    @staticmethod
    def load(path: str):
        data = JSONFile(path).read()
        info = data["info"]
        team_type = info['team_type']
        if team_type != TEAM_TYPE:
            return None
        match_type = info['match_type']
        if match_type != MATCH_TYPE:
            return None
        gender = info['gender']
        if gender != GENDER:
            return None

        date = info["dates"][0]
        city = extract_city(info)
        teams = info["teams"]
        team1, team2 = teams
        if team1 > team2:
            team1, team2 = team2, team1
        outcome = info["outcome"]
        winner = outcome.get("winner") or "no winner"
        return ODI(gender, date, city, team1, team2, winner)

    @staticmethod
    def load_list() -> list:
        odis = []
        for filename in os.listdir(os.path.join("data", "odis")):
            odi = ODI.load(os.path.join("data", "odis", filename))
            if odi is None:
                continue
            if not (
                odi.team1 in CWC_TEAM_LIST and odi.team2 in CWC_TEAM_LIST
            ):
                continue

            odis.append(odi)

        odis = sorted(odis, key=lambda odi: odi.date, reverse=True)
        log.info(f"Loaded {len(odis)} {TEAM_TYPE}-{GENDER}-{MATCH_TYPE}")
        return odis

    @staticmethod
    def load_list_for_team(team_name: str) -> list:
        odis = ODI.load_list()
        odis = [odi for odi in odis if odi.did_team_play(team_name)]
        return odis

    @staticmethod
    def load_idx2_by_teams(gender=None):
        odis = ODI.load_list(gender)
        idx = {}

        def update(team_a, team_b, odi):
            idx[team_a] = idx.get(team_a, {})
            idx[team_a][team_b] = idx[team_a].get(team_b, [])
            idx[team_a][team_b].append(odi)

        for odi in odis:
            update(odi.team1, odi.team2, odi)
            update(odi.team2, odi.team1, odi)

        return idx

    @staticmethod
    def build_hypothetical(team1: str, team2: str, winner: str):
        return ODI(None, None, None, team1, team2, winner)

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
