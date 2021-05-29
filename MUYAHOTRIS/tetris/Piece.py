import random
from Variable import *

class Piece:

    def __init__(self, piece_name=None):
        if piece_name:
            self.piece_name = piece_name
        else:
            self.piece_name = random.choice(list(Piece_Shape.PIECES.keys()))
        self.rotation = Num.Zero
        self.array2d = Piece_Shape.PIECES[self.piece_name][self.rotation]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotate(self, clockwise=True):
        if clockwise:
            self.rotation = (self.rotation + Num.One) % Num.Four
        else:
            self.rotation = (self.rotation - Num.One) % Num.Four
        self.array2d = Piece_Shape.PIECES[self.piece_name][self.rotation]