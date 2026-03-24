from point2d import Point2D
from roslina import Roslina
from organizm import Organizm

class Barszcz(Roslina):
    def __init__(self, position: Point2D, world):
        super().__init__('#', 10, position, False, world)

    def akcja(self):
        # Sprawdź sąsiednie pola
        ruchy = self.get_allowed_moves()
        for ruch in ruchy:
            nowa_pozycja = self.pozycja + ruch
            if (0 <= nowa_pozycja.get_x() < self.world.get_szerokosc() and
                    0 <= nowa_pozycja.get_y() < self.world.get_wysokosc()):
                sasiad = self.world.get_organizm(nowa_pozycja)
                if sasiad:
                    sasiad.collision(self)

    def kolizja(self, inny: Organizm):
        if not inny.is_immortal():
            nazwa = inny.__class__.__name__
            self.world.add_day_log(self, f"Zatrul {nazwa}")
            inny.zabij()
            self.zabij()
        else:
            self.zabij()

    def zabij_cyberowce(self):
        directions = [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
        for direction in directions:
            target_position = self.pozycja + direction
            if self.world.is_in_bounds(target_position):
                target_organism = self.world.get_organizm(target_position)
                if target_organism and target_organism.get_symbol() == 'C':
                    self.world.remove_organism(target_organism)
                    self.world.add_day_log(self, f"Zatrul CyberOwca na pozycji {target_position}")
