import random
from point2d import Point2D
from animal import Animal

class Antelope(Animal):
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, position, world):
        super().__init__('A', 4, 4, position, world)

    def action(self):
        self.increase_age(1)  # Wcześniej było self.age_up(1) lub self.postarz(1)
        move = random.randint(0, 3)
        # Antylopa porusza się o 2 pola
        while not self.set_position(Point2D(self.position.get_x() + 2 * Antelope.moves[move][0], self.position.get_y() + 2 * Antelope.moves[move][1]), False, False):
            move = (move + 1) % 4

    def try_escape(self):
        escapes = random.choice([True, False])
        if escapes:
            move = 0
            while not self.set_position(Point2D(self.position.get_x() + Antelope.moves[move][0], self.position.get_y() + Antelope.moves[move][1]), True, False):
                move += 1
                if move == 4:
                    self.world.add_log(self, " failed to escape")
                    return False
            self.world.add_log(self, " escaped!")
            return True
        return False

    def clone(self, location: Point2D):
        return Antelope(location, self.world)