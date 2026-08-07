import random
import pygame as py
from src.model.Enemy import Enemy
from src.model.Enum import Enum

class RoastedChicken(py.sprite.Sprite):
    def __init__(self, enemy: Enemy):
        super().__init__()
        self.screen = enemy.screen  # Surface de pygame
        self.image = Enum.Image.RoastedChicken
        self.rect = self.image.get_rect(center=(enemy.x, enemy.y))

        # Trayectoria parabólica (con parámetros aleatorios por instancia)
        self.origin_x = enemy.x   # x original (inicio de la parábola = 0)
        self.origin_y = enemy.y   # y original
        self.progress = 0.0       # avance horizontal acumulado (x desplazada)

        # --- Aleatoriedad ---
        # Dirección horizontal: 1 -> derecha, -1 -> izquierda
        self.direction = random.choice([-1, 1])
        # Altura máxima (coeficiente a): más alto o más bajo
        a = random.uniform(0.2, 0.5)
        # Alcance horizontal (coeficiente b): se va más lejos o menos en x
        b = random.uniform(6, 14)
        # Tiempo de vida (hasta dónde recorre la parábola), proporcional a b
        self.lifetime = random.randint(15, 25)
        self.a = a
        self.b = b

    def parabola_offset(self, x: float) -> float:
        """Devuelve el desplazamiento vertical (y) de una parábola que parte
        desde el origen (x=0), sube un poco y luego baja.

        Fórmula:  y = -a·x² + b·x
          - Raíz en x=0 y en x=(b/a)
          - Vértice (punto más alto) en x = b/(2a)
        """
        return -self.a * (x ** 2) + self.b * x

    def update(self) -> None:
        """Avanza el pollo asado por la parábola. Cada llamada incrementa el
        avance horizontal y reposiciona el rect según la función algebraica."""
        self.progress += 1.0
        offset_y = self.parabola_offset(self.progress)
        # Aplicar dirección (derecha o izquierda) al avance horizontal
        self.rect.centerx = self.origin_x + self.direction * self.progress
        self.rect.centery = self.origin_y - offset_y  # - para que suba hacia arriba
        if self.progress >= self.lifetime:
            self.kill()

    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)
