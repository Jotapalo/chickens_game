import pygame as py

py.init()

screen = py.display.set_mode((900, 600))
clock = py.time.Clock()
pl = 0

image = py.image.load("P.JPG")

player = py.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while True:
    for evento in py.event.get():
        if evento.type == py.QUIT:
            py.quit()
            exit()

    buttom = py.transform.scale(image, (900,600))
    screen.blit(buttom,(0,0))

    py.draw.circle(screen, "red", player, 30)

    keys = py.key.get_pressed()
    if keys[py.K_RIGHT]:
        player.x += 30
    if keys[py.K_LEFT]:
        player.x -= 30
    if keys[py.K_UP]:
        player.y -= 30
    if keys[py.K_DOWN]:
        player.y += 30

    py.display.flip()
    py.time.Clock().tick(60)
