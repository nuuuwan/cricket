class Runs:
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        if self.value == 1:
            return '1 run'
        return str(self.value) + ' runs'

    def __mul__(self, other):
        return Runs(int(self.value * other))
