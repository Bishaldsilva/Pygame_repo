import pygame
import math
import random

pygame.init()
rows = 60
cols = 60
size = 10
screen = pygame.display.set_mode((cols * size,rows*size))
pygame.display.set_caption("Rat in the Maze")
clock = pygame.time.Clock()

class Node:
    def __init__(self,row,col) -> None:
        self.row = row
        self.col = col
        self.center = (col * size + size /2,row * size + size/2)
        self.f = self.h = 0
        self.g = 10**9
        self.previous = None
        self.neighbors = []
        self.wall = False
        if random.random() < 0.3:
            self.wall = True

    def get_h(self,end):
        xd = end.row - self.row
        yd = end.col - self.col
        # d = (xd +yd) +(math.sqrt(2) -2)*min(xd,yd )
        d = math.sqrt(xd**2 + yd**2)
        self.h = d

    def get_neighbors(self,graph):
        row = self.row
        col = self.col

        if row > 0:
            self.neighbors.append(graph[row-1][col])

        if row < rows - 1:
            self.neighbors.append(graph[row+1][col])

        if col > 0:
            self.neighbors.append(graph[row][col - 1])

        if col < cols - 1:
            self.neighbors.append(graph[row][col + 1])

        if row > 0 and col > 0:
            self.neighbors.append(graph[row-1][col-1])
        if row < rows - 1 and col > 0:
            self.neighbors.append(graph[row+1][col-1])
        if row > 0 and col < cols -1:
            self.neighbors.append(graph[row-1][col+1])
        if row < rows - 1 and col < cols - 1:
            self.neighbors.append(graph[row+1][col+ 1])

def get_path(current):
    path = [current]
    while current.previous != None:
        current = current.previous
        path.insert(0,current)

    return path

def min_f(nodes):
    curr_node = nodes[0]
    for i in nodes:
        if i.f < curr_node.f:
            curr_node = i
    
    return curr_node

def draw(path):
    for i in range(len(path)-1):
    # for i in path:
        # pygame.draw.rect(screen,(255,0,0),(i.col * size,i.row * size,size,size))
        pygame.draw.line(screen,(255,0,0),path[i].center,path[i+1].center,3)

graph = [[Node(i,j) for j in range(cols)] for i in range(rows)]
graph[0][0].g = 0
end = graph[rows - 1][cols-1]
graph[0][0].wall = False
graph[rows-1][cols-1].wall = False

def draw_maze():
    for i in range(rows):
        for j in range(cols):
            if graph[i][j].wall:
                # pygame.draw.rect(screen,(0,0,0),(j * size,i * size,size,size))
                pygame.draw.circle(screen,(0,0,0),graph[i][j].center,4)

for i in range(rows):
    for j in range(cols):
        graph[i][j].get_neighbors(graph)
        graph[i][j].get_h(end)

openSet = [graph[0][0]]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255,255,255))
    if openSet != []:
        current = min_f(openSet)
        if(current == end):
            print("In the end...")
            openSet = []
        else:
            openSet.remove(current)
            for n in current.neighbors:
                if not n.wall:
                    tempg = current.g + 1
                    if tempg < n.g:
                        n.g = tempg
                        n.previous = current
                        n.f = n.g + n.h
                        if n not in openSet:
                            openSet.append(n)

        curr_path = get_path(current)

    if openSet == [] and current != end:
        print("solution not possible...")

    draw_maze()
    draw(curr_path)

    pygame.display.update()
    clock.tick(10)
