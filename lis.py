import random
from point2d import Point2D
from zwierze import Zwierze

class Lis(Zwierze):
    rand = random.Random()

    def __init__(self, pozycja, swiat):
        super().__init__('L', 3, 7, pozycja, swiat)

    def akcja(self):
        self.age_up(1)
        allowed_moves = self.get_allowed_moves()
        for move in range(self.rand.randint(0, len(allowed_moves) - 1), len(allowed_moves) * 2):
            new_position = self.pozycja + allowed_moves[move % len(allowed_moves)]
            if not self.world.is_in_bounds(new_position):
                continue
            organizm = self.world.get_organizm(new_position)
            if organizm is None:
                self.set_position(new_position, True, False)
                return
            if organizm.get_sila() <= self.get_sila():
                self.set_position(new_position, True, False)
                return
    def sklonuj(self, polozenie: Point2D):
        return Lis(polozenie, self.world)