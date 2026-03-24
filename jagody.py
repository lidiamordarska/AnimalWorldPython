from point2d import Point2D
from organizm import Organizm
from roslina import Roslina

class Jagody(Roslina):
    def __init__(self, pozycja: Point2D, swiat):
        super().__init__('%', 99, pozycja, False, swiat)

    def kolizja(self, inny: Organizm):
        if not inny.is_immortal():
            nazwa = inny.__class__.__name__
            self.world.dodaj_dziennik(self, f" Smiertelnie otruly {nazwa}")
            self.zabij()
            inny.zabij()
        else:
            self.zabij()

    def sklonuj(self, polozenie: Point2D):
        return Jagody(polozenie, self.world)