import pygame
import csv
import os
import random

pygame.font.init()
STAT_FONT = pygame.font.SysFont("arial", 30)

WIN_W = 1400
WIN_H = 900

xcells = 50
cell_size = WIN_W // xcells
ycells = WIN_H // cell_size

WIN_H = ycells * cell_size
CELL_VALS = False
border = 0
win = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Pathfinding")
win.fill((0,0,0))
load_file = "terrain.csv"

terrain = []
if os.path.exists(terrain_file):
    with open(terrain_file, mode="r") as file:
        reader = csv.reader(file)
        terrain = [row for row in reader]
        xcells = len(terrain[0])
        ycells = len(terrain)
        cell_size = WIN_H//ycells
        cell_size2 = WIN_W//xcells
        if cell_size > cell_size2:
            cell_size = cell_size2
else:
    terrain = [[str(int(not(bool(random.randint(0,2))))) if (x != 0 and x != xcells-1) else '1' for x in range(xcells)] if (y != 0 and y != ycells-1) else ['1']*xcells for y in range(ycells)]
    with open(terrain_file, mode="w") as file:
        writer = csv.writer(file)
        for row in terrain:
            writer.writerow(row)

#Cell format: [gcost, hcost, fcost, parent]
terrain_info = [[[None, None, None, []] for _ in range(xcells)] for _ in range(ycells)]


def draw_terrain(terrain, win):
    for y in range(len(terrain)):
        for x in range(len(terrain[0])):
            cell = pygame.Surface((cell_size-2*border, cell_size-2*border))
            if terrain[y][x] in ['0', 'o', 'c']:
                if terrain[y][x] == '0':
                    cell.fill((255,255,255))
                if terrain[y][x] == 'o':
                    cell.fill((0,255,0))
                if terrain[y][x] == 'c':
                    cell.fill(((255, 0, 0)))
                if terrain_info[y][x][2] != None and CELL_VALS:
                    gcost = STAT_FONT.render(str(terrain_info[y][x][0]), 1, (255,255,255))
                    hcost = STAT_FONT.render(str(terrain_info[y][x][1]), 1, (255,255,255))
                    fcost = STAT_FONT.render(str(terrain_info[y][x][2]), 1, (255,255,255))
                    cell.blit(gcost, (0,0))
                    cell.blit(hcost, (cell_size-hcost.get_width()-2*border,0))
                    cell.blit(fcost, (cell_size//2-fcost.get_width()//2, cell_size//2-fcost.get_height()//2))
            if terrain[y][x] == '1':
                cell.fill((0,0,0))
            if terrain[y][x] in ['s', 'f', 'p']:
                cell.fill((0,0,255))

            win.blit(cell, ((x*cell_size+border, y*cell_size+border)))

def update(terrain, win, points):
    for point in points:
        cell = pygame.Surface((cell_size-2*border, cell_size-2*border))
        if terrain[point[1]][point[0]] == '0':
            cell.fill((255,255,255))
        if terrain[point[1]][point[0]] == 'o':
            cell.fill((0,255,0))
        if terrain[point[1]][point[0]] == 'c':
            cell.fill(((255, 0, 0)))
        win.blit(cell, ((point[0]*cell_size+border, point[1]*cell_size+border)))

def distance(a, b):
    dx = abs(a[0]-b[0])
    dy = abs(a[1]-b[1])
    if dx >= dy:
        return dy * 14 + (dx-dy)*10
    return dx * 14 + (dy-dx)*10



start = [0,0]
end = [0,0]
for y in range(len(terrain)):
    for x in range(len(terrain[0])):
        if terrain[y][x] == 's':
            start = [x, y]
        if terrain[y][x] == 'f':
            end = [x, y]

def f_cost(point):
    return (distance(start, point) + distance(end, point))

def adj_nodes(node):
    x = node[0]
    y = node[1]
    adjs = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if not(dy == 0 and dx == 0):
                adjs.append([x+dx, y+dy])
    to_rem = []
    for adj in adjs:
        if terrain[adj[1]][adj[0]] == '1':
            to_rem.append(adj)
    for elt in to_rem:
        adjs.remove(elt)
    return adjs


open = [start]
closed = []
terrain_info[start[1]][start[0]] = [0, distance(start, end), distance(start, end)]
clock = pygame.time.Clock()
searching = True
draw_terrain(terrain, win)
while searching:
    open.sort(key=lambda x: terrain_info[x[1]][x[0]][2])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    current = open[0]
    open.remove(current)
    closed.append(current)
    terrain[current[1]][current[0]] = 'c'
    to_update = [current]
    if current == end:
        node = current
        while not(node == start):
            terrain[node[1]][node[0]] = 'p'
            node = terrain_info[node[1]][node[0]][3]
        terrain[start[1]][start[0]] = 'p'
        searching = False

    else:
        for neighbour in adj_nodes(current):
            if neighbour in closed:
                continue
            terrain[neighbour[1]][neighbour[0]] = 'o'
            gcost = terrain_info[current[1]][current[0]][0] + distance(current, neighbour)
            hcost = distance(neighbour, end)
            fcost = gcost+hcost
            if neighbour in open:
                oldgcost = terrain_info[neighbour[1]][neighbour[0]][0]
                if oldgcost < gcost:
                    continue
            terrain_info[neighbour[1]][neighbour[0]][0] = gcost
            terrain_info[neighbour[1]][neighbour[0]][1] = hcost
            terrain_info[neighbour[1]][neighbour[0]][2] = fcost
            terrain_info[neighbour[1]][neighbour[0]][3] = current

            if not(neighbour in open):
                to_update.append(neighbour)
                open.append(neighbour)


    update(terrain, win, to_update)
    pygame.display.update()

while True:
    draw_terrain(terrain, win)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
