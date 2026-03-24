from point2d import Point2D
from roslina import Roslina

class Mlecz(Roslina):
    def __init__(self, position: Point2D, world):
        super().__init__('*', 0, position, False, world)

    def akcja(self):
        for _ in range(3):
            super().akcja()

    def sklonuj(self, polozenie: Point2D):
        return Mlecz(polozenie, self.world)