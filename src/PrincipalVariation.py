class PrincipalVariation:
    def __init__(self):
        self.pv = []

    def update(self, depth, move):
        if len(self.pv) <= depth:
            self.pv.append(move)
        else:
            self.pv[depth] = move

    def get(self, depth):
        return self.pv[:depth + 1]

    def clear(self):
        self.pv = []
