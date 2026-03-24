from animal import Animal
from point2d import Point2D
from random import randint

class Human(Animal):
    def __init__(self, position: Point2D, world):
        # Zmieniłem symbol z 'C' na 'H' (Human), aby pasowało do nowej nazwy
        super().__init__('H', 4, 4, position, world)
        self.ability = -5
        self.direction = Point2D(0, 0)

    def action(self):
        print("Human action called")
        self.increase_age(1)  # Wcześniej age_up(1)
        speed = 1
        if self.ability > -5:
            self.ability -= 1
        self.immortal = self.ability > 0

        if self.immortal:
            print("Immortal, killing nearby organisms")
            self.kill_nearby_organisms()

        # Używam .get_x() i .get_y(), aby zachować spójność z poprzednimi plikami,
        # ale jeśli Twoja klasa Point2D pozwala na bezpośredni dostęp (.x), możesz to zmienić.
        new_position = Point2D(self.position.get_x() + self.direction.get_x() * speed,
                               self.position.get_y() + self.direction.get_y() * speed)
        self.set_position(new_position, False, False)
        self.direction = Point2D(0, 0)

        # Activate ability if it hasn't been activated yet
        if not self.immortal and self.ability == -5:
            print("Activating ability")
            self.activate_ability()

    def collision(self, other):
        if self is other:
            return
        # Używam self.get_strength() zamiennie za self.sila
        if self.ability > 0 and self.get_strength() <= other.get_strength():
            allowed_moves = self.get_allowed_moves()
            move = randint(0, 3)
            while not self.set_position(self.position + allowed_moves[move], False, False):
                move = (move + 1) % 4
        # self.world.add_log(self, "Warning! Human is killing!")
        else:
            super().collision(other)

    def set_direction(self, direction):
        new_x = self.position.get_x() + direction.get_x()
        new_y = self.position.get_y() + direction.get_y()
        if 0 <= new_x < self.world.get_width() and 0 <= new_y < self.world.get_height():
            self.direction = direction

    def activate_ability(self):
        if self.ability == -5:
            print("Ability activated")
            self.immortal = True
            self.ability = 5

    def set_ability(self, ability):
        self.ability = ability

    def escape(self):
        return self.immortal

    def kill_nearby_organisms(self):
        print("Checking nearby organisms")
        directions = [Point2D(1, 0), Point2D(-1, 0), Point2D(0, 1), Point2D(0, -1)]
        for direction in directions:
            target_position = self.position + direction
            if self.world.is_in_bounds(target_position):
                target_organism = self.world.get_organism(target_position)
                if target_organism is not None and target_organism is not self:
                    print(f"Killing nearby organism: {target_organism}")
                    self.world.remove_organism(target_organism)
                    # self.world.add_log(self, f"{self.__class__.__name__} killed {target_organism.__class__.__name__} at {target_position}")

    def __str__(self):
        data = super().__str__()
        data += str(self.ability) + ";"
        return data