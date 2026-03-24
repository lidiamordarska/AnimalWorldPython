from point2d import Point2D
from plant import Plant

class Dandelion(Plant):
    def __init__(self, position: Point2D, world):
        super().__init__('*', 0, position, False, world)

    def action(self):
        # Dandelion tries to spread 3 times per turn
        for _ in range(3):
            super().action()

    def clone(self, location: Point2D):
        return Dandelion(location, self.world)