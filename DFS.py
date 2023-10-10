import matplotlib.pyplot as plt
import numpy as np
import random

def initialize_grid(n):
    # Crea una cuadrícula NxN con todos los elementos inicializados a 0.
    return np.zeros((n, n), dtype=int)

def is_valid(x, y, grid):
    # Verifica si las coordenadas (x, y) están dentro de la cuadrícula y no son un obstáculo (valor 1).
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def generate_obstacles(grid, n):
    for _ in range(n):
        x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)
        while grid[x][y] == 1:
            x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)
        grid[x][y] = 1

def generate_start_goal(grid):
    empty_cells = [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == 0]
    if len(empty_cells) < 2:
        raise ValueError("La cuadrícula no tiene suficientes celdas libres para establecer el inicio y la meta.")
    start, goal = random.sample(empty_cells, 2)
    return start, goal

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
        
        # Define los movimientos posibles: arriba, abajo, derecha, izquierda.
        moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        
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
        current = parent.get(current)  # Usamos .get() para evitar KeyError
        if current is None:
            break
    
    path.append(start)
    return path[::-1]

    # if current is not None:
    #     path.append(start)
    #     return path[::-1]
    # else:
    #     return []  # No se encontró una ruta válida

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
    
    # Genera obstáculos aleatorios (N/2 obstáculos)
    num_obstacles = n // 2
    generate_obstacles(grid, num_obstacles)
    
    try:
        start, goal = generate_start_goal(grid)
    except ValueError as e:
        print(e)
        return
    
    path = dfs(grid, start, goal)
    if path:
        print("Camino encontrado:", path)
    else:
        print("No se encontró un camino válido.")
    
    draw_grid(grid, start, goal, path)

if __name__ == "__main__":
    main()
