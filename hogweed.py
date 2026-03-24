from point2d import Point2D
from plant import Plant
from organism import Organism

class Hogweed(Plant):
    def __init__(self, position: Point2D, world):
        super().__init__('#', 10, position, False, world)

    def action(self):
        # Check neighboring tiles
        moves = self.get_allowed_moves()
        for move in moves:
            new_position = self.position + move
            if (0 <= new_position.get_x() < self.world.get_width() and
                    0 <= new_position.get_y() < self.world.get_height()):
                neighbor = self.world.get_organism(new_position)
                if neighbor:
                    neighbor.collision(self)

    def collision(self, other: Organism):
        if not other.is_immortal():
            name = other.__class__.__name__
            self.world.add_log(self, f" poisoned {name}")
            other.kill()
            self.kill()
        else:
            self.kill()

    def kill_cybersheep(self):
        directions = [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
        for direction in directions:
            target_position = self.position + direction
            if self.world.is_in_bounds(target_position):
                target_organism = self.world.get_organism(target_position)
                if target_organism and target_organism.get_symbol() == 'C':
                    self.world.remove_organism(target_organism)
                    self.world.add_log(self, f" poisoned CyberSheep at position {target_position}")