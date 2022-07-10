import pygame
import time
import math
from the_game.Game_Info import GameInfo
from the_game.utility import image_scale, blit_text_centre
from the_game.car import ACarr
from the_game.photos import FINISH_LINE, BOARDER, TRACK, MY_CAR, LOGO
from the_game.computer_car import ComputerCarr


def haida():
    pygame.font.init()

    FINISH_LINE_POSITION = (443, 575)
    FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)
    TRACK_BORDER_MASK = pygame.mask.from_surface(BOARDER)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Masinitili')

    PATH = [(326, 635), (187, 610), (98, 517), (129, 395), (216, 320), (337, 309), (479, 304), (546, 198), (585, 139),
            (715, 89), (854, 106), (954, 147), (985, 223), (969, 307), (911, 363), (794, 378), (719, 471), (698, 548),
            (640, 604), (547, 629), (443, 635)]

    MAIN_FONT = pygame.font.SysFont('comicsans', 44)

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    class PlayerCarr(ACarr):
        IMG = MY_CAR
        START_POS = (425, 590)

        def reduce_speed(self):
            self.vel = max(self.vel - self.acceleration / 2, 0)
            self.move()

        def bounce(self):
            self.vel = -self.vel
            self.move()

    def draw(win, image, player_ca, computer_ca, game_inf):
        for img, pos in image:
            win.blit(img, pos)

        level_text = MAIN_FONT.render(f'Level {game_inf.level}', True, (255, 255, 255))
        win.blit(level_text, (10, HEIGHT - level_text.get_height() - 80))

        time_text = MAIN_FONT.render(f'Time {game_inf.get_level_time()}s', True, (255, 255, 255))
        win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

        vel_text = MAIN_FONT.render(f'Vel {round(player_car1.vel, 1)}px/s', True, (255, 255, 255))
        win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 1))

        player_ca.draw(win)
        computer_ca.draw(win)
        pygame.display.update()

    def move_player(player_carr):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            player_carr.rotate(left=True)
        if keys[pygame.K_d]:
            player_carr.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            player_carr.move_forward()
        if keys[pygame.K_s]:
            moved = True
            player_carr.move_backward()
        if not moved:
            player_carr.reduce_speed()

    def handle_collision(player_carr, computer_carr, game_inf):
        if player_carr.collide(TRACK_BORDER_MASK) is not None:
            player_carr.bounce()

        computer_finish_poi_collide = computer_carr.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
        if computer_finish_poi_collide is not None:
            blit_text_centre(WIN, MAIN_FONT, 'You Lost.. :(', RED)
            pygame.display.update()
            pygame.time.wait(3000)
            game_inf.reset()
            player_carr.reset()
            computer_carr.reset()

        player_finish_poi_collide = player_carr.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
        if player_finish_poi_collide is not None:
            print(player_finish_poi_collide)
            if player_finish_poi_collide[0] == 34:
                player_carr.bounce()
            else:
                game_inf.next_level()
                player_carr.reset()
                computer_carr.next_level(game_inf.level)

    run = True
    fps = 60
    clock = pygame.time.Clock()
    images = [(TRACK, (0, 0)), (FINISH_LINE, FINISH_LINE_POSITION), (BOARDER, (0, 0))]
    player_car1 = PlayerCarr(3, 3)
    computer_car = ComputerCarr(2, 4, PATH)
    game_info = GameInfo()

    while run:
        clock.tick(fps)

        draw(WIN, images, player_car1, computer_car, game_info)

        while not game_info.started:
            blit_text_centre(WIN, MAIN_FONT, f'Press any key to start level {game_info.level}!', BLUE)
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

        move_player(player_car1)
        computer_car.move()

        handle_collision(player_car1, computer_car, game_info)

        if game_info.game_finsish():
            blit_text_centre(WIN, MAIN_FONT, 'You Won the Game', BLUE)
            pygame.time.wait(5000)
            game_info.reset()
            player_car1.reset()
            computer_car.reset()

    pygame.quit()


if __name__ == "__main__":
    haida()
