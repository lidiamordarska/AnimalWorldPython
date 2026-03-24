from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from point2d import Point2D
from typing import Optional
from world import World  # Zmiana z 'import world' na konkretny import klasy

@dataclass
class Organism(ABC):
    icon: str
    strength: int        # Wcześniej: sila
    initiative: int
    position: Point2D    # Wcześniej: pozycja
    immortal: bool
    world: World         # Wcześniej: swiat
    age: int = 0
    previous_position: Optional[Point2D] = None

    def __post_init__(self):
        self.world.add_organism(self)  # Wcześniej: dodaj_organizm

    def get_position(self):
        return self.position

    def set_position(self, position: Point2D, must_be_empty: bool, reproduction: bool) -> bool:
        # Używamy get_x() oraz get_y() dla spójności z resztą kodu
        if (position.get_x() < 0 or position.get_x() >= self.world.get_width() or
                position.get_y() < 0 or position.get_y() >= self.world.get_height()):
            return False

        if must_be_empty and self.world.get_organism(position) is not None:
            return False

        self.previous_position = self.position
        other = self.world.get_organism(position)
        self.position = position

        if not reproduction:
            self.world.add_log(self, f" Moves from [{self.previous_position.get_x()};{self.previous_position.get_y()}] to [{self.position.get_x()};{self.position.get_y()}]")
            print(f" Moves [{self.icon}] from [{self.previous_position.get_x()};{self.previous_position.get_y()}] to [{self.position.get_x()};{self.position.get_y()}]")

        if other:
            other.collision(self)

        return True

    @abstractmethod
    def collision(self, other: 'Organism'):
        pass

    @abstractmethod
    def action(self): # Wcześniej: akcja
        pass

    @abstractmethod
    def clone(self, location: Point2D): # Dodane: abstractmethod, ponieważ każda klasa dziedzicząca tego używa!
        pass

    def escape(self) -> bool:
        return False

    @staticmethod
    def spawn(organism_instance, location: Point2D):
        # W oryginale argument nazywał się 'self', ale w metodach statycznych
        # nie używamy 'self', więc zmieniłem to na 'organism_instance'.
        return organism_instance.clone(location)

    def __str__(self):
        return f"{self.__class__.__name__};{self.position.get_x()};{self.position.get_y()};{self.strength};{self.age}"

    def get_initiative(self):
        return self.initiative

    def get_strength(self): # Wcześniej: get_sila
        return self.strength

    def get_age(self):
        return self.age

    def get_icon(self):
        return self.icon

    def increase_age(self, value: int): # Wcześniej: age_up
        self.age += value

    def kill(self): # Wcześniej: zabij
        self.position = Point2D(-1, -1)
        self.strength = -1
        self.initiative = -1

    def increase_strength(self, value: int): # Wcześniej: strengthen / wzmocnij
        self.strength += value

    def undo_move(self): # Wcześniej: cofnij_ruch
        self.set_position(self.previous_position, False, False)

    @staticmethod
    def priority(a, b) -> int:
        if a.initiative > b.initiative:
            return 1
        elif a.initiative < b.initiative:
            return 0
        else:
            return 1 if a.age > b.age else 0

    def is_immortal(self) -> bool:
        return self.immortal

    def reproduce(self, position: Point2D): # Wcześniej: rozmnoz
        new_organism = self.clone(position) # Wcześniej: sklonuj
        self.world.add_organism(new_organism)