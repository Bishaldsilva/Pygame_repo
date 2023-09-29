import pygame

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
X,Y = [],[]
cors = set()
gameActive = False

def drawPoints():
    for i,j in zip(X,Y):
        pygame.draw.circle(screen,(255,255,255),(i,j),5)

def solve():
    min_x,min_y = -1,-1
    max_x,max_y = -1,-1
    min_dist = 10**9
    max_dist = 0
    for i ,j in zip(X,Y):
        if i + j < min_dist:
            min_dist = i + j
            min_x,min_y = i,j
        if i + j > max_dist:
            max_dist = i + j
            max_x,max_y = i,j

    return min_x,min_y,max_x,max_y

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(0)

    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        if (x,y) not in cors:
            X.append(x)
            Y.append(y)
            cors.add((x,y))
            print(x,y)

    if len(X) > 0:
        min_x,min_y,max_x,max_y = solve()
        pygame.draw.line(screen,(255,0,0),(0,0),(min_x,min_y))
        pygame.draw.line(screen,(0,255,255),(0,0),(max_x,max_y))
    drawPoints()

    pygame.display.update()
    clock.tick(60)