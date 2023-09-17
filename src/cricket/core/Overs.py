class Overs:
    def __init__(self, overs: int, balls: int = 0):
        assert 0 <= balls < 6
        self.overs = overs
        self.balls = balls

    @property
    def balls_total(self) -> int:
        return self.overs * 6 + self.balls

    @property
    def overs_total(self) -> float:
        return self.overs + self.balls / 6.0

    def __sub__(self, other):
        balls_total = self.balls_total - other.balls_total
        overs = balls_total // 6
        balls = balls_total % 6
        return Overs(overs, balls)

    def __str__(self):
        return f'{self.overs}.{self.balls} overs'
