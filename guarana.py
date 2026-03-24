from roslina import Roslina
from point2d import Point2D

class Guarana(Roslina):
    def __init__(self, position: Point2D, world):
        super().__init__('@', 0, position, False, world)

    def kolizja(self, other):
        nazwa = other.__class__.__name__
        self.world.dodaj_dziennik(self, f"Wzmocnila {nazwa}")
        other.wzmocnij(3)
        self.zabij()

    def sklonuj(self, polozenie: Point2D):
        return Guarana(polozenie, self.world)
