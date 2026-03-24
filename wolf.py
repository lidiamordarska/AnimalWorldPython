from point2d import Point2D
from animal import Animal


class Wolf(Animal):

    def __init__(self, position: Point2D):
        super().__init__('W', 9, 5, position, False)

    def clone(self, location: Point2D):
        return Wolf(location)