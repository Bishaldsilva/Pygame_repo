from operator import truediv
import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.math import Vector2
from random import randint

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(6,10),Vector2(7,10)]
        self.direction = Vector2(-1,0)

    def draw(self):
        for body in self.body:
            x = int(body.x * CELL_SIZE)
            y = int(body.y * CELL_SIZE)
            pygame.draw.rect(screen,(255,255,255),(x+2,y+2,CELL_SIZE,CELL_SIZE))

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy

    def add_body(self):
        body_copy = self.body[:]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy
    
    def check_collision(self):
        if fruit.pos == self.body[0]:
            fruit.randomize()
            self.add_body()

    def update(self):
        self.move()
        self.check_collision()

class Fruit:
    def __init__(self):
        self.randomize()
    
    def randomize(self):
        self.pos = Vector2(randint(0,COLS - 1),randint(0, ROWS - 1))
    
    def draw(self):
        pygame.draw.rect(screen,(255,0,0),(int(self.pos.x) * CELL_SIZE,int(self.pos.y) * CELL_SIZE,CELL_SIZE,CELL_SIZE))
        

pygame.init()
ROWS = 20
COLS = 20
CELL_SIZE = 20
screen = pygame.display.set_mode((COLS * CELL_SIZE,ROWS * CELL_SIZE))
clock = pygame.time.Clock()

snake = Snake()
fruit = Fruit()

snake_movement_timer = pygame.USEREVENT + 1
pygame.time.set_timer(snake_movement_timer,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == snake_movement_timer:
            snake.update()

        if event.type == pygame.KEYDOWN:
            if event.key == K_UP and snake.direction.y != 1:
                snake.direction = Vector2(0,-1)
            if event.key == K_DOWN and snake.direction.y != -1:
                snake.direction = Vector2(0,1)
            if event.key == K_LEFT and snake.direction.x != 1:
                snake.direction = Vector2(-1,0)
            if event.key == K_RIGHT and snake.direction.x != -1:
                snake.direction = Vector2(1,0)

    screen.fill(0)
    snake.draw()
    fruit.draw()

    pygame.display.update()
    clock.tick(60)
