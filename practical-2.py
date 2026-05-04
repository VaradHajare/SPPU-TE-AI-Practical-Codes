# Practical 2: A* for Maze Solving

import heapq
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def a_star_visual(grid, start, goal):
    h = lambda a,b: abs(a[0]-b[0]) + abs(a[1]-b[1])

    def path(curr):
        p = []
        while curr in parent:
            p.append(curr)
            curr = parent[curr]
        return [start] + p[::-1]

    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    open_list = [(0, start)]
    g, parent, closed = {start:0}, {}, set()

    cmap = ListedColormap(["white","black","#d3d3d3","#1f77b4","#ffcc00","#2ecc71","#e74c3c"])
    plt.figure()

    while open_list:
        _, curr = heapq.heappop(open_list)
        if curr in closed: continue
        closed.add(curr)

        p = path(curr)
        temp = np.array(grid)

        for x,y in closed: temp[x,y] = 2
        for x,y in p: temp[x,y] = 3
        temp[curr] = 4
        temp[start], temp[goal] = 5, 6

        plt.clf()
        plt.imshow(temp, cmap=cmap, vmin=0, vmax=6)
        plt.title("A* Algorithm for Maze Solving")
        plt.pause(0.5)

        if curr == goal:
            plt.show()
            return p

        for dx,dy in dirs:
            nb = (curr[0]+dx, curr[1]+dy)
            if (0 <= nb[0] < len(grid) and 0 <= nb[1] < len(grid[0]) and grid[nb[0]][nb[1]] == 0):
                ng = g[curr] + 1
                if nb not in g or ng < g[nb]:
                    g[nb] = ng
                    heapq.heappush(open_list, (ng + h(nb,goal), nb))
                    parent[nb] = curr

    return None


grid = [
    [0,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,1,0,1,0,0,1],
    [1,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,0,1,0,1,1],
    [1,0,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,0,1,1,1,0],
    [1,1,1,1,1,0,0,0,0,0]
]

start, goal = (0,0), (9,9)

res = a_star_visual(grid, start, goal)

print("Path:\n" + " -> ".join(map(str,res)) if res else "No path found")