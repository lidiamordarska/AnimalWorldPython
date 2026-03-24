import random
from organizm import Organizm
from point2d import Point2D
import swiat

class Roslina(Organizm):
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

    def __init__(self, icon: str, strength: int, position: Point2D, immortal: bool, world: swiat):
        super().__init__(icon, strength, 0, position, immortal, world)

    def akcja(self):
        rozsianie = (random.random() < 0.02) # Placeholder for randomness.
        if rozsianie:
            allowed_moves = self.get_allowed_moves()
            random_move = random.randint(0, len(allowed_moves) - 1)
            for i in range(len(allowed_moves)):
                move = allowed_moves[(random_move + i) % len(allowed_moves)]
                new_position = self.pozycja + move
                if not self.world.is_in_bounds(new_position):
                    continue
                if self.world.get_organizm(new_position) is None:
                    try:
                        self.rozmnoz(new_position)
                        self.world.dodaj_dziennik(self, " Rozsianie")
                    except Exception as e:
                        print(e)
                    return

    def collision(self, other: 'Organizm'):
        if self == other:
            return
        if self.get_sila() > other.get_sila():
            other.zabij()
        elif self.get_sila() < other.get_sila():
            self.zabij()
        else:
            self.zabij()
            other.zabij()

    def get_allowed_moves(self):
        return self.ruchy
