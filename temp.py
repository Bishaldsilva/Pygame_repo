import pygame
import sys

from pygame.math import Vector2

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

gravity = Vector2(0,0.5)
force = Vector2(1,-3)
mu = 0.05

class Particle:
    def __init__(self,x,y,mass) -> None:
        self.pos = Vector2(x,y)
        self.mass = mass
        self.radius = 20
        self.velocity = Vector2(0,0)

    def applyForce(self,force):
        self.velocity += force

    def friction(self):
        diff = 600 - self.pos.y - self.radius
        if diff < 1:
            direction = (self.velocity.x + 0.0000000000001) / abs(self.velocity.x + 0.0000000000001)
            print(self.velocity.x)
            normal = self.mass * gravity.y
            friction = Vector2(-direction * mu * normal,0)
            self.applyForce(friction)

    def edge(self):
        if self.pos.y + self.radius >= 600:
            self.pos.y = 600 - self.radius
            self.velocity.y *= -1

        if self.pos.x + self.radius >= 600:
            self.pos.x = 600 - self.radius
            self.velocity.x *= -1

        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.velocity.x *= -1

    def update(self):
        self.pos += self.velocity
        self.friction()
        self.edge()

    def draw(self):
        x_cor = self.pos.x
        y_cor = self.pos.y
        pygame.draw.circle(screen,(255,255,255),(x_cor,y_cor),self.radius)

particle = Particle(300,300,3)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(0)

    if pygame.mouse.get_pressed()[0]:
        particle.applyForce(force)

    particle.applyForce(particle.mass * gravity)
    particle.update()
    particle.draw()

    pygame.display.update()
    clock.tick(60)