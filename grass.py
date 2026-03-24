from plant import Plant
from point2d import Point2D

class Grass(Plant):
    def __init__(self, position: Point2D, world):
        super().__init__(',', 0, position, False, world)

    def clone(self, location: Point2D):
        return Grass(location, self.world)