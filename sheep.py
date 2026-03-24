from animal import Animal
from point2d import Point2D


class Sheep(Animal):
    def __init__(self, position: Point2D, world):
        # Zmieniłem symbol z 'o' na 'S' (Sheep)
        super().__init__('S', 4, 4, position, world)

    def clone(self, location: Point2D):
        return Sheep(location, self.world)