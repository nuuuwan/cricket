from cricket.core.Overs import Overs
from cricket.core.Runs import Runs
from cricket.core.Wickets import Wickets


class Score:
    def __init__(self, runs: Runs, wickets: Wickets, overs: Overs):
        self.runs = runs
        self.wickets = wickets
        self.overs = overs

    def __str__(self):
        return f'{self.runs} for {self.wickets}, in {self.overs}'
