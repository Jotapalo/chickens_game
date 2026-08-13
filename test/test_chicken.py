import pygame as py
import os

BASE_PATH = os.path.join("src", "resources", "img", "chicken")

py.init()
screen = py.display.set_mode((900, 600))
py.display.set_caption("Chicken - test")
clock = py.time.Clock()
running = True

chickens_face = py.image.load(BASE_PATH+"\\chicken-face.png")
chickens_wings = py.image.load(BASE_PATH+"\\chicken-wings.png")
posx_face = 36
posy_face = 0
posx_wings = 0
posy_wings = 0

def cortar_sprites(sheet, ancho, alto):
    sprites = []

    dentro_sprite = False
    inicio = 0

    for x in range(ancho):

        columna_vacia = True

        for y in range(alto):
            if sheet.get_at((x, y)).a != 0:
                columna_vacia = False
                break

        if not dentro_sprite and not columna_vacia:
            inicio = x
            dentro_sprite = True

        elif dentro_sprite and columna_vacia:
            rect = py.Rect(inicio, 0, x - inicio, alto)
            sprites.append(sheet.subsurface(rect))
            dentro_sprite = False

    # Último sprite
    if dentro_sprite:
        rect = py.Rect(inicio, 0, ancho - inicio, alto)
        sprites.append(sheet.subsurface(rect))

    return sprites

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    # Init test
    screen.fill((255, 255, 255))
    """
    if posx_face > 450:
        posx_face = 36

    if posx_wings > 1865:
        posx_wings = 0

    frame_face = chickens_face.subsurface(py.Rect(posx_face, posy_face, 32, 43))
    frame_wings = chickens_wings.subsurface(py.Rect(posx_wings, posy_wings, 128, 116))

    screen.blit(frame_wings, (50, 143))
    screen.blit(frame_face, (100, 100))

    posx_face += 32
    posx_wings += 128
    """
    print(cortar_sprites(chickens_wings, chickens_wings.get_width(), 112))
    for frame in cortar_sprites(chickens_wings, chickens_wings.get_width(), 112):
        screen.blit(frame, (100, 100))

    py.display.flip()
    clock.tick(60)

py.quit()