import pygame as py 
from random import randint as numero_aleatorio

py.init()

# Setup window display info
width, height = 900, 600
screen = py.display.set_mode((width, height))
py.display.set_caption("pedrito con una piedra en el culito")

# Load background image
image = py.image.load("P.JPG")

# Set pause
pause = False
font = py.font.Font (None, 36)
white = 255, 255,255

class Player(py.Vector2):
    def __init__(self):
        super().__init__(screen.get_width() / 2, screen.get_height() / 2)
        self.image_player = py.image.load("pedorro.PNG")
        self.image_player = py.transform.scale(self.image_player, (70, 70))
        self.player_react = self.image_player.get_rect(center=self)


class Bullet(py.Vector2):
    def __init__(self, pos_x, pos_y, data):
        super().__init__(pos_x, pos_y)
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.bullet_react = self.image.get_rect(center=self)

    def move_up(self, speed=5):
        self.y -= speed  # Move the bullet up by reducing y

    def get_character(self, data):
        if data == 1:
            return "bullet_1.png"
        if data == 2:
            return "bullet_2.png"


class PowerUp(py.Vector2):

    def __init__(self):
        super().__init__(numero_aleatorio(25, 825), -1)
        self.image = py.image.load("power_up.png")
        self.image = py.transform.scale(self.image, (80, 80))
        self.gem_react = self.image.get_rect(center=self)

    def move_down(self, speed=1):
        self.y += speed  # Move the bullet up by reducing y


def summon_power_up():
    power_up = PowerUp()
    return power_up


player = Player()
contador_bala = 0
list_of_bullets = []
list_of_power_ups = []
speed = 10
actual_ammo = 1

# Game loop
while True:
    # Event handling
    for evento in py.event.get():
        if evento.type == py.QUIT:
            py.quit()
            exit()

    # Increment the bullet counter
    contador_bala += 1

    # Draw background
    buttom = py.transform.scale(image, (900, 600))
    screen.blit(buttom, (0, 0))

    # Player movement
    keys = py.key.get_pressed()
    if keys [py.K_ESCAPE]:
        pause = not pause


    if not pause:
        if keys[py.K_RIGHT] or keys[py.K_d]:
            player.x += speed
        if keys[py.K_LEFT] or keys[py.K_a]:
            player.x -= speed
        if keys[py.K_UP] or keys[py.K_w]:
            player.y -= speed
        if keys[py.K_DOWN] or keys[py.K_s]:
            player.y += speed

    # Constrain player position within the screen boundaries
    player.x = max(player.player_react.width // 2, min(player.x, width - player.player_react.width // 2))
    player.y = max(player.player_react.width // 2, min(player.y, height - player.player_react.width // 2))

    # Update player's position
    player.player_react.center = (player.x, player.y)
    screen.blit(player.image_player, player.player_react)

    # Shooting bullets every 100 frames
    if contador_bala >= 20:
        contador_bala = 0
        # Create a new bullet starting at the player's current position
        list_of_bullets.append(Bullet(player.x, player.y, data=actual_ammo))

    # SPAWNEAR power up

    if numero_aleatorio(1, 100) == 10:
        list_of_power_ups.append(summon_power_up())

    # Update and draw each bullet
    for bullet in list_of_bullets[:]:  # Use a copy of the list to safely remove bullets
        bullet.move_up(speed=20)  # Move the bullet up
        bullet.bullet_react.center = (bullet.x, bullet.y)
        screen.blit(bullet.image, bullet.bullet_react)

        # Remove bullets that go off the top of the screen
        if bullet.y < 0:
            list_of_bullets.remove(bullet)

    for power in list_of_power_ups[:]:
        power.move_down(speed=10)
        power.gem_react.center = (power.x, power.y)
        screen.blit(power.image, power.gem_react)

        if power.gem_react.colliderect(player.player_react):
            print("colision detectada")
            actual_ammo = 2
            list_of_power_ups.remove(power)
    
    if pause:
        pause_text = font.render("STOP", True, white)
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

    # Update display and frame rate
    py.display.flip()
    py.time.Clock().tick(60)

