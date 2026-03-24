import csv
from typing import List
from point2d import Point2D
from organizm import Organizm
from czlowiek import Czlowiek
from trawa import Trawa
from guarana import Guarana
from owca import Owca
from barszcz import Barszcz
from mlecz import Mlecz
from jagody import Jagody
from antylopa import Antylopa
from lis import Lis
from zolw import Zolw
from wilk import Wilk
from cyber_owca import CyberOwca
class Swiat:
    instance = None

    def __init__(self, szerokosc: int, wysokosc: int):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.organizmy = []
        self.tura = 0
        self.czlowiek = None
        self.logi = []

    @classmethod
    def get_instance(cls, szerokosc: int = None, wysokosc: int = None):
        if cls.instance is None and szerokosc is not None and wysokosc is not None:
            cls.instance = cls(szerokosc, wysokosc)
        return cls.instance

    @classmethod
    def get_instance_from_file(cls, plik: str):
        instance = None
        with open(plik, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            first_line = next(reader)
            tura, szerokosc, wysokosc = map(int, first_line)
            instance = cls(szerokosc, wysokosc)
            instance.tura = tura

            for row in reader:
                if not row:
                    continue
                nazwa, x, y, sila, wiek, *rest = row
                x, y, sila, wiek = map(float, (x, y)) if '.' in x else map(int, (x, y, sila, wiek))
                obj = None
                if nazwa == "Czlowiek":
                    obj = Czlowiek(Point2D(x, y), instance)
                    instance.czlowiek = obj
                    umiejetnosc = int(rest[0])
                    instance.czlowiek.set_umiejetnosc(umiejetnosc)
                elif nazwa == "Antylopa":
                     obj = Antylopa(Point2D(x, y), instance)
                elif nazwa == "Trawa":
                    obj = Trawa(Point2D(x, y), instance)
                elif nazwa == "Owca":
                     obj = Owca(Point2D(x, y), instance)
                elif nazwa == "Wilk":
                     obj = Wilk(Point2D(x, y), instance)
                elif nazwa == "Mlecz":
                     obj = Mlecz(Point2D(x, y), instance)
                elif nazwa == "Guarana":
                    obj = Guarana(Point2D(x, y), instance)
                elif nazwa == "Barszcz":
                    obj = Barszcz(Point2D(x, y), instance)
                elif nazwa == "Jagody":
                    obj = Jagody(Point2D(x, y), instance)
                elif nazwa == "Lis":
                    obj = Lis(Point2D(x, y), instance)
                elif nazwa == "Zolw":
                    obj = Zolw(Point2D(x, y), instance)

                if obj:
                    obj.wzmocnij(int(sila) - obj.get_sila())
                    obj.postarz(int(wiek))
                    instance.organizmy.append(obj)

        cls.instance = instance
        return cls.instance

    def wyczysc_dziennik(self):
        self.logi.clear()

    def poczatkowa_populacja(self):
        #self.czlowiek = Czlowiek(Point2D(5, 5), self)
        Antylopa(Point2D(10, 10), self)
        Trawa(Point2D(2, 0), self)
        #Owca(Point2D(19, 19), self)
        #Owca(Point2D(16, 17), self)
        Wilk(Point2D(4, 7), self)
        #Wilk(Point2D(6, 7), self)
        #Wilk(Point2D(5, 8), self)
        Lis(Point2D(5, 7), self)
        Lis(Point2D(6, 7), self)
        Lis(Point2D(5, 8), self)
        Lis(Point2D(6, 8), self)
        Lis(Point2D(5, 9), self)
        Mlecz(Point2D(3, 9), self)
        #Guarana(Point2D(6, 5), self)
        #Barszcz(Point2D(18, 17), self)
        #Jagody(Point2D(10, 12), self)
        #Barszcz(Point2D(7, 7), self)
        #Zolw(Point2D(0, 3), self)

    def wykonaj_ture(self):
        self.wyczysc_dziennik()
        self.tura += 1
        self.organizmy = [o for o in self.organizmy if o.get_sila() >= 0]
        self._sort_organisms()
        size = len(self.organizmy)
        for i in range(size):
            if self.organizmy[i].get_sila() >= 0:
                self.organizmy[i].akcja()

    def _sort_organisms(self):
        self.organizmy.sort(key=lambda organizm: organizm.get_initiative(), reverse=True)

    def zapisz_stan(self, nazwa_pliku: str):
        with open(nazwa_pliku + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([self.tura, self.szerokosc, self.wysokosc])
            for o in self.organizmy:
                if o.get_sila() > -1:
                    writer.writerow([o.__class__.__name__, o.getpointX(), o.getpointY(), o.get_sila(), o.get_wiek()])

    def wczytaj_stan(self, nazwa_pliku: str):
        swiat = self.get_instance_from_file(nazwa_pliku + '.csv')
        self.tura = swiat.tura
        self.szerokosc = swiat.szerokosc
        self.wysokosc = swiat.wysokosc
        self.organizmy = swiat.organizmy
        self.logi = swiat.logi
        self.czlowiek = swiat.czlowiek

    def dodaj_organizm(self, organizm):
        self.organizmy.append(organizm)

    def dodaj_organizm_po_nazwie(self, name: str, position: Point2D):
        organizm = Organizm.spawn(self, position)
        if organizm:
            self.organizmy.append(organizm)
            print(f" narodzil sie na [{organizm.getpointX()},{organizm.getpointY()}]")
            self.dodaj_dziennik(organizm, f" narodzil sie na [{organizm.getpointX()},{organizm.getpointY()}]")

    def get_organizm(self, pozycja: Point2D):
        if not (0 <= pozycja.get_x() < self.szerokosc and 0 <= pozycja.get_y() < self.wysokosc):
            return None
        for organizm in self.organizmy:
            if organizm.pozycja.get_x() == pozycja.get_x() and organizm.pozycja.get_y() == pozycja.get_y():
                return organizm
        return None

    def get_organizmy(self) -> List[Organizm]:
        return list(self.organizmy)

    def get_czlowiek(self):
        return self.czlowiek

    def get_logi(self) -> List[str]:
        return list(self.logi)

    def dodaj_dziennik(self, zrodlo: Organizm, log: str):
        nazwa = zrodlo.__class__.__name__
        self.logi.append(f"{nazwa}{log}")

    def get_szerokosc(self):
        return self.szerokosc

    def get_wysokosc(self):
        return self.wysokosc

    def is_in_bounds(self, pozycja: Point2D):
        return 0 <= pozycja.get_x() < self.szerokosc and 0 <= pozycja.get_y() < self.wysokosc

    def resetuj_swiat(self):
        self.organizmy.clear()
        self.logi.clear()
        self.czlowiek = None

    def is_position_within_bounds(self, position):
        return 0 <= position.get_x() < self.get_szerokosc() and 0 <= position.get_y() < self.get_wysokosc()

    def remove_organism(self, organism):
        if organism in self.organizmy:
            self.organizmy.remove(organism)
            organism.zabij()


