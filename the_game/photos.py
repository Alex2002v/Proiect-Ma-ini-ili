from the_game.utility import image_scale
import pygame

TRACK = image_scale(pygame.image.load('roads.jpg'), 4)
BOARDER = image_scale(pygame.image.load('boarder1.png'), 4)
FINISH_LINE = image_scale(pygame.image.load('finish.png'), 0.2)
MY_CAR = image_scale(pygame.image.load('mycar.png'), 0.2)
LOGO = pygame.image.load('logo.jpg')

