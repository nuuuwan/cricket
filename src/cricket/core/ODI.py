import os
from functools import cache

from utils import SECONDS_IN, JSONFile, Log, Time, TimeFormat

from cricket.core.CITY_TO_COUNTRY import CITY_TO_COUNTRY
from cricket.core.CWC2023_TEAM_LIST import CWC2023_TEAM_LIST
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

    def did_teams_play(self, team1: str, team2: str) -> bool:
        return self.did_team_play(team1) and self.did_team_play(team2)
    
    def did_any_teams_play(self, teams: list[str]) -> bool:
        for team in teams:
            if self.did_team_play(team):
                return True
        return False

    @property
    def date_ut(self):
        return TimeFormat('%Y-%m-%d').parse(self.date).ut

    @property
    def date_short(self) -> str:
        return TimeFormat('%b %d').stringify(Time(self.date_ut))

    @property
    def date_week(self) -> int:
        return int((self.date_ut + SECONDS_IN.DAY * 4) / SECONDS_IN.WEEK)

    @property
    def years_ago(self):
        return (Time.now().ut - self.date_ut) / SECONDS_IN.AVG_YEAR

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

    @cache
    @staticmethod
    def load_list() -> list:
        odis = []
        for filename in os.listdir(os.path.join("data", "odis")):
            odi = ODI.load(os.path.join("data", "odis", filename))
            if odi is None:
                continue
            if not (
                odi.team1 in CWC2023_TEAM_LIST
                and odi.team2 in CWC2023_TEAM_LIST
            ):
                continue

            odis.append(odi)

        odis = sorted(odis, key=lambda odi: odi.date, reverse=True)
        log.debug(f"Loaded {len(odis)} {TEAM_TYPE}-{GENDER}-{MATCH_TYPE}")
        return odis

    @staticmethod
    def load_list_for_team(team_name: str) -> list:
        odis = ODI.load_list()
        odis = [odi for odi in odis if odi.did_team_play(team_name)]
        return odis

    @staticmethod
    def build_hypothetical(team1: str, team2: str, winner: str):
        return ODI(None, None, None, team1, team2, winner)

    def __str__(self):
        icon1 = icon2 = ''
        if self.team1 == self.winner:
            icon1 = '✅'
        elif self.team2 == self.winner:
            icon2 = '✅'
        return f"{self.date} ({self.time_weight:.2f}) {icon1}{self.team1} vs {icon2}{self.team2} [{self.city}, {self.country}]"

    @property
    def year(self):
        return self.date[:4]
