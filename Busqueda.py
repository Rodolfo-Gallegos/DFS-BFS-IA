import matplotlib.pyplot as plt
import numpy as np

def initialize_grid(n):
    # Crea una cuadrícula NxN con todos los elementos inicializados a 0.
    return np.zeros((n, n), dtype=int)

def is_valid(x, y, grid):
    # Verifica si las coordenadas (x, y) están dentro de la cuadrícula y no son un obstáculo (valor 1).
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def dfs(grid, start, goal):
    stack = [start]
    visited = set()
    parent = {}
    
    while stack:
        current = stack.pop()
        if current == goal:
            break
        
        x, y = current
        visited.add(current)
        
        # Define los movimientos posibles: arriba, abajo, izquierda y derecha.
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in moves:
            neighbor = (x + dx, y + dy)
            
            if is_valid(neighbor[0], neighbor[1], grid) and neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current
    
    # Reconstruye la trayectoria desde el objetivo hasta el inicio.
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    
    return path[::-1]

def draw_grid(grid, start, goal, path):
    plt.imshow(grid, cmap='gray')
    plt.scatter(*start[::-1], color='green', marker='o', s=100, label='Inicio')
    plt.scatter(*goal[::-1], color='red', marker='x', s=100, label='Meta')
    
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='blue', label='Camino')
    
    plt.legend()
    plt.show()

def main():
    n = 10  # Tamaño de la cuadrícula (NxN)
    grid = initialize_grid(n)
    
    start = (0, 0)  # Coordenadas de inicio
    goal = (9, 9)   # Coordenadas de la meta
    
    # Establece obstáculos en la cuadrícula (1 indica un obstáculo).
    grid[1][2] = grid[2][2] = grid[3][2] = grid[4][2] = 1
    grid[6][5] = grid[6][6] = grid[6][7] = 1
    
    path = dfs(grid, start, goal)
    print("Camino encontrado:", path)
    
    draw_grid(grid, start, goal, path)

if __name__ == "__main__":
    main()
