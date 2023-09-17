class Wickets:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value == 1:
            return '1 wicket'
        return str(self.value) + ' wickets'
