from functools import cached_property

from cricket.core.EMOJI import EMOJI
from cricket.core.ODI import ODI


class HeadToHead:
    def __init__(self, team1, team2, country_list=[]):
        self.team1 = team1
        self.team2 = team2
        self.country_list = country_list

    @cached_property
    def odis(self) -> list[ODI]:
        odis = ODI.load_list()
        filtered_odis = [
            odi for odi in odis if odi.did_teams_play(self.team1, self.team2)
        ]
        if self.country_list:
            filtered_odis = [
                odi
                for odi in filtered_odis
                if odi.country in self.country_list
            ]
        return filtered_odis

    @cached_property
    def team1_win_odis(self):
        return [odi for odi in self.odis if odi.winner == self.team1]

    @cached_property
    def team2_win_odis(self):
        return [odi for odi in self.odis if odi.winner == self.team2]

    @cached_property
    def n1(self):
        return len(self.team1_win_odis)

    @cached_property
    def n2(self):
        return len(self.team2_win_odis)

    @cached_property
    def n(self):
        return self.n1 + self.n2

    @cached_property
    def p1(self):
        return self.n1 / self.n

    @cached_property
    def wn1(self):
        return sum([odi.time_weight for odi in self.team1_win_odis])

    @cached_property
    def wn2(self):
        return sum([odi.time_weight for odi in self.team2_win_odis])
``
    @cached_property
    def wn(self):
        return self.wn1 + self.wn2

    @cached_property
    def wp1(self):
        if self.wn1 + self.wn2 == 0:
            return 0.5
        return self.wn1 / (self.wn1 + self.wn2)

    @cached_property
    def history_emoji(self):
        N_HISTORY_EMOJI = 5
        return ''.join(
            [
                EMOJI.WIN if odi.winner == self.team1 else EMOJI.LOSE
                for odi in self.odis[:N_HISTORY_EMOJI]
            ]
        )
