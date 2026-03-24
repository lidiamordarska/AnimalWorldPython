import random
from point2d import Point2D
from animal import Animal


class Fox(Animal):
    rand = random.Random()

    def __init__(self, position, world):
        # Zmieniłem symbol z 'L' na 'F' (Fox)
        super().__init__('F', 3, 7, position, world)

    def action(self):
        self.increase_age(1)
        allowed_moves = self.get_allowed_moves()

        # Zabezpieczenie na wypadek braku możliwych ruchów
        if not allowed_moves:
            return

        for move in range(self.rand.randint(0, len(allowed_moves) - 1), len(allowed_moves) * 2):
            new_position = self.position + allowed_moves[move % len(allowed_moves)]

            if not self.world.is_in_bounds(new_position):
                continue

            organism = self.world.get_organism(new_position)
            if organism is None:
                self.set_position(new_position, True, False)
                return

            # Lis ma dobry węch: idzie tylko tam, gdzie przeciwnik jest słabszy (lub równy)
            if organism.get_strength() <= self.get_strength():
                self.set_position(new_position, True, False)
                return

    def clone(self, location: Point2D):
        return Fox(location, self.world)