class Overs:
    def __init__(self, overs: int, balls: int=0):
        assert 0 <= balls < 6
        self.overs = overs
        self.balls = balls

    @property
    def balls_total(self) -> int:
        return self.overs * 6 + self.balls

    @property
    def overs_total(self) -> float:
        return self.overs + self.balls / 6.0
