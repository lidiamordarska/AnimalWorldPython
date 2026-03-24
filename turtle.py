import random
from point2d import Point2D
from animal import Animal
from organism import Organism


class Turtle(Animal):
    rand = random.Random()

    def __init__(self, position, world):
        # Zmieniłem symbol z 'Z' na 'T' (Turtle)
        super().__init__('T', 2, 1, position, world)

    def action(self):
        # 25% chance to make a move
        makes_move = self.rand.randint(0, 99) >= 75
        if makes_move:
            super().action()
        else:
            self.increase_age(1)  # Spójne z wcześniejszym tłumaczeniem (zamiast age_up)

    def collision(self, other: Organism):
        # Żółw odpiera ataki zwierząt o sile mniejszej niż 5
        if other.get_strength() < 5 and not isinstance(other, Turtle):
            self.world.add_log(self, " deflected the attack")
            other.undo_move()  # Zamiast cofnij_ruch()
        else:
            super().collision(other)

    def clone(self, location: Point2D):
        return Turtle(location, self.world)