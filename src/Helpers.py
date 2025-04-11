class NPS:
    def __init__(self, position, a, b, cavitation_margin, title="", n=1):
        self.position = position
        self.a = a
        self.b = b
        self.cavitation_margin = cavitation_margin
        self.title = title
        self.n = n

    def __str__(self):
        return f"NPS(position={self.position}, a={self.a}, b={self.b}, cavitation_margin={self.cavitation_margin})"


class Withdrawal:
    def __init__(self, position, flow):
        self.position = position
        self.flow = flow
