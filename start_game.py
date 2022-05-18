import pygame
import time
import math
from pygame.locals import *  # import all modules from Pygame
from the_game.utility import image_scale, blit_rot_center


TRACK = image_scale(pygame.image.load('roads.jpg'), 4)
MY_CAR = image_scale(pygame.image.load('mycar.png'), 0.2)
LOGO = pygame.image.load('logo.jpg')
BOARDER = image_scale(pygame.image.load('boarder.png'), 4)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Masinitili')


class ACar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.vel = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rot_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

class PlayerCar(ACar):
    IMG = MY_CAR
    START_POS = (512, 580)


def draw(win, image, player_ca):
    for img, pos in image:
        win.blit(img, pos)
    player_ca.draw(win)
    pygame.display.update()


run = True
FPS = 60
clock = pygame.time.Clock()
images = [(TRACK, (0, 0))]
player_car = PlayerCar(4, 4)


while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    WIN.blit(TRACK, (0, 0))
    WIN.blit(MY_CAR, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        player_car.move_forward()




pygame.quit()
