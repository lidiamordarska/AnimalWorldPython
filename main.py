import pygame
from pygame.locals import *
from swiat import Swiat
from czlowiek import Czlowiek
from point2d import Point2D


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1060, 700
        self.grid_size = 20
        self.cell_size = 32
        self.buttons = []
        self.swiat = None
        self.player = None

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Wirtualny Świat, Lidia Mordarska 197859")
        self.font = pygame.font.SysFont("Arial", 20)
        self._running = True

        # Initialize buttons
        self.buttons = [
            {"label": "Wykonaj Turę", "rect": pygame.Rect(900, 50, 150, 50), "action": self.wykonaj_ture},
            {"label": "Zapisz Stan", "rect": pygame.Rect(900, 120, 150, 50), "action": self.zapisz_stan},
            {"label": "Wczytaj Stan", "rect": pygame.Rect(900, 190, 150, 50), "action": self.wczytaj_stan},
            {"label": "Aktywuj Moc", "rect": pygame.Rect(900, 260, 150, 50), "action": self.aktywuj_moc},
        ]

        self.swiat = Swiat.get_instance(self.grid_size, self.grid_size)
        self.swiat.poczatkowa_populacja()

        self.player = Czlowiek(Point2D(5, 5), self.swiat)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["action"]()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.set_direction(Point2D(0, -1))
            elif event.key == pygame.K_DOWN:
                self.player.set_direction(Point2D(0, 1))
            elif event.key == pygame.K_LEFT:
                self.player.set_direction(Point2D(-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.player.set_direction(Point2D(1, 0))

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(15 + x * self.cell_size, 15 + y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self._display_surf, (255, 255, 255), rect, 1)

        for organizm in self.swiat.get_organizmy():
            if (organizm.pozycja.get_x() > -1 and organizm.pozycja.get_y() > -1):
                rect = pygame.Rect(15 + int(organizm.pozycja.get_x()) * self.cell_size,
                                   15 + int(organizm.pozycja.get_y()) * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self._display_surf, (255, 0, 0), rect)

                ikona = organizm.get_icon()
                font = pygame.font.Font(None, 36)
                text_surface = font.render(ikona, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                self._display_surf.blit(text_surface, text_rect)

        for button in self.buttons:
            pygame.draw.rect(self._display_surf, (100, 100, 100), button["rect"])
            text_surface = self.font.render(button["label"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self._display_surf.blit(text_surface, text_rect)



        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def wykonaj_ture(self):
        self.swiat.wykonaj_ture()
        self.on_render()

    def zapisz_stan(self):
        self.swiat.zapisz_stan("stan_swiata")

    def wczytaj_stan(self):
        self.swiat.wczytaj_stan("stan_swiata")

    def aktywuj_moc(self):
        self.player.activate_ability()
        self.on_render()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
