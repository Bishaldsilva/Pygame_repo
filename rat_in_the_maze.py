import pygame
from pygame import draw
from pygame.version import ver

pygame.init()
rows = 20
cols = 20
size = 30
screen = pygame.display.set_mode((cols * size, rows * size + 100))
clock = pygame.time.Clock()

walls = []
gameActive = False
maze = [[0 for _ in range(cols)] for _ in range(rows)]
visited = [[0 for i in range(cols)] for j in range(rows)]
ans = []
path = ""
ind = 0
rat_x = 0
rat_y = 0

def drawRat():
    global rat_x,rat_y,ind
    if path[ind] == "U":
        rat_x -= 1
    elif path[ind] == "D":
        rat_x += 1
    elif path[ind] == "L":
        rat_y -=1
    else:
        rat_y += 1
    ind += 1

def issafe(newx,newy,visited,rows,cols):
    return (newx >= 0 and newx < rows) and (newy >=0 and newy < cols) and maze[newx][newy] == 0 and visited[newx][newy] == 0

def solve(x,y,visited,path,rows,cols):
    global ans
    # print(x,y)
    if x == rows - 1 and y == cols - 1:
        ans.append(path)
        return True

    if issafe(x,y,visited,rows,cols):
        visited[x][y] = 1
        if solve(x + 1,y,visited,path+"D",rows,cols):
            return True
        if solve(x,y + 1,visited,path+"R",rows,cols):
            return True
        if solve(x - 1,y,visited,path+"U",rows,cols):
            return True
        if solve(x,y - 1,visited,path+"L",rows,cols):
            return True
        visited[x][y] = 0
        return False
    
    return False

class RM:
    def __init__(self):
        self.maze = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visited = [[0 for _ in range(cols)] for _ in range(rows)]
        self.ans = []

    def issafe(self,newx,newy):
        return (newx >= 0 and newx < rows) and (newy >=0 and newy < cols) and self.maze[newx][newy] == 0 and visited[newx][newy] == 0

    def solve(self,x,y,path):
        print(x,y)
        if x == cols - 1 and y == rows - 1:
            self.ans.append(path)
            return True

        if self.maze[x][y] == 1:
            return False

        visited[x][y] = 1
        # up
        if self.issafe(x - 1,y):
            self.solve(x - 1,y,path + "U")
        # down
        if self.issafe(x + 1,y):
            self.solve(x + 1,y,path + "D")
        # left
        if self.issafe(x,y - 1):
            self.solve(x,y - 1,path + "L")
        # right
        if self.issafe(x,y + 1):
            self.solve(x,y + 1,path + "R")

        visited[x][y] = 0

rm = RM()

rat_movement = pygame.USEREVENT + 1
pygame.time.set_timer(rat_movement,500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive == False:
                print(maze)
                solve(0,0,visited,"",rows,cols)
                path = min(ans)
                print(ans)
                gameActive=True

        if event.type == rat_movement and gameActive:
            if ind < len(path):
                drawRat()

    pygame.draw.rect(screen,(0,255,255),(0,0,cols * size,rows * size))


    if not gameActive:
        if pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            x = x // size
            y = y // size
            if [x,y] not in walls:
                maze[y][x] = 1
                walls.append([x,y]) 
    else:
        pygame.draw.rect(screen,(255,0,0),(rat_y * size,rat_x * size,size,size))

    for i in walls:
        pygame.draw.rect(screen,(0,0,0),(i[0] * size, i[1] * size,size,size))

    pygame.display.update()
    clock.tick(60)
