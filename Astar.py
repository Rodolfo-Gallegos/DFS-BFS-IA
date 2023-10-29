import matplotlib.pyplot as plt
import numpy as np
import random

def initialize_grid(n):
    return np.zeros((n, n), dtype=int)

def is_valid(x, y, grid):
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

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def a_star(grid, start, goal):
    open_set = [start]
    came_from = {}
    g_score = {(cell[0], cell[1]): float('inf') for cell in np.ndindex(grid.shape)}
    g_score[start] = 0

    f_score = {(cell[0], cell[1]): float('inf') for cell in np.ndindex(grid.shape)}
    f_score[start] = manhattan_distance(start, goal)

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path

        open_set.remove(current)

        for neighbor in [(current[0], current[1] + 1), (current[0], current[1] - 1), (current[0] + 1, current[1]), (current[0] - 1, current[1])]:
            if is_valid(neighbor[0], neighbor[1], grid):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

    return None  # No se encontró un camino válido

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def draw_grid(grid, start, goal, path, visited):
    fig, ax = plt.subplots()

    ax.set_facecolor('white')
    cell_size = 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color='black'))
            elif grid[i][j] == 0:
                # Calcula el valor de calor en función de la distancia
                if goal:
                    distance = manhattan_distance((i, j), goal)
                    max_heat = max(len(grid), len(grid[0]))  # Máxima distancia posible en la cuadrícula
                    heat_value = 1 - (distance / max_heat)  # Ajusta el valor entre 0 (frío) y 1 (caliente)
                    color = plt.cm.viridis(heat_value)  # Utiliza el mapa de colores viridis de Matplotlib
                else:
                    color = 'white'

                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color=color))

    plt.scatter(start[1] * cell_size + cell_size / 2, start[0] * cell_size + cell_size / 2, color='white', marker='o',
                s=100)
    plt.scatter(goal[1] * cell_size + cell_size / 2, goal[0] * cell_size + cell_size / 2, color='red', marker='x',
                s=100)

    if path:
        path_x, path_y = zip(*path)
        path_x = [x * cell_size + cell_size / 2 for x in path_x]
        path_y = [y * cell_size + cell_size / 2 for y in path_y]
        plt.plot(path_y, path_x, color='white', label='Camino')

    if visited:
        visited_x, visited_y = zip(*visited)
        visited_x = [x * cell_size + cell_size / 2 for x in visited_x]
        visited_y = [y * cell_size + cell_size / 2 for y in visited_y]
        for i, (x, y) in enumerate(zip(visited_x, visited_y), 1):
            plt.text(y, x, str(i), ha='center', va='center', color='white', fontsize=14)

    for i in range(len(grid) + 1):
        plt.axhline(y=i * cell_size, color='black', linewidth=0.1)
    for j in range(len(grid[0]) + 1):
        plt.axvline(x=j * cell_size, color='black', linewidth=0.1)

    plt.legend()
    plt.show()


def main():
    n = 10
    grid = initialize_grid(n)
    num_obstacles = (n * n) // 4
    genera_obstaculos(grid, num_obstacles)

    try:
        start, goal = genera_start_goal(grid)
    except ValueError as e:
        print(e)
        return

    path = a_star(grid, start, goal)

    if path:
        print("Camino encontrado:", path)
    else:
        print("No se encontró un camino válido.")

    draw_grid(grid, start, goal, path, [])


if __name__ == "__main__":
    main()
