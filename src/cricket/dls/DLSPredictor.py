import os
from functools import cache

from utils import File, Log

from cricket.core.Overs import Overs
from cricket.core.Runs import Runs
from cricket.core.Score import Score
from cricket.core.Wickets import Wickets

log = Log('DLSPredictor')


class DLSPredictor:
    @staticmethod
    def get_res_idx():
        res_idx = {}
        RES_FILE_PATH = os.path.join('data', 'dls', 'resources_per_over.csv')
        lines = File(RES_FILE_PATH).read_lines()
        for i_line, line in enumerate(lines[1:]):
            overs_rem = 50 - i_line
            if overs_rem not in res_idx:
                res_idx[overs_rem] = {}

            cells = line.split(',')
            for i_cell, cell in enumerate(cells[1:]):
                wickets = i_cell
                res_idx[overs_rem][wickets] = float(cell)
            res_idx[overs_rem][10] = 0
        return res_idx

    def __init__(self):
        self.res_idx = DLSPredictor.get_res_idx()

    @cache
    def project(
        self,
        score: Score,
        total_overs: Overs,
    ) -> Score:
        res_rem_at_start = self.get_res_rem(Wickets(0), total_overs)
        res_rem_now = self.get_res_rem(
            score.wickets, total_overs - score.overs
        )
        log.debug(f'{res_rem_at_start=}, {res_rem_now=}')
        runs = score.runs * (
            res_rem_at_start / (res_rem_at_start - res_rem_now)
        )
        return Score(runs, Wickets(10),total_overs)
    
    @cache
    def get_res_rem(self, wickets_lost: Wickets, overs_rem: Overs):
        overs_min = int(overs_rem.overs_total)
        overs_max = overs_min + 1
        f_overs = (overs_rem.overs_total - overs_min) * 10 / 6
        r_min = self.res_idx[overs_min][wickets_lost.value]
        r_max = self.res_idx[overs_max][wickets_lost.value]
        return round(r_min + (r_max - r_min) * f_overs, 3)


if __name__ == '__main__':
    predictor = DLSPredictor()

    score = Score(Runs(130), Wickets(5), Overs(27, 4))
    print(score)

    print(predictor.project(score, Overs(45)))
