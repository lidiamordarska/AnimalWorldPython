import random
from point2d import Point2D
from zwierze import Zwierze

class Antylopa(Zwierze):
    ruchy = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, pozycja, swiat):
        super().__init__('A', 4, 4, pozycja, swiat)

    def akcja(self):
        self.age_up(1)
        move = random.randint(0, 3)
        while not self.set_position(Point2D(self.pozycja.get_x() + 2 * Antylopa.ruchy[move][0], self.pozycja.get_y() + 2 * Antylopa.ruchy[move][1]), False, False):
            move = (move + 1) % 4

    def czy_ucieczka(self):
        ucieczka = random.choice([True, False])
        if ucieczka:
            move = 0
            while not self.set_position(Point2D(self.pozycja.get_x() + Antylopa.ruchy[move][0], self.pozycja.get_y() + Antylopa.ruchy[move][1]), True, False):
                move += 1
                if move == 4:  # Poprawka z 8 na 4, bo tylko 4 ruchy są dostępne
                    self.world.dodaj_dziennik(self, " nie zdazyla uciec")
                    return False
            self.world.dodaj_dziennik(self, " uciekla!")
            return True
        return False

    def sklonuj(self, polozenie: Point2D):
        return Antylopa(polozenie, self.world)
