from functools import cached_property

from cricket.core.ODI import ODI


class HeadToHead:
    def __init__(self, func_team1, func_team2):
        self.func_team1 = func_team1
        self.func_team2 = func_team2

    @cached_property
    def team1_win_odis(self):
        odis = ODI.load_list()
        return [odi for odi in odis if self.func_team1(odi)]

    @cached_property
    def team2_win_odis(self):
        odis = ODI.load_list()
        return [odi for odi in odis if self.func_team2(odi)]

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

    @cached_property
    def wn(self):
        return self.wn1 + self.wn2

    @cached_property
    def wp1(self):
        if self.wn1 + self.wn2 == 0:
            return 0.5
        return self.wn1 / (self.wn1 + self.wn2)
