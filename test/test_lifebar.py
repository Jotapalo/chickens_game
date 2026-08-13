import pygame as py
import os

PLAYER_SRC = os.path.join("src", "resources", "lifebar", "player_bar")
ENEMY_SRC = os.path.join("src", "resources", "lifebar", "enemy_bar")
EMPTY_SRC = os.path.join("src", "resources", "lifebar", "empty_bg")

py.init()
screen = py.display.set_mode((900, 600))
py.display.set_caption("LifeBar - test")
clock = py.time.Clock()
running = True

empty_l = py.image.load(EMPTY_SRC + "\\empty_l.png")
empty_m = py.image.load(EMPTY_SRC + "\\empty_m.png")
empty_r = py.image.load(EMPTY_SRC + "\\empty_r.png")

player_l = py.image.load(PLAYER_SRC + "\\player_l.png")
player_m = py.image.load(PLAYER_SRC + "\\player_m.png")
player_r = py.image.load(PLAYER_SRC + "\\player_r.png")

enemy_l = py.image.load(ENEMY_SRC + "\\enemy_l.png")
enemy_m = py.image.load(ENEMY_SRC + "\\enemy_m.png")
enemy_r = py.image.load(ENEMY_SRC + "\\enemy_r.png")

def load_life(max_life, actual_life, max_size_x, size_y, coo: tuple[int, int], bar_type:str) -> None:

    if actual_life > max_life:
        actual_life == max_life
    
    posx, posy = coo[0], coo[1]
    last_x = posx

    # BACKGROUND
    center_widht = max_size_x - empty_l.get_width()*2 # tamaño del centro en pixeles
    empty_center = py.transform.scale(empty_m, (center_widht, size_y))
    empty_left = py.transform.scale(empty_l, (empty_l.get_width(), size_y))
    empty_rigth = py.transform.scale(empty_r, (empty_r.get_width(), size_y))

    
    screen.blit(empty_left, (last_x, posy))
    last_x += empty_left.get_width()

    screen.blit(empty_center, (last_x, posy))
    last_x += empty_center.get_width()

    screen.blit(empty_rigth, (last_x, posy))

    last_x = posx

    # FOREGROUND
    if bar_type == "player":
        center_widht_player = (actual_life/max_life)*center_widht 
        player_left = py.transform.scale(player_l, (player_l.get_width(), size_y))
        player_right = py.transform.scale(player_r, (player_r.get_width(), size_y))
        player_center = py.transform.scale(player_m, (center_widht_player, size_y))

        screen.blit(player_left, (last_x, posy))
        last_x += player_left.get_width()

        screen.blit(player_center, (last_x, posy))
        last_x += player_center.get_width()

        screen.blit(player_right, (last_x, posy))
    else:
        center_widht_enemy = (actual_life/max_life)*center_widht 
        enemy_left = py.transform.scale(enemy_l, (enemy_l.get_width(), size_y))
        enemy_right = py.transform.scale(enemy_r, (enemy_r.get_width(), size_y))
        enemy_center = py.transform.scale(enemy_m, (center_widht_enemy, size_y))

        screen.blit(enemy_left, (last_x, posy))
        last_x += enemy_left.get_width()

        screen.blit(enemy_center, (last_x, posy))
        last_x += enemy_center.get_width()

        screen.blit(enemy_right, (last_x, posy))


max_life = 100
counter = max_life

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    # Init test
    screen.fill((255, 255, 255))

    counter -= 1

    load_life(max_life=max_life, 
                  actual_life=counter,
                  max_size_x=100,
                  size_y=20,
                  coo=(100, 100),
                  bar_type="player")

    load_life(max_life=max_life, 
                      actual_life=counter,
                      max_size_x=100,
                      size_y=20,
                      coo=(100, 200),
                      bar_type="enemy")

    if counter > 100:
        counter = 0
    if counter < 0:
        counter = 100

    py.display.flip()
    clock.tick(60)

py.quit()