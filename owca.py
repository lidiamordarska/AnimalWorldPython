from zwierze import Zwierze
from point2d import Point2D

class Owca(Zwierze):
    def __init__(self, pozycja: Point2D, swiat):
        super().__init__('o', 4, 4, pozycja, swiat)
    def sklonuj(self, polozenie: Point2D):
        return Owca(polozenie, self.world)