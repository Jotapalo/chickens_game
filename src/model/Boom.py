import pygame as py
from src.model.Enum import Enum


class Boom(py.sprite.Sprite):
    """Animación de explosión (spritesheet boom.png).

    Contiene la lógica de corte del spritesheet y el avance de frames.
    Los frames se cargan una sola vez como atributos de clase para
    reutilizarlos en todas las instancias (en lugar de recargarlos por
    cada explosión).

    El ciclo de vida se controla con el atributo `finished` (y no con
    alive()/kill()), porque estas explosiones no viven dentro de un
    grupo de pygame sino en una lista simple.
    """
    NUM_FRAMES = 6
    # Tamaño al que se redimensiona cada frame en pantalla
    frame_wh = 100
    _spritesheet_loaded = False
    _frames: list = []
    _frames_boss: list = []

    @classmethod
    def _load_frames(cls) -> None:
        """Carga y corta el spritesheet en los NUM_FRAMES frames (una sola vez).

        Usa el mismo muestreo de sprites que test_frame_boom.py:
        carga con convert_alpha() y recorta cada frame con subsurface(rect).
        """
        if cls._spritesheet_loaded:
            return

        spritesheet = py.image.load(Enum.resourcePath.BOOM).convert_alpha()

        # Rectángulos que delimitan cada frame dentro del spritesheet (x, y, w, h)
        FRAME_RECTS = [
            py.Rect(106,  442, 601-106,   972-442),
            py.Rect(660,  320, 1329-660,  1090-320),
            py.Rect(1419, 229, 2329-1419, 1170-229),
            py.Rect(2340, 180, 3360-2340, 1230-180),
            py.Rect(3439, 180, 4509-3439, 1230-180),
            py.Rect(4570, 230, 5568-4570, 1210-230),
        ]

        cls._frames = []

        for rect in FRAME_RECTS:
            frame = spritesheet.subsurface(rect)
            frame = py.transform.scale(frame, (cls.frame_wh, cls.frame_wh))
            frame_boss = py.transform.scale(frame, (200, 200))
            frame = frame.convert_alpha()
            frame_boss = frame_boss.convert_alpha()
            cls._frames.append(frame)
            cls._frames_boss.append(frame)

        cls._spritesheet_loaded = True

    def __init__(self, screen, posx, posy, frame_duration: int = 8, isBoss:bool = False):
        super().__init__()
        self.__class__._load_frames()

        self.screen = screen
        self.frame_index = 0
        # Cada cuántas llamadas a update() se avanza un frame (velocidad de la animación)
        self.frame_duration = max(1, frame_duration)
        self._frame_counter = 0
        self.finished = False
        self.isBoss = isBoss
        if isBoss:
            self.image = self.__class__._frames_boss[0]
        else:
            self.image = self.__class__._frames[0]

        self.rect = self.image.get_rect(center=(int(posx), int(posy)))

    def update(self) -> None:
        """Avanza la animación. Al terminar los frames, marca la explosión como terminada."""
        if self.finished:
            return

        self._frame_counter += 1
        if self._frame_counter >= self.frame_duration:
            self._frame_counter = 0
            self.frame_index += 1

            if self.frame_index >= self.__class__.NUM_FRAMES:
                self.finished = True
            else:
                if self.isBoss:
                    self.image = self.__class__._frames_boss[self.frame_index]
                else:
                    self.image = self.__class__._frames[self.frame_index]

    def draw(self) -> None:
        self.update()
        if not self.finished:
            self.screen.blit(self.image, self.rect)
