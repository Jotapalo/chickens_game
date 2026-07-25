import pygame as py

from src.enum import colorsMap
from src.enum import resEnum

class Screen:
    def __init__(self, width, height):
        self.surface = py.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.initializer()

    def initializer(self):
        py.display.set_caption("Chickens Game")
        self.font_image = py.image.load(resEnum.FONT)
        self.counter_bg_1 = 0
        self.counter_bg_2 = -600

        self.pause = False
        self.pause_font = py.font.Font(None, 36)
        self.pause_text = self.pause_font.render("Juego en Pausa", True, colorsMap.RED)

    def draw_background(self):
        self.surface.blit(py.transform.scale(self.font_image, (900, 600)), (0,self.counter_bg_1))
        self.surface.blit(py.transform.scale(self.font_image, (900, 600)), (0,self.counter_bg_2))
        self.counter_bg_1 += 0.5
        self.counter_bg_2 += 0.5

        if self.counter_bg_1 == 600:
            self.counter_bg_1 = -600
        if self.counter_bg_2 == 600:
            self.counter_bg_2 = -600

    def pause_protocol(self):
         # Si el juego está en pausa, mostrar el mensaje de pausa
        self.surface.fill(colorsMap.WHITE)
        self.surface.blit(self.pause_text,
                           (self.width // 2 - self.pause_text.get_width() // 2,
                             self.height // 2 - self.pause_text.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa
