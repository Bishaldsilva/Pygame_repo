import pygame
from pygame.math import Vector2

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

gravity = Vector2(0,0.5)
wind = Vector2(1,0)
mu = 0.05

class Particle:
    def __init__(self,x,y,mass):
        self.pos = Vector2(x,y)
        self.radius = 30
        self.mass = mass
        self.velocity = Vector2(0,0)

    def applyForce(self,force):
        self.velocity += force

    def friction(self):
        diff = 600 - self.pos.y - self.radius

        if diff < 1:
            direction = (self.velocity.x + 0.000001) / abs(self.velocity.x + 0.000001)
            normal = self.mass * gravity.y
            friction = Vector2(-direction * mu * normal,0)
            self.applyForce(friction)

    def edges(self):
        if self.pos.y + self.radius >= 600:
            self.pos.y = 600 - self.radius
            self.velocity.y *= -1

        if self.pos.x + self.radius >= 600:
            self.pos.x = 600 - self.radius
            self.velocity.x *= -1
        
        if self.pos.x <= 0:
            self.pos.x = 0
            self.velocity.x *= -1

    def update(self):
        self.pos += self.velocity
        self.friction()
        self.edges()

    def draw(self):
        x_cor = self.pos.x
        y_cor = self.pos.y
        rect = pygame.Rect(x_cor,y_cor,self.radius,self.radius)
        pygame.draw.ellipse(screen,(255,255,255),rect)

particle = Particle(200,300,3)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(0)

    if(pygame.mouse.get_pressed()[0]):
        particle.applyForce(wind)

    particle.applyForce(gravity * particle.mass)
    particle.update()
    particle.draw()

    pygame.display.update()
    clock.tick(60)
