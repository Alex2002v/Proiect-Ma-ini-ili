import pygame
import time
import math
from pygame.locals import *  # import all modules from Pygame
from the_game.utility import image_scale, blit_rot_center, blit_text_centre
pygame.font.init()

TRACK = image_scale(pygame.image.load('roads.jpg'), 4)
BOARDER = image_scale(pygame.image.load('boarder1.png'), 4)
FINISH_LINE = image_scale(pygame.image.load('finish.png'), 0.2)
FINISH_LINE_POSITION = (443, 575)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)
TRACK_BORDER_MASK = pygame.mask.from_surface(BOARDER)
MY_CAR = image_scale(pygame.image.load('mycar.png'), 0.2)
LOGO = pygame.image.load('logo.jpg')

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Masinitili')
PATH = [(326, 635), (187, 610), (98, 517), (129, 395), (216, 320), (337, 309), (479, 304), (546, 198),(585, 139), (715, 89), (854, 106), (954, 147), (985, 223), (969, 307), (911, 363), (794, 378), (719, 471), (698, 548), (640, 604), (547, 629), (443, 635)]

MAIN_FONT = pygame.font.SysFont('comicsans', 44)


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level = 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finsish(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time )


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

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0


class PlayerCar(ACar):
    IMG = MY_CAR
    START_POS = (425, 590)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(ACar):
    IMG = MY_CAR
    START_POS = (425, 620)

    def __init__(self, max_vel, rotatiob_vel, path=[]):
        super().__init__(max_vel, rotatiob_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_deff = target_x - self.x
        y_deff = target_y - self.y

        if y_deff == 0:
            desired_radius_angle = math.pi / 2
        else:
            desired_radius_angle = math.atan(x_deff / y_deff)

        if target_y > self.y:
            desired_radius_angle += math.pi

        differences_in_angle = self.angle - math.degrees(desired_radius_angle)
        if differences_in_angle >= 180:
            differences_in_angle -= 360

        if differences_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(differences_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(differences_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


def draw(win, image, player_ca, computer_ca, game_info):
    for img, pos in image:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f'Level {game_info.level}', 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f'Time {game_info.get_level_time()}s', 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(f'Vel {round(player_car.vel, 1)}px/s', 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_ca.draw(win)
    computer_ca.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
    if computer_finish_poi_collide is not None:
        blit_text_centre(WIN, MAIN_FONT, 'You Lost')
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
    if player_finish_poi_collide is not None:
        print(player_finish_poi_collide)
        if player_finish_poi_collide[0] == 34:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level((game_info.level))


run = True
FPS = 60
clock = pygame.time.Clock()
images = [(TRACK, (0, 0)), (FINISH_LINE, FINISH_LINE_POSITION), (BOARDER, (0, 0))]
player_car = PlayerCar(3, 3)
computer_car = ComputerCar(3, 4, PATH)
game_info = GameInfo()


while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car, game_info)

    while not game_info.started:
        blit_text_centre(WIN, MAIN_FONT, f'Press any key to start level {game_info.level}!')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    WIN.blit(TRACK, (0, 0))
    WIN.blit(MY_CAR, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finsish():
        blit_text_centre(WIN, MAIN_FONT, 'You Won the Game')
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

print(computer_car.path)
pygame.quit()
