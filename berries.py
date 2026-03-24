from point2d import Point2D
from organism import Organism
from plant import Plant

class Berries(Plant):
    def __init__(self, position: Point2D, world):
        super().__init__('%', 99, position, False, world)

    def collision(self, other: Organism):
        if not other.is_immortal():
            name = other.__class__.__name__
            self.world.add_log(self, f" fatally poisoned {name}")
            self.kill()
            other.kill()
        else:
            self.kill()

    def clone(self, location: Point2D):
        return Berries(location, self.world)