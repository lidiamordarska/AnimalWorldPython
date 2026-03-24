import random
from point2d import Point2D
from zwierze import Zwierze
from organizm import Organizm

class Zolw(Zwierze):
    rand = random.Random()

    def __init__(self, pozycja, swiat):
        super().__init__('Z', 2, 1, pozycja, swiat)

    def akcja(self):
        robi_ruch = self.rand.randint(0, 99) >= 75  # 25% szans na ruch
        if robi_ruch:
            super().akcja()
        else:
            self.age_up(1)

    def kolizja(self, inny: Organizm):
        if inny.get_sila() < 5 and not isinstance(inny, Zolw):
            self.world.dodaj_dziennik(self, "Odparł atak")
            inny.cofnij_ruch()
        else:
            super().collision(inny)
    def sklonuj(self, polozenie: Point2D):
        return Zolw(polozenie, self.world)
