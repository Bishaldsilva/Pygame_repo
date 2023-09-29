import pygame
from pygame.constants import K_SPACE, QUIT
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

gameActive = False
X = []
Y = []
cors = set()
b,m = 100,120
lr,epochs = 0.01,100

def scaling(x,y):
    l1,l2 = [],[]
    for i,j in zip(x,y):
        l1.append((i / 600) * 2 - 1)
        l2.append((j / 600) * 2 - 1)

    return np.array(l1),np.array(l2)

def upscale(n):
    return ((n + 1) / 2) * 600

def downscale(n):
    return (n / 600) * 2 - 1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameActive:
                X,Y = scaling(X,Y)
                # print(X,Y)
                gameActive = True

    if not gameActive:
        if pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            if (x,y) not in cors:
                X.append(x)
                Y.append(y)
                cors.add((x,y))
            pygame.draw.ellipse(screen,(255,255,255),(x-5,y-5,10,10))
    else:
        screen.fill(0)
        for i,j in zip(X,Y):
            pygame.draw.ellipse(screen,(255,255,255),(upscale(i)-5,upscale(j)-5,10,10))
    
        slope_b = -2 * np.sum(Y - m*X - b)
        slope_m = -2 * np.sum((Y - m*X - b)*X)

        b = b - lr * slope_b
        m = m - lr * slope_m

        # print(slope_b,slope_m,b,m)
        y_left = m * downscale(0) + b
        y_right = m * downscale(600) + b
        pygame.draw.line(screen,(255,0,0),(0,upscale(y_left)),(600,upscale(y_right)))

    # print(X,Y)

    pygame.display.update()
    clock.tick(60)