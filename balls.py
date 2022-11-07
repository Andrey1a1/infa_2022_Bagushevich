import pygame as pg                 
from random import randint, random
import numpy as np


width = 1000
heigth = 700

pg.init()

balls_number = 10
FPS = 60
speed_loss = 0.03           #energy loss becouse of interaction with wall
g = 1000                     #gravity force acceleration
screen = pg.display.set_mode([width, heigth])


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
EDGE = (150, 150, 150)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    def __init__(self, coord, speed, rad, color, cost):
        '''
        Create a ball .
        '''
        self.coord = coord
        self.speed = speed
        self.rad = rad
        self.color = color
        self.cost = cost
    
    def move(self):   
        '''
        Makes the ball move.
        '''                                                                                                                                     
        self.coord = self.coord + self.speed * (1 / FPS)
    def caught(self, x, y):
        '''
        Returns whether the ball is caught.
        '''
        return (self.rad ** 2) >= ((self.coord[0] - x) ** 2 + (self.coord[1] - y) ** 2)                                                                       
    
    def wall_collide(self, wall_x, wall_y): 
        '''
        Creates wall reflections with a possibly inelastic impact.
        '''                                                                                                                
        if   (((self.coord[0] - self.rad) < wall_x[0]) and (self.speed[0] < 0)) or (((self.coord[0] + self.rad) > wall_x[1]) and (self.speed[0] > 0)):
            self.speed[0] = - self.speed[0] * np.sqrt(1 - speed_loss)
        elif (((self.coord[1] - self.rad) < wall_y[0]) and (self.speed[1] < 0)) or (((self.coord[1] + self.rad) > wall_y[1]) and (self.speed[1] > 0)):
            self.speed[1] = - self.speed[1] * np.sqrt(1 - speed_loss)
    

def new_ball(frequency, mincost, maxcost):
    '''
    Creates new ball, define frequency and cost of unusual balls.
    '''
    x = 100 + random() * 800
    y = 100 + random() * 500
    r = 10 + random() * 40
    v_x = -500 + random() * 1000
    v_y = -500 + random() * 1000
    color = COLORS[randint(0, 5)]
    if random() < frequency:
        cost = randint(mincost, maxcost)
    else:
        cost = 1
    ball = Ball(np.array([x, y]), np.array([v_x, v_y]), r, color, cost)
    return ball

def draw_ball(screen, ball):
    '''
    Draws new ball.
    '''
    pg.draw.circle(screen, ball.color, ball.coord, ball.rad)
    
font = pg.font.SysFont("ariel", 50)                       #Font of score

pg.display.update()
clock = pg.time.Clock()
finished = False
balls = []
score = 0

for i in range(balls_number):
    ball = new_ball(0, 1, 1)
    draw_ball(screen, ball)
    balls.append(ball)   


while not finished:
    clock.tick(FPS)     

    for event in pg.event.get():                                #body (click on balls to create new and delete old)
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            for i in range(len(balls)):
                if balls[i].caught(x, y) == True: 
                    score += balls[i].cost
                    balls[i] = new_ball(0.2, 3, 7)
        
    screen.fill((50,50,70)) 

    for i in range(len(balls)):
        balls[i].wall_collide([0, width], [0, heigth])
        if balls[i].cost > 1:
            balls[i].color = COLORS[randint(0, 5)]
            
        balls[i].move()
        draw_ball(screen, balls[i])
        balls[i].speed[1] += g * (1 / FPS)                                    # drawing and moving balls

    
    
    label = font.render(f"Your score: {score}", True, "YELLOW")
    screen.blit(label, [50, 10])
    
    pg.display.update()

           

pg.quit()