from zwierze import Zwierze
from point2d import Point2D
from random import randint

class Czlowiek(Zwierze):
    def __init__(self, position: Point2D, world):
        super().__init__('C', 4, 4, position, world)
        self.umiejetnosc = -5
        self.kierunek = Point2D(0, 0)

    def akcja(self):
        print("Czlowiek akcja called")
        self.age_up(1)
        predkosc = 1
        if self.umiejetnosc > -5:
            self.umiejetnosc -= 1
        self.immortal = self.umiejetnosc > 0

        if self.immortal:
            print("Immortal, killing nearby organisms")
            self.kill_nearby_organisms()


        new_position = Point2D(self.pozycja.x + self.kierunek.x * predkosc, self.pozycja.y + self.kierunek.y * predkosc)
        self.set_position(new_position, False, False)  # Zmieniono reproduction na False
        self.kierunek = Point2D(0, 0)

        # Activate ability if it hasn't been activated yet
        if not self.immortal and self.umiejetnosc == -5:
            print("Activating ability")
            self.activate_ability()

    def collision(self, other):
        if self is other:
            return
        if self.umiejetnosc > 0 and self.sila <= other.sila:
            allowed_moves = self.get_allowed_moves()
            move = randint(0, 3)
            while not self.set_position(self.pozycja + allowed_moves[move], False, False):
                move = (move + 1) % 4
        # self.world.add_day_log(self, "Uwaga! Czlowiek zabija!")
        else:
            super().collision(other)

    def set_direction(self, direction):
        new_x = self.pozycja.x + direction.x
        new_y = self.pozycja.y + direction.y
        if 0 <= new_x < self.world.get_szerokosc() and 0 <= new_y < self.world.get_wysokosc():
            self.kierunek = direction

    def activate_ability(self):
        if self.umiejetnosc == -5:
            print("Ability activated")
            self.immortal = True
            self.umiejetnosc = 5

    def set_ability(self, umiejetnosc):
        self.umiejetnosc = umiejetnosc

    def escape(self):
        return self.immortal

    def kill_nearby_organisms(self):
        print("Checking nearby organisms")
        directions = [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
        for direction in directions:
            target_position = self.pozycja + direction
            if self.world.is_in_bounds(target_position):
                target_organism = self.world.get_organizm(target_position)
                if target_organism is not None and target_organism is not self:
                    print(f"Killing nearby organism: {target_organism}")
                    self.world.remove_organism(target_organism)
                    #self.world.add_day_log(self, f"{self} killed {target_organism} at {target_position}")

    def __str__(self):
        data = super().__str__()
        data += str(self.umiejetnosc) + ";"
        return data
