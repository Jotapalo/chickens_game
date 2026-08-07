"""
test.py
=====================================================================
Script autocontenido para reproducir la animación de un spritesheet
de explosión (boom.png) SIN depender de la clase Boom ni del juego.

Construye TODO lo necesario dentro de este archivo:
  1. Carga el spritesheet.
  2. Recorta cada frame usando los rectángulos de `FRAME_RECTS`.
  3. Escala cada frame a un tamaño jugable.
  4. Reproduce la animación en un bucle con pygame.

Uso (desde la raíz del proyecto):
    python test/test_frame_boom.py
"""

import os 

import pygame as py

# La imagen del spritesheet (ajusta la ruta si hace falta)
SPRITESHEET_PATH = os.path.join("src", "resources", "boom.png")

# Tamaño al que se redimensiona cada frame en pantalla
FRAME_WH = 160

# Velocidad: cuántos frames de juego dura cada fotograma de la animación
FRAME_DURATION = 6

# Colores
GRAY = (40, 40, 40)


# Rectángulos que delimitan cada frame dentro del spritesheet (x, y, w, h)
FRAME_RECTS = [
    py.Rect(106,  442, 601-106,   972-442), 
    py.Rect(660,  320, 1329-660,  1090-320),
    py.Rect(1419, 229, 2329-1419, 1170-229),
    py.Rect(2340, 180, 3360-2340, 1230-180),
    py.Rect(3439, 180, 4509-3439, 1230-180),
    py.Rect(4570, 230, 5568-4570, 1210-230),
]


def cut_spritesheet(image):
    """Devuelve la lista de superficies (frames) recortadas del spritesheet.

    Cada frame se recorta usando el rectángulo correspondiente de
    `FRAME_RECTS`, que delimita la posición y el tamaño real de cada
    fotograma dentro del spritesheet.
    """
    frames = []
    for rect in FRAME_RECTS:
        frame = image.subsurface(rect)
        frame = frame.convert_alpha()
        frames.append(frame)
    return frames


def main():
    py.init()
    screen = py.display.set_mode((900, 600))
    py.display.set_caption("Spritesheet boom - test")
    clock = py.time.Clock()

    # 1) Cargar el spritesheet
    sheet = py.image.load(SPRITESHEET_PATH).convert_alpha()

    # 2) Recortar los frames usando los rectángulos de FRAME_RECTS
    frames = cut_spritesheet(sheet)
    print(f"Frames detectados: {len(frames)}")

    # 3) Escalar cada frame a un tamaño uniforme y centrarlo
    scaled_frames = []
    for f in frames:
        scaled = py.transform.scale(f, (100, 100))
        scaled_frames.append(scaled)

    # 4) Reproducir la animación
    frame_index = 0
    frame_counter = 0
    running = True

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        frame_counter += 1
        if frame_counter >= FRAME_DURATION:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(scaled_frames)

        # Dibujar
        screen.fill(GRAY)
        pos = ((900 - FRAME_WH) // 2, (600 - FRAME_WH) // 2)
        screen.blit(scaled_frames[frame_index], pos)
        py.display.flip()
        clock.tick(60)

    py.quit()


if __name__ == "__main__":
    main()
