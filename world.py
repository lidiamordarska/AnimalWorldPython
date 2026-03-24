import csv
from typing import List
from point2d import Point2D
from organism import Organism
from human import Human
from grass import Grass
from guarana import Guarana
from sheep import Sheep
from hogweed import Hogweed
from dandelion import Dandelion
from berries import Berries
from antelope import Antelope
from fox import Fox
from turtle import Turtle
from wolf import Wolf
from cyber_sheep import CyberSheep


class World:
    instance = None

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.organisms = []
        self.turn = 0
        self.human = None
        self.logs = []

    @classmethod
    def get_instance(cls, width: int = None, height: int = None):
        if cls.instance is None and width is not None and height is not None:
            cls.instance = cls(width, height)
        return cls.instance

    @classmethod
    def get_instance_from_file(cls, filename: str):
        instance = None
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            first_line = next(reader)
            turn, width, height = map(int, first_line)
            instance = cls(width, height)
            instance.turn = turn

            for row in reader:
                if not row:
                    continue
                name, x, y, strength, age, *rest = row
                x, y, strength, age = map(float, (x, y)) if '.' in x else map(int, (x, y, strength, age))
                obj = None

                if name == "Human":
                    obj = Human(Point2D(x, y), instance)
                    instance.human = obj
                    ability = int(rest[0])
                    instance.human.set_ability(ability)
                elif name == "Antelope":
                    obj = Antelope(Point2D(x, y), instance)
                elif name == "Grass":
                    obj = Grass(Point2D(x, y), instance)
                elif name == "Sheep":
                    obj = Sheep(Point2D(x, y), instance)
                elif name == "Wolf":
                    obj = Wolf(Point2D(x, y), instance)
                elif name == "Dandelion":
                    obj = Dandelion(Point2D(x, y), instance)
                elif name == "Guarana":
                    obj = Guarana(Point2D(x, y), instance)
                elif name == "Hogweed":
                    obj = Hogweed(Point2D(x, y), instance)
                elif name == "Berries":
                    obj = Berries(Point2D(x, y), instance)
                elif name == "Fox":
                    obj = Fox(Point2D(x, y), instance)
                elif name == "Turtle":
                    obj = Turtle(Point2D(x, y), instance)

                if obj:
                    obj.increase_strength(int(strength) - obj.get_strength())
                    obj.increase_age(int(age))
                    instance.organisms.append(obj)

        cls.instance = instance
        return cls.instance

    def clear_logs(self):
        self.logs.clear()

    def initial_population(self):
        # self.human = Human(Point2D(5, 5), self)
        wolf = Wolf(Point2D(4, 7))
        self.add_organism(wolf)
        antelope = Antelope(Point2D(10, 10))
        self.add_organism(antelope)
        grass  = Grass(Point2D(2, 0))
        self.add_organism(grass)
        # Sheep(Point2D(19, 19), self)
        # Sheep(Point2D(16, 17), self)
        # Wolf(Point2D(6, 7), self)
        # Wolf(Point2D(5, 8), self)
        fox = Fox(Point2D(5, 7))
        self.add_organism(fox)
        dandelion = Dandelion(Point2D(3, 9))
        self.add_organism(dandelion)
        # Guarana(Point2D(6, 5), self)
        # Hogweed(Point2D(18, 17), self)
        # Berries(Point2D(10, 12), self)
        # Hogweed(Point2D(7, 7), self)
        # Turtle(Point2D(0, 3), self)

    def execute_turn(self):
        self.clear_logs()
        self.turn += 1
        self.organisms = [o for o in self.organisms if o.get_strength() >= 0]
        self._sort_organisms()
        size = len(self.organisms)
        for i in range(size):
            if self.organisms[i].get_strength() >= 0:
                self.organisms[i].action(self)

    def _sort_organisms(self):
        self.organisms.sort(key=lambda organism: organism.get_initiative(), reverse=True)

    def save_state(self, filename: str):
        with open(filename + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([self.turn, self.width, self.height])
            for o in self.organisms:
                if o.get_strength() > -1:
                    writer.writerow(
                        [o.__class__.__name__, o.position.get_x(), o.position.get_y(), o.get_strength(), o.get_age()])

    def load_state(self, filename: str):
        world = self.get_instance_from_file(filename + '.csv')
        self.turn = world.turn
        self.width = world.width
        self.height = world.height
        self.organisms = world.organisms
        self.logs = world.logs
        self.human = world.human

    def add_organism(self, organism):
        self.organisms.append(organism)

    def add_organism_by_name(self, name: str, position: Point2D):
        organism = Organism.spawn(self, position)
        if organism:
            self.organisms.append(organism)
            print(f" was born at [{organism.position.get_x()},{organism.position.get_y()}]")
            self.add_log(organism, f" was born at [{organism.position.get_x()},{organism.position.get_y()}]")

    def get_organism(self, position: Point2D):
        if not (0 <= position.get_x() < self.width and 0 <= position.get_y() < self.height):
            return None
        for organism in self.organisms:
            if organism.position.get_x() == position.get_x() and organism.position.get_y() == position.get_y():
                return organism
        return None

    def get_organisms(self) -> List[Organism]:
        return list(self.organisms)

    def get_human(self):
        return self.human

    def get_logs(self) -> List[str]:
        return list(self.logs)

    def add_log(self, source: Organism, log: str):
        name = source.__class__.__name__
        self.logs.append(f"{name}{log}")

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def is_in_bounds(self, position: Point2D):
        return 0 <= position.get_x() < self.width and 0 <= position.get_y() < self.height

    def reset_world(self):
        self.organisms.clear()
        self.logs.clear()
        self.human = None

    def is_position_within_bounds(self, position):
        return 0 <= position.get_x() < self.get_width() and 0 <= position.get_y() < self.get_height()

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            organism.kill()