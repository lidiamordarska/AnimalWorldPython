from plant import Plant
from point2d import Point2D

class Guarana(Plant):
    def __init__(self, position: Point2D, world):
        super().__init__('@', 0, position, False, world)

    def collision(self, other):
        name = other.__class__.__name__
        self.world.add_log(self, f" strengthened {name}")
        other.increase_strength(3)
        self.kill()

    def clone(self, location: Point2D):
        return Guarana(location, self.world)