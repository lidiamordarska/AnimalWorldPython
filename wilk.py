from point2d import Point2D
from zwierze import Zwierze

class Wilk(Zwierze):

    def __init__(self, position: Point2D, world):
        super().__init__('W', 9, 5, position, world)
    def sklonuj(self, polozenie: Point2D):
        return Wilk(polozenie, self.world)
