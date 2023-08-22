import pygame
from game import *

width = 1600
height = 800
pygame.init()  # запустить программу pygame
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Грабитель")
clock = pygame.time.Clock()  # для того чтобы отрабатывать кол-во fps в секунду
fps =100
screen.fill((255, 255, 255))
save = 0 #номер уровня

next_level = Level_three(screen, width, height,save)

while True:
    if next_level.check_event_loop():
        save += 1
        if save ==  1:
            next_level = Level_two(screen, width, height,save)
        if save == 2:
            next_level = Level_three(screen, width, height,save)
    next_level.update_action()
    next_level.show()
    clock.tick(fps)
    pygame.display.flip()  # все делаем в перевернутом экране
