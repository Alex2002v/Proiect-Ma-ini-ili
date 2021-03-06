import pygame


def image_scale(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rot_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_centre(win, font, text, colour):
    render = font.render(text, 1, (200, 200, 200), colour)
    win.blit(render, (win.get_width() / 2 - render.get_width() / 2, win.get_width() /
                      2 - render.get_height() / 2))
