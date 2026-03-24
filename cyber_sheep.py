from hogweed import Hogweed
from point2d import Point2D
from animal import Animal


class CyberSheep(Animal):
    def __init__(self, position: Point2D, world):
        # Symbol zmieniony na 'C', aby pasował do metody kill_cybersheep w klasie Hogweed
        super().__init__('C', 4, 4, position, world)

    def clone(self, location: Point2D):
        return CyberSheep(location, self.world)

    def find_nearby_hogweed(self):
        # Check neighboring tiles for hogweed
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # Pomijamy sprawdzanie pola, na którym stoi sama CyberOwca
                if dx == 0 and dy == 0:
                    continue

                new_position = Point2D(self.position.get_x() + dx, self.position.get_y() + dy)
                if self.world.is_in_bounds(new_position):
                    organism = self.world.get_organism(new_position)
                    if isinstance(organism, Hogweed):
                        return organism
        return None