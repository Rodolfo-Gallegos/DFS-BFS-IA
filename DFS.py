import matplotlib.pyplot as plt
import numpy as np
import random

def initialize_grid(n):
    # Crea una cuadrícula NxN con todos los elementos inicializados a 0.
    return np.zeros((n, n), dtype=int)

def is_valid(x, y, grid):
    # Verifica si las coordenadas (x, y) están dentro de la cuadrícula y no son un obstáculo (valor 1).
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def genera_obstaculos(grid, n):
    for _ in range(n):
        x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)
        while grid[x][y] == 1:
            x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)
        grid[x][y] = 1

def genera_start_goal(grid):
    empty_cells = [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == 0]
    if len(empty_cells) < 2:
        raise ValueError("La cuadrícula no tiene suficientes celdas libres para establecer el inicio y la meta.")
    start, goal = random.sample(empty_cells, 2)
    return start, goal

def dfs(grid, start, goal):
    stack = [start]
    visited = set()
    visited_list = []  # Lista para almacenar los nodos visitados en orden

    parent = {}

    while stack:
        current = stack.pop()
        if current == goal:
            break

        x, y = current
        if current not in visited:
            visited.add(current)
            visited_list.append(current)

            # Define los movimientos posibles: izquierda, derecha, abajo, arriba.
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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

    # Devuelve tanto la lista de nodos visitados como el camino
    return visited_list, path[::-1]


def draw_grid(grid, start, goal, path, visited):
    fig, ax = plt.subplots()
    
    # Configura el fondo blanco
    ax.set_facecolor('white')
    
    # Tamaño de las celdas y espaciado de la cuadrícula
    cell_size = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:  # Obstáculo
                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color='black'))
            elif grid[i][j] == 0:  # Celda libre
                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color='white', edgecolor='black'))
    
    plt.scatter(start[1] * cell_size + cell_size / 2, start[0] * cell_size + cell_size / 2, color='orange', marker='o', s=100)
    plt.scatter(goal[1] * cell_size + cell_size / 2, goal[0] * cell_size + cell_size / 2, color='red', marker='x', s=100)
    
    if path:
        path_x, path_y = zip(*path)
        path_x = [x * cell_size + cell_size / 2 for x in path_x]
        path_y = [y * cell_size + cell_size / 2 for y in path_y]
        plt.plot(path_y, path_x, color='blue', label='Camino')
    
    if visited:
        visited_x, visited_y = zip(*visited)
        visited_x = [x * cell_size + cell_size / 2 for x in visited_x]
        visited_y = [y * cell_size + cell_size / 2 for y in visited_y]
        for i, (x, y) in enumerate(zip(visited_x, visited_y), 1):
            plt.text(y, x, str(i), ha='center', va='center', color='green', fontsize=14)
    
    # Dibuja la cuadrícula
    for i in range(len(grid) + 1):
        plt.axhline(y=i * cell_size, color='black', linewidth=0.1)
    for j in range(len(grid[0]) + 1):
        plt.axvline(x=j * cell_size, color='black', linewidth=0.1)
    
    plt.legend()
    plt.show()


def main():
    n = 10 # Tamaño de la cuadrícula (NxN)
    grid = initialize_grid(n)
    
    # Genera obstáculos aleatorios (N^2/4 obstáculos)
    num_obstacles = (n*n) // 4
    genera_obstaculos(grid, num_obstacles)
    
    try:
        start, goal = genera_start_goal(grid)
    except ValueError as e:
        print(e)
        return
    
    visited, path = dfs(grid, start, goal)
    if path:
        print("Camino encontrado:", path)
        print("Camino recorrido:", visited)
    else:
        print("No se encontró un camino válido.")
    
    draw_grid(grid, start, goal, path, visited)

if __name__ == "__main__":
    main()
