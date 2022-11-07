import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
circle(screen, (205, 205, 50), (200, 200), 160)
circle(screen, (255, 255, 0), (200, 200), 150)

rect(screen, (0, 0, 0), (140, 250, 120, 15))
rect(screen, (0, 0, 0), (175, 260, 55, 10))
pygame.draw.polygon(screen, (0,0,0), 
                    [[140, 150], [130, 150], 
                     [180, 130], [190, 130]])
pygame.draw.polygon(screen, (0,0,0), 
                    [[260, 150], [270, 150], 
                     [220, 130], [210, 130]])
circle(screen, (255, 255, 255), (240, 160), 15)
circle(screen, (255, 255, 255), (160, 160), 15)
circle(screen, (0, 0, 0), (240, 160), 10)
circle(screen, (0, 0, 0), (160, 160), 10)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()