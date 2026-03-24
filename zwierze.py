import random
from organizm import Organizm
from point2d import Point2D
import swiat

class Zwierze(Organizm):
    ruchy = [
        Point2D(1, 0),
        Point2D(0, 1),
        Point2D(-1, 0),
        Point2D(0, -1),
        Point2D(-1, -1),
        Point2D(1, -1),
        Point2D(-1, 1),
        Point2D(1, 1)
    ]

    def __init__(self, icon: str, strength: int, initiative: int, position: Point2D, world: swiat):
        super().__init__(icon, strength, initiative, position, False, world)

    def akcja(self):
        self.age_up(1)
        allowed_moves = self.get_allowed_moves()
        ruch = random.randint(0, 3)
        while True:
            new_position = self.pozycja + allowed_moves[ruch]
            if self.world.is_in_bounds(new_position):
                self.set_position(new_position, False, False)
                break
            else:
                ruch = (ruch + 1) % 4

    def collision(self, other: 'Organizm'):
        if self == other:
            return
        if isinstance(other, self.__class__):
            if self.get_age() < 4 or other.get_age() < 4:
                return
            allowed_moves = self.get_allowed_moves()
            self.world.dodaj_dziennik(self, " rozmnozyl/a sie")
            ruch = random.randint(0, 3)
            while not self.world.is_in_bounds(self.pozycja + allowed_moves[ruch]) or self.world.get_organizm(self.pozycja + allowed_moves[ruch]) is not None:
                ruch += 1
                if ruch > 8:
                    self.world.dodaj_dziennik(self, " nie ma miejsca na rozmnozenie")
                    return
            self.cofnij_ruch()
            self.rozmnoz(self.pozycja + allowed_moves[ruch])
        elif self.escape() or other.escape():
            return
        elif self.get_sila() > other.get_sila():
            self.world.dodaj_dziennik(self, " wygral/a walke")
            other.zabij()
        elif self.get_sila() < other.get_sila():
            self.world.dodaj_dziennik(self, " przegral/a walke")
            self.zabij()
        else:
            self.world.dodaj_dziennik(self, " sily sa rowne")
            other.zabij()

    def get_allowed_moves(self):
        return self.ruchy
