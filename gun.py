import math
from random import choice, randint
import numpy as np
import pygame



FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

g = 1               #gravity force
q = 0.2             # energy loss


class Ball:
    def __init__(self, screen: pygame.Surface, x= 40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = gun.xx
        self.y = gun.yy
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (self.x >= WIDTH - self.r) and (self.vx > 0):
            self.vx = -self.vx*(1-q)
        if (self.y >= HEIGHT - self.r) and (self.vy < 0):
            self.vy = -self.vy*(1-q)
        self.vy -= g
        self.x += self.vx
        self.y -= self.vy 

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r+obj.r)**2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.xx = 40
        self.yy = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, (self.xx, self.yy), (self.xx+(self.f2_power+20)*np.cos(self.an), self.yy+(self.f2_power+20)*np.sin(self.an)), 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY

    def move(self, event):
        
        self.yy -= 10

class Target:
    def __init__(self) -> None:
        self.points = 0
        self.live = 1
        
        self.x = randint(600, 780)
        self.y = randint(100, 550)
        self.r = randint(2, 50)
        self.tvx = randint(1,5)
        self.tvy = randint(1, 5)

    def new_target(self):
        """ Инициализация новой цели. """        
        self.live = 10
        self.x = randint(300, 780)
        self.y = randint(100, 500)
        self.r = randint(30, 50)
        self.tvx = randint(-7, 7)
        self.tvy = randint(-7, 7)   

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
        self.x += self.tvx
        self.y -= self.tvy
        if (self.x >= WIDTH - self.r) and (self.tvx > 0):
            self.tvx = -self.tvx
        if (self.y >= HEIGHT - self.r) and (self.tvy < 0):
            self.tvy = -self.tvy
        if (self.y <= self.r) and (self.tvy > 0):
            self.tvy = -self.tvy
        if (self.x <= 200) and (self.tvx < 0):
            self.tvx = -self.tvx
        

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x,self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
target = Target()
target2= Target()

gun = Gun(screen)
ball = Ball(screen)
targets = []

for i in range(3):
    target = Target()
    targets.append(target) 
   
score = 0 
font = pygame.font.SysFont("ariel", 50)  
clock = pygame.time.Clock()


finished = False


while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            gun.move(event)
    for t in targets:
        t.move()    
       

    for b in balls:
        b.move()
        b.live =- 1
        for t in targets:
            if b.hittest(t) and t.live:
                t.hit()
                t.new_target()
                score += 1    
     
    gun.power_up()
    label = font.render(f"Your score: {score}", True, "BLACK")
    screen.blit(label, [50, 10])
    pygame.display.update()

pygame.quit()
