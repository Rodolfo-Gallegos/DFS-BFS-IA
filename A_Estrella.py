import matplotlib.pyplot as plt
import numpy as np
import random

# Inicializa una cuadrícula de tamaño 'n' y la llena de ceros.
def inicializar_cuadricula(n):
    return np.zeros((n, n), dtype=int)

# Comprueba si una posición (x, y) es válida en la cuadrícula y no es un obstáculo (valor 1).
def es_valida(x, y, cuadricula):
    return 0 <= x < len(cuadricula) and 0 <= y < len(cuadricula[0]) and cuadricula[x][y] == 0

# Genera obstáculos aleatorios en la cuadrícula.
def generar_obstaculos(cuadricula, n):
    for _ in range(n):
        x, y = random.randint(0, len(cuadricula) - 1), random.randint(0, len(cuadricula[0]) - 1)
        while cuadricula[x][y] == 1:
            x, y = random.randint(0, len(cuadricula) - 1), random.randint(0, len(cuadricula[0]) - 1)
        cuadricula[x][y] = 1

# Genera posiciones de inicio y meta en la cuadrícula sin obstáculos.
def generar_inicio_meta(cuadricula):
    celdas_libres = [(x, y) for x in range(len(cuadricula)) for y in range(len(cuadricula[0])) if cuadricula[x][y] == 0]
    if len(celdas_libres) < 2:
        raise ValueError("La cuadrícula no tiene suficientes celdas libres para establecer el inicio y la meta.")
    inicio, meta = random.sample(celdas_libres, 2)
    return inicio, meta

# Calcula la distancia de Manhattan entre dos puntos en la cuadrícula.
def distancia_manhattan(punto1, punto2):
    return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])

def a_star(cuadricula, inicio, meta):
    open_set = [inicio]  # Conjunto de nodos abiertos para explorar.
    came_from = {}  # Diccionario para rastrear cómo llegamos a cada nodo.
    
    g_n = {(celda[0], celda[1]): float('inf') for celda in np.ndindex(cuadricula.shape)}  # g_n para cada celda.
    g_n[inicio] = 0  # El g_n del inicio es 0.

    f_n = {(celda[0], celda[1]): float('inf') for celda in np.ndindex(cuadricula.shape)}  # f_n para cada celda.
    f_n[inicio] = distancia_manhattan(inicio, meta)  # Estimación inicial de f_n.

    while open_set:
        current = min(open_set, key=lambda celda: f_n[celda])  # Selecciona el nodo con el f_n más bajo.

        if current == meta:  # Si hemos llegado a la meta, reconstruimos el camino y lo devolvemos.
            camino = reconstruir_camino(came_from, current)
            return camino

        open_set.remove(current)  # Removemos el nodo actual del conjunto abierto.

        for neighbor in [(current[0], current[1] + 1), (current[0], current[1] - 1), (current[0] + 1, current[1]), (current[0] - 1, current[1])]:
            if es_valida(neighbor[0], neighbor[1], cuadricula):
                tentative_g_n = g_n[current] + 1  # Calcula el g_n tentativo.

                if tentative_g_n < g_n[neighbor]:
                    came_from[neighbor] = current  # Almacenamos cómo llegamos a esta celda.
                    g_n[neighbor] = tentative_g_n  # Actualizamos el g_n.
                    f_n[neighbor] = g_n[neighbor] + distancia_manhattan(neighbor, meta)  # Actualizamos el f_n.

                    if neighbor not in open_set:
                        open_set.append(neighbor)  # Agregamos el vecino al conjunto abierto.

    return None  # Si no se encuentra un camino, retornamos None.


# Reconstruye el camino desde la meta hasta el inicio.
def reconstruir_camino(came_from, actual):
    camino_total = [actual]
    while actual in came_from:
        actual = came_from[actual]
        camino_total.insert(0, actual)
    return camino_total

# Dibuja la cuadrícula con inicio, meta y el camino encontrado.
def dibujar_cuadricula(cuadricula, inicio, meta, camino, visitados):
    fig, ax = plt.subplots()

    ax.set_facecolor('white')
    tamano_celda = 1

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[0])):
            if cuadricula[i][j] == 1:
                ax.add_patch(plt.Rectangle((j * tamano_celda, i * tamano_celda), tamano_celda, tamano_celda, color='black'))
            elif cuadricula[i][j] == 0:
                if meta:
                    distancia = distancia_manhattan((i, j), meta)
                    maxima_distancia = max(len(cuadricula), len(cuadricula[0]))
                    valor_calor = 1 - (distancia / maxima_distancia)
                    color = plt.cm.viridis(valor_calor)
                else:
                    color = 'white'

                ax.add_patch(plt.Rectangle((j * tamano_celda, i * tamano_celda), tamano_celda, tamano_celda, color=color))

    plt.scatter(inicio[1] * tamano_celda + tamano_celda / 2, inicio[0] * tamano_celda + tamano_celda / 2, color='white', marker='o',
                s=100)
    plt.scatter(meta[1] * tamano_celda + tamano_celda / 2, meta[0] * tamano_celda + tamano_celda / 2, color='red', marker='x',
                s=100)

    if camino:
        camino_x, camino_y = zip(*camino)
        camino_x = [x * tamano_celda + tamano_celda / 2 for x in camino_x]
        camino_y = [y * tamano_celda + tamano_celda / 2 for y in camino_y]
        plt.plot(camino_y, camino_x, color='white', label='Camino')

    if visitados:
        visitados_x, visitados_y = zip(*visitados)
        visitados_x = [x * tamano_celda + tamano_celda / 2 for x in visitados_x]
        visitados_y = [y * tamano_celda + tamano_celda / 2 for y in visitados_y]
        for i, (x, y) in enumerate(zip(visitados_x, visitados_y), 1):
            plt.text(y, x, str(i), ha='center', va='center', color='white', fontsize=14)

    for i in range(len(cuadricula) + 1):
        plt.axhline(y=i * tamano_celda, color='black', linewidth=0.1)
    for j in range(len(cuadricula[0]) + 1):
        plt.axvline(x=j * tamano_celda, color='black', linewidth=0.1)

    plt.legend()
    plt.show()

# Función principal que ejecuta el algoritmo.
def main():
    n = 10
    cuadricula = inicializar_cuadricula(n)
    num_obstaculos = (n * n) // 4
    generar_obstaculos(cuadricula, num_obstaculos)

    try:
        inicio, meta = generar_inicio_meta(cuadricula)
    except ValueError as e:
        print(e)
        return

    camino = a_star(cuadricula, inicio, meta)

    if camino:
        print("Camino encontrado:", camino)
    else:
        print("No se encontró un camino válido.")

    dibujar_cuadricula(cuadricula, inicio, meta, camino, [])

if __name__ == "__main__":
    main()
