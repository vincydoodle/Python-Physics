class sim():
    def __init__(self, G, m1, m2, d):
        self.G = G
        self.m1 = m1
        self.m2 = m2
        self.d = d
        self.F = (G * m1 * m2) / d**2
        self.w1 = m1 * G
        self.w2 = m2 * G

    def move(self):
        pass
