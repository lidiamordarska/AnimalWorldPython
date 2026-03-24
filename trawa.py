from roslina import Roslina
from point2d import Point2D


class Trawa(Roslina):
    def __init__(self, position: Point2D, world):
        super().__init__(',', 0, position, False, world)

    def sklonuj(self, polozenie: Point2D):
        return Trawa(polozenie, self.world)
