import pygame
import math
from the_game.car import ACarr
from the_game.photos import MY_CAR


class ComputerCarr(ACarr):
    IMG = MY_CAR
    START_POS = (425, 620)

    def __init__(self, max_vel, rotatiob_vel, path=None):
        super().__init__(max_vel, rotatiob_vel)
        if path is None:
            path = []
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