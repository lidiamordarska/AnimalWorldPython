from barszcz import Barszcz
from point2d import Point2D
from zwierze import Zwierze


class CyberOwca(Zwierze):
    def __init__(self, pozycja: Point2D, swiat):
        super().__init__('O', 4, 4, pozycja, swiat)

    def sklonuj(self, polozenie: Point2D):
        return CyberOwca(polozenie, self.world)

    def find_nearby_barszcz(self):
        directions = [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
        for direction in directions:
            new_position = self.pozycja + direction
            if self.world.is_in_bounds(new_position):
                organism = self.world.get_organizm(new_position)
                if isinstance(organism, Barszcz):
                    return organism
        return None

    def find_nearby_barszcz(self):
        # Sprawdź w sąsiednich polach, czy jest barszcz
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_position = Point2D(self.pozycja.x + dx, self.pozycja.y + dy)
                if self.world.is_in_bounds(new_position):
                    organism = self.world.get_organizm(new_position)
                    if isinstance(organism, Barszcz):
                        return organism
        return None
