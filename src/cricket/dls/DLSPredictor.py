import os
from functools import cache

from utils import File, Log

from cricket.core.Overs import Overs

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
    def predict(
        self,
        runs: int,
        wickets_lost: int,
        overs_used: float,
        total_overs: float,
    ):
        res_rem_at_start = self.get_res_rem(0, total_overs)
        res_rem_now = self.get_res_rem(wickets_lost, total_overs - overs_used)
        log.debug(f'{res_rem_at_start=}, {res_rem_now=}')
        return int(runs * res_rem_at_start / (res_rem_at_start - res_rem_now))

    @cache
    def get_res_rem(self, wickets_lost: int, overs_rem: float):
        overs_min = int(overs_rem)
        overs_max = overs_min + 1
        f_overs = (overs_rem - overs_min) * 10 / 6
        r_min = self.res_idx[overs_min][wickets_lost]
        r_max = self.res_idx[overs_max][wickets_lost]
        return round(r_min + (r_max - r_min) * f_overs, 3)


if __name__ == '__main__':
    predictor = DLSPredictor()
    print(predictor.get_res_rem(5, Overs(17, 2).overs_total))
    print(predictor.get_res_rem(5, Overs(14, 2).overs_total))
    print(predictor.predict(130, 5, Overs(27, 4).overs_total, Overs(42).overs_total))
