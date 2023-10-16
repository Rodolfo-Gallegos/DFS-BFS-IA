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

def hill_climbing(grid, start, goal, max_iterations):
    current = start
    visited = set()
    visited_list = []
    path = []
    iterations = 0

    while current != goal and iterations < max_iterations:
        visited.add(current)
        visited_list.append(current)
        path.append(current)
        x, y = current

        moves = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        moves.sort(key=lambda move: manhattan_distance(move, goal))

        for move in moves:
            if is_valid(move[0], move[1], grid) and move not in visited:
                current = move
                break

        iterations += 1

    if iterations >= max_iterations:
        print("El algoritmo se atascó después de", max_iterations, "iteraciones.")

    if current == goal:
        path.append(goal)  # Agregar la posición del objetivo si no se alcanza

    return path, visited_list

def draw_grid(grid, start, goal, path, visited):
    fig, ax = plt.subplots()

    ax.set_facecolor('white')
    cell_size = 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color='black'))
            elif grid[i][j] == 0:
                ax.add_patch(plt.Rectangle((j * cell_size, i * cell_size), cell_size, cell_size, color='white',
                                          edgecolor='black'))

    plt.scatter(start[1] * cell_size + cell_size / 2, start[0] * cell_size + cell_size / 2, color='orange', marker='o',
                s=100)
    plt.scatter(goal[1] * cell_size + cell_size / 2, goal[0] * cell_size + cell_size / 2, color='red', marker='x',
                s=100)

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
            plt.text(y, x, str(i), ha='center', va='center', color='green', fontsize=10)

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

    path, visited = hill_climbing(grid, start, goal, num_obstacles)

    if path:
        print("Camino encontrado:", path)
        print("Camino recorrido:", visited)
    else:
        print("No se encontró un camino válido.")

    draw_grid(grid, start, goal, path, visited)

if __name__ == "__main__":
    main()
