import random
from organism import Organism
from point2d import Point2D
from world import World  # Importujemy klasę World zamiast 'import world'

class Plant(Organism):
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

    def __init__(self, icon: str, strength: int, position: Point2D, immortal: bool, world: World):
        super().__init__(icon, strength, 0, position, immortal, world)

    def action(self):
        # 2% chance to spread
        spreads = (random.random() < 0.02)
        if spreads:
            allowed_moves = self.get_allowed_moves()
            random_move = random.randint(0, len(allowed_moves) - 1)
            for i in range(len(allowed_moves)):
                move = allowed_moves[(random_move + i) % len(allowed_moves)]
                new_position = self.position + move
                if not self.world.is_in_bounds(new_position):
                    continue
                if self.world.get_organism(new_position) is None:
                    try:
                        self.reproduce(new_position)
                        self.world.add_log(self, " spread")
                    except Exception as e:
                        print(e)
                    return

    def collision(self, other: 'Organism'):
        if self == other:
            return
        if self.get_strength() > other.get_strength():
            other.kill()
        elif self.get_strength() < other.get_strength():
            self.kill()
        else:
            self.kill()
            other.kill()

    def get_allowed_moves(self):
        return self.moves