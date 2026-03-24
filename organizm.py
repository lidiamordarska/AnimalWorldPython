from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from point2d import Point2D
from typing import Optional
import swiat

@dataclass
class Organizm(ABC):
    icon: str
    sila: int
    initiative: int
    pozycja: Point2D
    immortal: bool
    world: swiat
    age: int = 0
    previous_position: Optional[Point2D] = None

    def __post_init__(self):
        self.world.dodaj_organizm(self)

    def get_position(self):
        return self.pozycja

    def set_position(self, pozycja: Point2D, must_be_empty: bool, reproduction: bool) -> bool:
        if (pozycja.x < 0 or pozycja.x >= self.world.get_szerokosc() or
                pozycja.y < 0 or pozycja.y >= self.world.get_wysokosc()):
            return False

        if must_be_empty and self.world.get_organizm(pozycja) is not None:
            return False

        self.previous_position = self.pozycja
        other = self.world.get_organizm(pozycja)
        self.pozycja = pozycja

        if not reproduction:
            self.world.dodaj_dziennik(self, f" Moves from [{self.previous_position.x};{self.previous_position.y}] to [{self.pozycja.x};{self.pozycja.y}]")
            print(f" Moves [{self.icon}] from [{self.previous_position.x};{self.previous_position.y}] to [{self.pozycja.x};{self.pozycja.y}]")

        if other:
            other.collision(self)

        return True

    @abstractmethod
    def collision(self, other: 'Organism'):
        pass

    @abstractmethod
    def akcja(self):
        pass

    def escape(self) -> bool:
        return False

    @staticmethod
    def spawn(self, polozenie: Point2D):
        self.sklonuj(polozenie)

    def __str__(self):
        return f"{self.__class__.__name__};{self.pozycja.x};{self.pozycja.y};{self.sila};{self.age}"

    def get_initiative(self):
        return self.initiative

    def get_sila(self):
        return self.sila

    def get_age(self):
        return self.age

    def get_icon(self):
        return self.icon

    def age_up(self, value: int):
        self.age += value

    def zabij(self):
        self.pozycja = Point2D(-1, -1)
        self.sila = -1
        self.initiative = -1


    def strengthen(self, value: int):
        self.sila += value

    def cofnij_ruch(self):
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

    def rozmnoz(self, pozycja: Point2D):
        nowy = self.sklonuj(pozycja)
        self.world.dodaj_organizm(nowy)