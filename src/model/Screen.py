import pygame as py

from src.model.Enum import Enum
from src.model.Planet import Planet

class Screen:
    def __init__(self, width, height):
        self.surface = py.display.set_mode((width, height), py.RESIZABLE)
        self.width = width
        self.height = height
        self.initializer()
        self.background_delta = 0.8
        self.PlanetList: list[Planet] = list()


    def initializer(self):
        py.display.set_caption("Chickens Game")
        # Cargar y pre-escalar el fondo una sola vez con smoothscale (nitidez)
        font_image = py.image.load(Enum.resourcePath.FONT_3).convert()
        self.font_image = py.transform.smoothscale(font_image, (1020, 600))
        self.bg_part_1 = 0
        self.bg_part_2 = 600

        self.pause = False
        self.pause_font = py.font.Font(Enum.resourcePath.DEFAULT_FONT, 36)
        self.pause_text = self.pause_font.render("Juego en Pausa", True, Enum.colorsMap.RED)

        self.game_over = False
        self.game_over_font = py.font.Font(Enum.resourcePath.DEFAULT_FONT, 45)
        self.game_over_font = self.game_over_font.render("GAME OVER", True, Enum.colorsMap.RED)

        self.win_font = py.font.Font(Enum.resourcePath.DEFAULT_FONT, 45)
        self.win_font = self.win_font.render("YOU WIN!", True, Enum.colorsMap.GREEN)

    def draw_background(self):
        self.surface.blit(self.font_image, (0, self.bg_part_1))
        self.surface.blit(py.transform.flip(self.font_image, 0, 1), (0, self.bg_part_2))
        self.bg_part_1 += self.background_delta
        self.bg_part_2 += self.background_delta

        if self.bg_part_1 >= 600:
            self.bg_part_1 = -600
        if self.bg_part_2 >= 600:
            self.bg_part_2 = -600

        for planet in self.PlanetList:
            planet.draw_and_move(self.surface)

    def pause_protocol(self):
         # Si el juego está en pausa, mostrar el mensaje de pausa
        self.surface.blit(self.pause_text,
                           (self.width // 2 - self.pause_text.get_width() // 2,
                             self.height // 2 - self.pause_text.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa

    def game_over_protocol(self):
        # Si el juego está en pausa, mostrar el mensaje de pausa
        self.surface.fill(Enum.colorsMap.WHITE)
        self.surface.blit(self.game_over_font,
                            (self.width // 2 - self.game_over_font.get_width() // 2,
                                self.height // 2 - self.game_over_font.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa

    def win_protocol(self):
            # Si el juego está en pausa, mostrar el mensaje de pausa
        self.surface.fill(Enum.colorsMap.WHITE)
        self.surface.blit(self.win_font,
                            (self.width // 2 - self.win_font.get_width() // 2,
                                self.height // 2 - self.win_font.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa

    def summon_planet(self, planet_string, posx, posy):
        planet = None
        match planet_string:
            case "planet_1":
                planet = Enum.Image.Planet_1
            case "planet_2":
                planet = Enum.Image.Planet_2
            case "saturn":
                planet = Enum.Image.Saturn
            case _:
                print("No se pudo cargar el planeta especificado")

        self.PlanetList.append(Planet(planet, posx, posy))
                
        
