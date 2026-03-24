import random
from organism import Organism
from point2d import Point2D
from world import World


class Animal(Organism):
    moves = [
        Point2D(1, 0),
        Point2D(0, 1),
        Point2D(-1, 0),
        Point2D(0, -1),
        Point2D(-1, -1),
        Point2D(1, -1),
        Point2D(-1, 1),
        Point2D(1, 1)
    ]

    def __init__(self, icon: str, strength: int, initiative: int, position: Point2D, world: World):
        super().__init__(icon, strength, initiative, position, False, world)

    def action(self, world: 'World'):
        self.increase_age(1)
        allowed_moves = self.get_allowed_moves()
        move = random.randint(0, 3)
        while True:
            new_position = self.position + allowed_moves[move]
            if world.is_in_bounds(new_position):
                self.set_position(new_position, False, False)
                break
            else:
                move = (move + 1) % 4

    def collision(self, other: 'Organism', world: 'World'):
        if self == other:
            return

        if isinstance(other, self.__class__):
            if self.get_age() < 4 or other.get_age() < 4:
                return
            allowed_moves = self.get_allowed_moves()
            world.add_log(self, " reproduced")
            move = random.randint(0, 3)

            while not world.is_in_bounds(
                    self.position + allowed_moves[move % len(allowed_moves)]) or self.world.get_organism(
                    self.position + allowed_moves[move % len(allowed_moves)]) is not None:
                move += 1
                if move > 8:
                    world.add_log(self, " has no space to reproduce")
                    return
            self.undo_move()
            self.reproduce(self.position + allowed_moves[move % len(allowed_moves)])

        elif self.escape() or other.escape():
            return

        elif self.get_strength() > other.get_strength():
            world.add_log(self, " won the fight")
            other.kill()
        elif self.get_strength() < other.get_strength():
            world.add_log(self, " lost the fight")
            self.kill()
        else:
            world.add_log(self, " tied the fight (strengths are equal)")
            other.kill()

    def get_allowed_moves(self):
        return self.moves