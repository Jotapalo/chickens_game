import pygame as py

py.init()

width, height = 900, 600
screen = py.display.set_mode((width, height))
py.display.set_caption("pedrito con una piedra en el culito")

image = py.image.load("P.JPG")

player = py.Vector2(screen.get_width() / 2, screen.get_height() / 2)

image_player = py.image.load("pedorro.PNG")
image_player = py.transform.scale(image_player,(70,70))
player_rect = image_player.get_rect(center=player)

speed = 30

while True:
    for evento in py.event.get():
        if evento.type == py.QUIT:
            py.quit()
            exit()

    buttom = py.transform.scale(image, (900,600))
    screen.blit(buttom,(0,0))

    keys = py.key.get_pressed()
    if keys[py.K_RIGHT]:
        player.x += speed
    if keys[py.K_LEFT]:
        player.x -= speed
    if keys[py.K_UP]:
        player.y -= speed 
    if keys[py.K_DOWN]:
        player.y += speed

    player.x = max(player_rect.width // 2, min(player.x, width - player_rect.width // 2))
    player.y = max(player_rect.width// 2, min(player.y, height - player_rect.width // 2))

    player_rect.center = (player.x, player.y)

    screen.blit(image_player, player_rect)


    py.display.flip()
    py.time.Clock().tick(60)

